import os
from pathlib import Path


class Config:
    """
    统一管理花卉识别服务配置：
    - 路径（项目根、模型目录、uploads、db）
    - Flask/SQLAlchemy 配置
    """

    FILE = Path(__file__).resolve()

    BASE_DIR = FILE.parent
    ROOT = FILE.parents[2]
    PRODUCTION = os.environ.get('APP_ENV') == 'production'
    DATA_DIR = Path(os.environ.get('FLOWER_DATA_DIR', str(BASE_DIR / 'instance')))
    CORS_ORIGINS = [origin.strip() for origin in os.environ.get(
        'CORS_ORIGINS', 'http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173,http://127.0.0.1:5173'
    ).split(',') if origin.strip()]
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', '' if PRODUCTION else 'admin123')
    FLOWER_MODEL_DIR = os.environ.get('FLOWER_MODEL_DIR', str(ROOT / 'model_assets' / 'flower-resnet18'))
    FLOWER_DEVICE = os.environ.get('FLOWER_DEVICE', 'cpu')
    FLOWER_NUM_THREADS = int(os.environ.get('FLOWER_NUM_THREADS', '4'))

    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-should-be-changed')
    # 显式启用后可在缺少模型权重时预览网站，识别接口返回 503。
    PREVIEW_MODE = os.environ.get('FLOWER_PREVIEW_MODE', '0') == '1'
    # 请求体总大小限制（用于批量上传）；单张大小由业务逻辑单独限制
    MAX_CONTENT_LENGTH = 30 * 1024 * 1024  # 30MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

    # JWT 配置
    JWT_SECRET = os.environ.get('JWT_SECRET', 'jwt-dev-key-should-be-changed')
    JWT_EXPIRATION = 24 * 60 * 60  # 24小时
    JWT_EXPIRATION_REMEMBER = 7 * 24 * 60 * 60  # 7天（记住我）

    # 上传目录：统一走项目根 uploads
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', str(DATA_DIR / 'uploads') if PRODUCTION else str(ROOT / 'uploads'))

    # SQLite（固定到 backend/instance 下）
    DB_PATH = str(DATA_DIR / 'flower_classification.db')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f"sqlite:///{DB_PATH}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session 配置
    PERMANENT_SESSION_LIFETIME = 24 * 60 * 60  # 24小时
    SESSION_COOKIE_SECURE = PRODUCTION
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'  # 防止CSRF，允许same-site请求
    SESSION_COOKIE_NAME = 'flower_session'
