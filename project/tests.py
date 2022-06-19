import unittest
import pandas as pd
import numpy as np
from monkey_model import Monkey
from utils import check_hexacolor
from utils import euclidean_distance
from monkey_classif import read_monkeys_from_csv
from monkey_classif import compute_knn


class TestMonkeyKnn(unittest.TestCase):

    def testHexaCode(self):
        """This method tests that check_hexacolor() catches
        valid hexadecimal codes for fur_color."""

        good_codes = ["#123456", "#ABCDEF", "#abcdef", "#aBc123"]               # valid hexa codes

        for i in good_codes:
            self.assertTrue(check_hexacolor(i))                                 # function must return True

    def testHexaError(self):
        """This method tests that the Monkey class raises an error for
        invalid hexadecimal codes for fur_color."""

        bad_codes = ["ABCDEF", "abcdef", "#1234567", "#ff&fff"]                 # invalid hexa codes

        for i in bad_codes:
            self.assertRaises(ValueError, Monkey, i, 1.678, 74.123, "gorilla")  # class must raise ValueError

    def testBmiFct(self):
        """This method tests that compute_bmi() returns positive numbers."""

        specimen_1 = Monkey("#000000", 1.574, 45.500, "underweight human")      # realistic values for humans
        specimen_2 = Monkey("#000000", 1.701, 59.100, "healthy human")
        specimen_3 = Monkey("#000000", 1.803, 86.400, "overweight human")
        specimen_4 = Monkey("#000000", 1.549, 77.300, "obese human")

        gold_bmis = [specimen_1.compute_bmi(),
                     specimen_2.compute_bmi(),
                     specimen_3.compute_bmi(),
                     specimen_4.compute_bmi()]

        for i in gold_bmis:
            self.assertGreater(i, 0)                                            # k must be > 0

    def testDataframe(self):
        """This method tests that read_monkeys_from_csv()
        returns a pandas dataframe of the correct format."""

        # .csv with 4 incorrect headers, 5 incorrect rows, 1 correct row
        bad_csv = "test_data/test_df.csv"           # import .csv as a pandas dataframe
        test_df = read_monkeys_from_csv(bad_csv)    # put it in a variable

        gold_headers = ["id", "fur_color", "species", "size", "weight",
                        "monkey", "fur_color_int", "bmi", "empty_str"]

        # testing headers renaming, reordering, creation
        self.assertEqual(list(test_df.columns), gold_headers)                   # headers must == gold_headers
        # testing row drop for NaN values, neg size, neg weight, incorrect hex color codes
        self.assertEqual(test_df.shape[0], 2)                                   # must drop all rows but two
        # testing hex to int conversion
        self.assertEqual(type(test_df["fur_color_int"].iloc[0]), np.int64)      # value must be int

    def testEucliDist(self):
        """This method tests that euclidean_distance() makes accurate computations."""

        monkey_1_bmi = 92.73
        monkey_1_color = 3020328
        monkey_2_bmi = 76.01
        monkey_2_color = 1188122
        test_distance = euclidean_distance(monkey_1_bmi, monkey_1_color, monkey_2_bmi, monkey_2_color)

        self.assertEqual(round(test_distance, 2), 1832206.00)       # test_distance (2 decimals) must be 1832206.00

    def testKnn(self):
        """This method tests that compute_knn() makes accurate guesses."""

        knn_df = "test_data/test_knn.csv"           # .csv with 5 labelled bonobos and 1 unlabelled bonobo
        test_knn = pd.read_csv(knn_df)              # import .csv as a pandas dataframe

        guess_df = compute_knn(test_knn)            # make a guess

        gold_count = 6                                          # the df should have 6 labelled bonobos now
        test_count = int(guess_df["species"].value_counts())    # how many there are in the df

        self.assertEqual(test_count, gold_count)                # which must be 6


if __name__ == '__main__':
    unittest.main()
