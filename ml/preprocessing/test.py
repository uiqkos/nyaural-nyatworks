import unittest

from preprocessing.transformers import Cleaner, Lemmatizer, StopWordsRemover, Stemmer


class TestTransformers(unittest.TestCase):
    def setUp(self) -> None:
        self.ip = 'Hello, its 136.43.98.36.'
        self.punctuation = 'Hello, it`s me~|!!'
        self.emails = 'Hi, example@example.com!'
        self.addresses = '2311 North Los Robles Avenue is good for you!'
        self.dates = '20 December 2006 or 13 May, 2007 or 13th of May?'
        self.texts = [self.ip, self.punctuation, self.emails, self.addresses, self.dates]

    def test_Cleaner(self):
        cleaner = Cleaner(generator=False)
        self.assertEqual(
            cleaner.transform(self.texts),
            ['Hello its ', 'Hello its me', 'Hi ', ' is good for you', ' or  or ']
        )

    def test_Lemmatizer(self):
        lemmatizer = Lemmatizer(generator=False)

        self.assertEqual(
            lemmatizer.transform(['its am the cars cows'.split()]),
            [['it', 'am', 'the', 'better', 'car', 'cow']]
        )

    def test_Stemmer(self):
        # todo check different lemmatizers
        stemmer = Stemmer(generator=False)

        self.assertEqual(
            stemmer.transform(
                [['Connects', 'Connecting', 'Connections', 'Connected', 'Connection', 'Connectings', 'Connect']]
            ),
            [['connect'] * 7]
        )

    def test_StopWordsRemover(self):
        stopwordsremover = StopWordsRemover(generator=False)

        self.assertEqual(
            stopwordsremover.transform(["Nick likes to play football, however he is not too fond of tennis.".split()]),
            [['Nick', 'likes', 'play', 'football,', 'however', 'fond', 'tennis.']]
        )
