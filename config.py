import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = Path(__file__).resolve().parent / 'ml' / 'data'

config: dict = json.load(open(BASE_DIR.joinpath('config.json'), 'r'))
