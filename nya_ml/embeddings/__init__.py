from typing import Dict, Callable

from nya_ml.embeddings.embeddingsource import EmbeddingSource
from nya_utils.datatools import expand_dict

_embedding_by_name = expand_dict({
    ('ruwiki', 'ru-wiki', 'ruwikicorp',
     name := 'ruwikiruscorpora_upos_cbow_300_10_2021'): EmbeddingSource(
        name=name,
        filename=name + '.zip',
        url='http://vectors.nlpl.eu/repository/20/220.zip'
    ),

})

get_source: Callable[[str], EmbeddingSource] = _embedding_by_name.get
