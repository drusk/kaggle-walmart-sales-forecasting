import os
import unittest

from extract_features import (DateTransformer, NumericalFeatureExtractor,
                              OneHotEncoder)


def path(filename):
    """
    Performs path resolution to the test data file.
    """
    return os.path.join(os.path.dirname(__file__), filename)


class BaseTest(unittest.TestCase):
    def assert_array_equals(self, actual, expected):
        for i, row in enumerate(actual.tolist()):
            self.assertListEqual(row, expected[i])


class OneHotEncoderTest(BaseTest):
    def setUp(self):
        self.transformer = OneHotEncoder()

    def test_transform(self):
        numerical = self.transformer.transform(
            ["awful", "poor", "ok", "good", "great"]
        )

        self.assert_array_equals(
            numerical,
            [[1, 0, 0, 0, 0],
             [0, 1, 0, 0, 0],
             [0, 0, 1, 0, 0],
             [0, 0, 0, 1, 0],
             [0, 0, 0, 0, 1]]
        )

    def test_transform_duplicates(self):
        numerical = self.transformer.transform(
            ["awful", "poor", "awful", "ok", "good", "great",
             "good", "poor"]
        )

        self.assert_array_equals(
            numerical,
            [[1, 0, 0, 0, 0],
             [0, 1, 0, 0, 0],
             [1, 0, 0, 0, 0],
             [0, 0, 1, 0, 0],
             [0, 0, 0, 1, 0],
             [0, 0, 0, 0, 1],
             [0, 0, 0, 1, 0],
             [0, 1, 0, 0, 0]]
        )


class DateTransformerTest(BaseTest):
    def setUp(self):
        self.transformer = DateTransformer()

    def test_transform(self):
        numerical = self.transformer.transform(
            [
                "2010-02-05",
                "2010-02-12",
                "2010-02-19",
                "2010-02-12",
                "2010-03-12"
            ]
        )

        self.assertListEqual(
            numerical.tolist(),
            [0, 1, 2, 1, 3]
        )


class NumericalFeatureExtractorTest(BaseTest):
    def test_extract_dates_and_categorical(self):
        extractor = NumericalFeatureExtractor(path("head_full_csv"))
        feature_vectors = extractor.get_feature_vectors()

        self.assert_array_equals(
            feature_vectors,
            [
                [1, 1, 0, 151315, 0, 42.31, 2.572, 0, 0, 0, 0, 0,
                 211.0963582, 8.106, 0, 24924.5],
                [1, 0, 1, 151315, 1, 42.31, 2.572, 0, 0, 0, 0, 0,
                 211.0963582, 8.106, 0, 50605.27],
                [1, 1, 0, 151315, 2, 42.31, 2.572, 100.0, 0, 0, 0, 0,
                 211.0963582, 8.106, 1, 13740.12],
                [1, 1, 0, 151315, 0, 42.31, 2.572, 0, 0, 0, 0, 0,
                 211.0963582, 8.106, 0, 39954.04],
                [1, 1, 0, 151315, 2, 42.31, 2.572, 0, 0, 0, 0, 50.0,
                 211.0963582, 8.106, 0, 32229.38]
            ]
        )



if __name__ == '__main__':
    unittest.main()
