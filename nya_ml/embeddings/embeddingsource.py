import os
from pathlib import Path

import gensim
from torchnlp.download import download_file_maybe_extract


class EmbeddingSource:
    def __init__(self, name, url, filename):
        self.url = url
        self.name = name
        self.filename = filename

    def load(self, directory: Path) -> gensim.models.KeyedVectors:
        emb_directory = directory.joinpath(self.name)
        emb_directory.mkdir(exist_ok=True, parents=True)

        if (path := emb_directory.joinpath('model.bin')).exists():
            model = gensim.models.KeyedVectors.load_word2vec_format(
                str(path),
                binary=True
            )
            return model

        download_file_maybe_extract(
            url=self.url,
            directory=str(emb_directory),
            filename=self.filename,
            check_files=['model.bin']
        )

        os.remove(emb_directory / self.filename)

        return self.load(directory)
