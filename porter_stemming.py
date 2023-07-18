class PorterStemmer:
    # I read the porter.txt file and found your note
    def __init__(self):
        self.step1a_replacements = {
            "sses": "ss",
            "ies": "i",
            "ss": "ss",
            "s": ""
        }

        self.step1b_replacements_ed = {
            "at": "ate",
            "bl": "ble",
            "iz": "ize"
        }

        self.step1b_replacements_ing = {
            "at": "ate",
            "bl": "ble",
            "iz": "ize"
        }

        self.step1c_replacement = {
            "y": "i"
        }

        self.step2_replacements = {
            "ational": "ate",
            "tional": "tion",
            "enci": "ence",
            "anci": "ance",
            "izer": "ize",
            "bli": "ble",
            "alli": "al",
            "entli": "ent",
            "eli": "e",
            "ousli": "ous",
            "ization": "ize",
            "ation": "ate",
            "ator": "ate",
            "alism": "al",
            "iveness": "ive",
            "fulness": "ful",
            "ousness": "ous",
            "aliti": "al",
            "iviti": "ive",
            "biliti": "ble"
        }

        self.step3_replacements = {
            "icate": "ic",
            "ative": "",
            "alize": "al",
            "iciti": "ic",
            "ical": "ic",
            "ful": "",
            "ness": ""
        }

        self.step4_replacements = {
            "al": "",
            "ance": "",
            "ence": "",
            "er": "",
            "ic": "",
            "able": "",
            "ible": "",
            "ant": "",
            "ement": "",
            "ment": "",
            "ent": "",
            "sion": "s",
            "tion": "t",
            "ou": "",
            "ism": "",
            "ate": "",
            "iti": "",
            "ous": "",
            "ive": "",
            "ize": ""
        }

        self.step5a_condition = lambda word: word.endswith("e") and self.count_measure(word[:-1]) > 1
        self.step5a_replacement = lambda word: word[:-1]

        self.step5b_condition = lambda word: self.count_measure(word) > 1 and self.ends_with_double_consonant(word)
        self.step5b_replacement = lambda word: word[:-1]

    def stem(self, word):

        word = word.lower()
        if len(word) < 3:
            return word
        # print('step1a', word)

        # Step 1a
        word = self.apply_replacements(word, self.step1a_replacements)
        # print('step1b', word)
        # Step 1b
        if word.endswith("eed"):
            if self.count_measure(word[:-3]) > 0:
                word = word[:-1]
        elif word.endswith("ed"):
            if self.contains_vowel(word[:-2]):
                word = self.process_suffix(word[:-2], self.step1b_replacements_ed)
        elif word.endswith("ing"):
            if self.contains_vowel(word[:-3]):
                word = self.process_suffix(word[:-3], self.step1b_replacements_ing)
        # print('step1c', word)

        # Step 1c
        word = self.process_suffix(word, self.step1c_replacement)
        # print('step2', word)

        # Step 2
        word = self.process_suffix(word, self.step2_replacements)
        # print('step3', word)

        # Step 3
        word = self.process_suffix(word, self.step3_replacements)
        # print('step4', word)

        # Step 4
        word = self.process_suffix(word, self.step4_replacements)
        # print('step5a', word)

        # Step 5a
        if self.step5a_condition(word):
            word = self.step5a_replacement(word)
        # print('step5b', word)

        # Step 5b
        if self.step5b_condition(word):
            word = self.step5b_replacement(word)
        #  print('step5b', word)

        return word

    def process_suffix(self, word, replacements):
        for suffix, replacement in replacements.items():
            if word.endswith(suffix):
                return word[:-len(suffix)] + replacement
        return word

    def count_measure(self, word):
        count = 0
        prev_char_vowel = False

        for char in word:
            if char in "aeiou":
                if not prev_char_vowel:
                    count += 1
                prev_char_vowel = True
            else:
                prev_char_vowel = False

        return count

    def contains_vowel(self, word):
        return any(char in "aeiou" for char in word)

    def ends_with_double_consonant(self, word):
        return len(word) >= 2 and word[-1] == word[-2] and word[-1] not in "aeiou"

    def apply_replacements(self, word, replacements):
        for suffix, replacement in replacements.items():
            if word.endswith(suffix):
                return word[:-len(suffix)] + replacement
        return word
