import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / 'data'

config: dict = json.load(open(BASE_DIR.joinpath('config.json'), 'r'))
