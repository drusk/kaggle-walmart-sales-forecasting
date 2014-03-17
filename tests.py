import os
import unittest

from extract_features import (NumericalFeatureExtractor,
                              NumberTransformer, OneHotEncoder, Transformer)


def path(filename):
    """
    Performs path resolution to the test data file.
    """
    return os.path.join(os.path.dirname(__file__), filename)


class BaseTest(unittest.TestCase):
    def assert_array_equals(self, actual, expected):
        for i, row in enumerate(actual.tolist()):
            for j in xrange(len(row)):
                actual_val = row[j]
                expected_val = expected[i][j]

                self.assertAlmostEqual(
                    expected_val, actual_val,
                    msg="expected (%d, %d) to be %f, but was %f" % (
                        i, j, expected_val, actual_val)
                )


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


class TransformerTest(BaseTest):
    def test_normalize(self):
        transformer = Transformer(normalize=True)

        normalized = transformer.do_normalize([5, 2, 8, 11, 7])
        self.assertListEqual(
            normalized.tolist(),
            [1.0 / 3, 0, 2.0 / 3, 1, 5.0 / 9]
        )


class NumberTransformerTeset(BaseTest):
    def test_normalize(self):
        transformer = NumberTransformer(normalize=True)

        normalized = transformer.do_normalize([5, 2, 8, 11, 7])
        self.assertListEqual(
            normalized.tolist(),
            [1.0 / 3, 0, 2.0 / 3, 1, 5.0 / 9]
        )


class NumericalFeatureExtractorTest(BaseTest):
    def test_extract_dates_and_categorical(self):
        extractor = NumericalFeatureExtractor(path("head_full_csv"))
        feature_vectors = extractor.extract_features()

        self.assert_array_equals(
            feature_vectors,
            [
                [1, 1, 1, 0, 151315, 2010, 2, 5, 42.31, 2.572, 0, 0, 0, 0, 0,
                 211.0963582, 8.106, 0, 24924.5],
                [1, 2, 0, 1, 202307, 2010, 2, 12, 56.47, 3.564, 0, 0, 0, 0, 0,
                 129.5183333, 8.106, 0, 50605.27],
                [1, 1, 1, 0, 57197, 2010, 2, 19, 64.88, 2.572, 100.0, 0, 0, 0, 0,
                 211.0963582, 8.106, 1, 13740.12],
                [1, 3, 1, 0, 196321, 2011, 2, 5, 77.2, 2.572, 0, 0, 0, 0, 0,
                 130.9776667, 8.106, 0, 39954.04],
                [1, 2, 1, 0, 39910, 2010, 2, 19, 82.99, 2.572, 0, 0, 0, 0, 50.0,
                 211.0963582, 8.106, 0, 32229.38]
            ]
        )

    def test_extract_normalize(self):
        extractor = NumericalFeatureExtractor(path("head_full_csv"),
                                              normalize=True)
        feature_vectors = extractor.extract_features()

        self.assert_array_equals(
            feature_vectors,
            [
                [0, 0, 1, 0, 0.68600405179898643447,
                 0.0, 0.16666666666666666666, 0.16129032258064516129,
                 0.0, 0.0, 0, 0, 0, 0, 0.0, 1.0, 0.0, 0, 24924.5],
                [0, 0.5, 0, 1, 1.0,
                 0.0, 0.16666666666666666666, 0.38709677419354838709,
                 0.34808259587020648967, 1.0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0,
                 50605.27],
                [0, 0, 1, 0, 0.10644901075758788647,
                 0.0, 0.16666666666666666666, 0.61290322580645161290,
                 0.55481809242871189773, 0.0, 1.0, 0, 0, 0, 0.0,
                 1.0, 0.0, 1, 13740.12],
                [0, 1, 1, 0, 0.96313971317204135544,
                 1.0, 0.16666666666666666666, 0.16129032258064516129,
                 0.85766961651917404129, 0.0, 0, 0, 0, 0, 0.0,
                 0.01788880524858110410, 0.0, 0, 39954.04],
                [0, 0.5, 1, 0, 0.0,
                 0.0, 0.16666666666666666666, 0.61290322580645161290,
                 1.0, 0.0, 0, 0, 0, 0, 1.0, 1.0, 0.0, 0, 32229.38]
            ]
        )


if __name__ == '__main__':
    unittest.main()
