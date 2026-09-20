"""Model installation verifies the trained five-class weights."""
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.download_flower_model import ROOT, MODEL_NAME, install, verified


class ModelInstallTests(unittest.TestCase):
    def test_local_install_and_idempotence(self):
        with tempfile.TemporaryDirectory() as tmp, patch.dict(os.environ, {'FLOWER_MODEL_DIR': tmp, 'FLOWER_MODEL_URL': ''}):
            install(ROOT / 'model_assets/flower-resnet18' / MODEL_NAME)
            target = Path(tmp) / MODEL_NAME
            self.assertTrue(verified(target))
            stamp = target.stat().st_mtime_ns
            install()
            self.assertEqual(target.stat().st_mtime_ns, stamp)

    def test_missing_source_and_wrong_weight_fail(self):
        with tempfile.TemporaryDirectory() as tmp, patch.dict(os.environ, {'FLOWER_MODEL_DIR': tmp, 'FLOWER_MODEL_URL': ''}):
            with self.assertRaisesRegex(RuntimeError, 'missing or invalid'):
                install()
            invalid = Path(tmp) / 'incorrect.pt'
            invalid.write_bytes(b'incorrect weights')
            with self.assertRaisesRegex(RuntimeError, 'SHA256 mismatch'):
                install(invalid)
            self.assertFalse((Path(tmp) / MODEL_NAME).exists())
            self.assertFalse((Path(tmp) / 'best-ckpt2.pt.part').exists())
