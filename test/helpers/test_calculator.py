import unittest
from helpers.calculator import *

class TestCostCalculator(unittest.TestCase):

    def test_base_cost(self):
        calculator = CostCalculator("hello")
        self.assertEqual(calculator.base_cost(), BASE_COST)

    def test_symbol_cost(self):
        calculator = CostCalculator("hello!")
        expected_cost = len("hello!") * SYMBOL_COST
        self.assertEqual(calculator.symbol_cost(), expected_cost)

    def test_length_cost_under_threshold(self):
        calculator = CostCalculator("short text")
        self.assertEqual(calculator.length_cost(), 0)

    def test_length_cost_over_threshold(self):
        long_text = "a" * (LENGTH_PENALTY_THRESHOLD + 1)
        calculator = CostCalculator(long_text)
        self.assertEqual(calculator.length_cost(), LENGTH_PENALTY)

    def test_vowels_cost(self):
        text_with_vowels_every_third = "abcdefghijklmno"
        calculator = CostCalculator(text_with_vowels_every_third)
        # 'e' and 'o' are vowels at index 2 and 8 (in 0-indexed system)
        expected_cost = 2 * VOWEL_COST
        self.assertEqual(calculator.vowels_cost(), expected_cost)

    def test_vowels_cost_no_vowels(self):
        calculator = CostCalculator("bcdfgh")
        self.assertEqual(calculator.vowels_cost(), 0)

    def test_uniq_bonus_no_duplicates(self):
        calculator = CostCalculator("unique words only")
        self.assertEqual(calculator.uniq_bonus(), -UNIQ_REWARD)

    def test_uniq_bonus_with_duplicates(self):
        calculator = CostCalculator("repeated repeated words")
        self.assertEqual(calculator.uniq_bonus(), 0)

    def test_word_cost_small_words(self):
        calculator = CostCalculator("a bc def")
        expected_cost = 3 * SMALL_WORD_COST
        self.assertEqual(calculator.word_cost(), expected_cost)

    def test_word_cost_mixed_word_sizes(self):
        calculator = CostCalculator("a longword abcde")
        expected_cost = SMALL_WORD_COST + LARGE_WORD_COST + MEDIUM_WORD_COST
        self.assertEqual(calculator.word_cost(), expected_cost)

    def test_palindrome_multiplier_palindrome(self):
        calculator = CostCalculator("A man a plan a canal Panama")
        self.assertEqual(calculator.palindrome(), PALINDROME_MULTIPLIER)

    def test_palindrome_multiplier_non_palindrome(self):
        calculator = CostCalculator("This is not a palindrome")
        self.assertEqual(calculator.palindrome(), 1)

    def test_calculate_score_non_palindrome(self):
        calculator = CostCalculator("abc def")
        # Manually calculate expected score
        expected_score = BASE_COST
        expected_score += len("abc def") * SYMBOL_COST
        expected_score += calculator.vowels_cost()
        expected_score += calculator.word_cost()
        expected_score += calculator.uniq_bonus()
        expected_score = calculator.check_correct_min(expected_score)
        self.assertEqual(calculator.calculate_score(), round(expected_score, 3))

    def test_calculate_score_palindrome(self):
        calculator = CostCalculator("A man a plan a canal Panama")
        # Similar to above, calculate expected score manually
        expected_score = BASE_COST
        expected_score += len("A man a plan a canal Panama") * SYMBOL_COST
        expected_score += calculator.vowels_cost()
        expected_score += calculator.word_cost()
        expected_score = calculator.check_correct_min(expected_score)
        expected_score *= PALINDROME_MULTIPLIER
        self.assertEqual(calculator.calculate_score(), round(expected_score, 3))


if __name__ == "__main__":
    unittest.main()