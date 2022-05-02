import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / 'data'
MODELS_PATH = BASE_DIR / 'models'

config: dict = json.load(open(BASE_DIR.joinpath('config.json'), 'r'))
