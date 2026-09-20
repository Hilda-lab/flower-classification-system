"""Install the trained five-class model from a local file or configured URL."""
import argparse
import hashlib
import os
import shutil
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL_NAME = 'best-ckpt2.pt'
MODEL_SHA256 = 'db18cc2e517fa7f008216164db8a7124856969739015072a00235d9ef3145b44'


def verified(path):
    return path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == MODEL_SHA256


def install(source=None):
    model_dir = Path(os.environ.get('FLOWER_MODEL_DIR', ROOT / 'model_assets' / 'flower-resnet18'))
    target = model_dir / MODEL_NAME
    if verified(target):
        print(f'Already verified: {target}')
        return
    url = os.environ.get('FLOWER_MODEL_URL')
    if not source and not url:
        raise RuntimeError('Five-class model missing or invalid. Use --source PATH to best-ckpt2.pt, '
                           'or set FLOWER_MODEL_URL to a direct download URL for that file.')
    model_dir.mkdir(parents=True, exist_ok=True)
    partial = target.with_suffix('.pt.part')
    try:
        if source:
            shutil.copyfile(source, partial)
        else:
            if not url.startswith('https://'):
                raise ValueError('FLOWER_MODEL_URL must use HTTPS')
            with urllib.request.urlopen(url, timeout=60) as response, partial.open('wb') as stream:
                shutil.copyfileobj(response, stream)
        if not verified(partial):
            raise RuntimeError('SHA256 mismatch: expected the trained five-class best-ckpt2.pt')
        partial.replace(target)
    finally:
        partial.unlink(missing_ok=True)
    print(f'Installed and verified: {target}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, help='Local path to the trained best-ckpt2.pt')
    args = parser.parse_args()
    install(args.source)
