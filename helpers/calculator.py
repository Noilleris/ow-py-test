import re

BASE_COST = 1.0
SYMBOL_COST = 0.05
LENGTH_PENALTY_THRESHOLD = 100
LENGTH_PENALTY = 5.0
VOWEL_COST = 0.35
UNIQ_REWARD = 2.0
LARGE_WORD_LEN = 7
MEDIUM_WORD_LEN = 3
SMALL_WORD_COST = 0.1
MEDIUM_WORD_COST = 0.2
LARGE_WORD_COST = 0.3
PALINDROME_MULTIPLIER = 2

WORD = r"[a-zA-Z'-]+"
VOWELS = r'[aeiouAEIOU]'

VOWELS_START = 2
VOWELS_STEP = 3

class CostCalculator:
    def __init__(self, text: str):
        self.text = text
        self.words = re.findall(WORD, text)

    def base_cost(self):
        return BASE_COST

    def symbol_cost(self):
        return len(self.text) * SYMBOL_COST

    def length_cost(self):
        if len(self.text) >= LENGTH_PENALTY_THRESHOLD:
            return LENGTH_PENALTY
        return 0

    def vowels_cost(self):
        third_vowels = len(re.findall(VOWELS, self.text[VOWELS_START::VOWELS_STEP]))

        return third_vowels * VOWEL_COST

    def uniq_bonus(self):

        unique_words = set(self.words)

        if len(self.words) == len(unique_words):
            return -UNIQ_REWARD

        return 0

    def word_cost(self):
        cost = 0

        for word in self.words:
            if len(word) > LARGE_WORD_LEN:
                cost += LARGE_WORD_COST
            elif len(word) > MEDIUM_WORD_LEN:
                cost += MEDIUM_WORD_COST
            else:
                cost += SMALL_WORD_COST

        return cost

    def check_correct_min(self, total_cost):
        return max(BASE_COST, total_cost)

    def palindrome(self):
        cleaned_text = re.sub(r'\W+', '', self.text).lower()
        if len(cleaned_text) > 1 and cleaned_text == cleaned_text[::-1]:
            return PALINDROME_MULTIPLIER

        return 1

    def calculate_score(self):
        total_cost = self.base_cost()

        total_cost += self.symbol_cost()

        total_cost += self.length_cost()

        total_cost += self.vowels_cost()

        total_cost += self.uniq_bonus()

        total_cost += self.word_cost()

        total_cost = self.check_correct_min(total_cost)

        total_cost *= self.palindrome()

        return round(total_cost,3)