"""Real-model API checks using an isolated SQLite database and upload directory."""
import io
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from flower_classification_backend.backend.config import Config


class FlowerIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.original = (Config.SQLALCHEMY_DATABASE_URI, Config.UPLOAD_FOLDER, Config.PREVIEW_MODE)
        Config.SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(Path(cls.temp.name) / 'test.db')
        Config.UPLOAD_FOLDER = str(Path(cls.temp.name) / 'uploads')
        Config.PREVIEW_MODE = False
        from flower_classification_backend.backend.app import create_app
        from flower_classification_backend.backend.models import User
        from flower_classification_backend.backend.extensions import db
        from flower_classification_backend.backend.services.jwt_service import JWTManager
        cls.app = create_app()
        cls.app.config['TESTING'] = True
        cls.client = cls.app.test_client()
        with cls.app.app_context():
            user = User(username='flower-test', email='flower-test@example.com')
            db.session.add(user)
            db.session.commit()
            cls.headers = {'Authorization': 'Bearer ' + JWTManager.encode_token(user.id, user.username)}
        with zipfile.ZipFile(Path(Config.FLOWER_MODEL_DIR) / 'datasets.zip') as archive:
            names = sorted(n for n in archive.namelist() if n.startswith('datasets/test/Sunflower/') and n.lower().endswith(('.jpg', '.jpeg', '.png')))
            cls.photo = archive.read(names[0])

    @classmethod
    def tearDownClass(cls):
        from flower_classification_backend.backend.extensions import db
        with cls.app.app_context():
            db.session.remove()
            db.engine.dispose()
        Config.SQLALCHEMY_DATABASE_URI, Config.UPLOAD_FOLDER, Config.PREVIEW_MODE = cls.original
        cls.temp.cleanup()

    def upload(self, endpoint='/api/detect'):
        return self.client.post(endpoint, headers=self.headers,
                                data={'file': (io.BytesIO(self.photo), 'sunflower.jpg')})

    def test_single_result_image_history_and_statistics(self):
        response = self.upload()
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        top = data['results'][0]
        self.assertEqual(top['class_name'], '向日葵')
        self.assertEqual(top['task'], 'flower')
        self.assertIsNone(top['bbox'])
        self.assertAlmostEqual(data['average_confidence'], top['confidence'])
        for key in ('original_url', 'result_url'):
            with self.client.get(data[key], headers=self.headers) as image_response:
                self.assertEqual(image_response.status_code, 200)
        history = self.client.get('/api/user/history', headers=self.headers).get_json()
        self.assertTrue(any(r['results'][0]['class_name'] == '向日葵' for r in history['data']))
        from flower_classification_backend.backend.managers.stats_manager import StatsManager
        from flower_classification_backend.backend.extensions import db
        from flower_classification_backend.backend.models import DetectionHistory
        with self.app.app_context():
            db.session.add(DetectionHistory(image_path='legacy', result=json.dumps([
                {'class_name': '厨余垃圾-菠萝', 'confidence': 0.8}]), confidence=0.8))
            db.session.commit()
            counts = StatsManager()._get_class_distribution()
            self.assertGreaterEqual(counts['向日葵'], 1)
            self.assertEqual(counts['历史垃圾识别'], 1)

    def test_batch_partial_failure(self):
        response = self.client.post('/api/detect/batch', headers=self.headers, data={
            'files': [(io.BytesIO(self.photo), 'flower.jpg'), (io.BytesIO(b'bad'), 'bad.txt')]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['success_count'], 1)
        self.assertEqual(response.get_json()['failed_count'], 1)

    def test_realtime_matches_single(self):
        single = self.upload().get_json()
        response = self.upload('/api/detect/realtime')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['results'], single['results'])

    def test_auth_preview_and_invalid_extension(self):
        self.assertEqual(self.client.post('/api/detect').status_code, 401)
        response = self.client.post('/api/detect', headers=self.headers,
                                    data={'file': (io.BytesIO(b'bad'), 'bad.txt')})
        self.assertEqual(response.status_code, 400)
        model = self.app.extensions['yolo']
        try:
            self.app.extensions['yolo'] = None
            self.assertEqual(self.upload().status_code, 503)
        finally:
            self.app.extensions['yolo'] = model


if __name__ == '__main__':
    unittest.main()
