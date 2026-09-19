"""Download pinned public release assets, verifying SHA256 before replacement."""
import argparse
import hashlib
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://github.com/LIU42/FlowerClassify/releases/download/v1.4.0/'
ASSETS = {
    'best-ckpt1.pt': 'be70e44fae334d14d4485d6fb49cb9b31637ebcdc2156b32da78678bd605d0f1',
    'datasets.zip': '6804192695a6211c9fad1f3024c29ed9666d0e9115e0ccd310b67c1a46ceddf0',
}


def download(name):
    target = ROOT / 'model_assets' / 'flower-resnet18' / name
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.is_file() and hashlib.sha256(target.read_bytes()).hexdigest() == ASSETS[name]:
        print(f'Already verified: {target.name}')
        return
    partial = target.with_suffix(target.suffix + '.part')
    digest = hashlib.sha256()
    with urllib.request.urlopen(BASE + name, timeout=60) as response, partial.open('wb') as stream:
        while chunk := response.read(1024 * 1024):
            digest.update(chunk)
            stream.write(chunk)
    if digest.hexdigest() != ASSETS[name]:
        raise RuntimeError(f'SHA256 mismatch: {name}; partial file retained for inspection')
    partial.replace(target)
    print(f'Downloaded and verified: {name}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--test-data', action='store_true', help='Also download the test dataset archive for validation')
    args = parser.parse_args()
    download('best-ckpt1.pt')
    if args.test_data:
        download('datasets.zip')
