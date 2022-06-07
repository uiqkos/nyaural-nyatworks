import os
from pathlib import Path
from typing import Iterator


def file_names(path):
    return list(zip(*os.walk(path)))[2][0]


def file_paths(path) -> Iterator[Path]:
    return map(path.joinpath, file_names(path))
