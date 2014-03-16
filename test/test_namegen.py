from namegen.namegen import *
import unittest

class TestNamegen(unittest.TestCase):

    def test_with_one_syllable(self):
        examples = ['na','nana','nanana','nanana']

        for i in range(1,11):
            for seed in xrange(10):
                language = Language.language_from_samples(examples,frac_2s=i/10.0,frac_3s=0.0,seed=seed)
                self.assertEqual("na",language.name_fixed_length(num_syllables=1,capitalize=False))
                self.assertEqual("nana",language.name_fixed_length(num_syllables=2,capitalize=False))
                self.assertEqual("nanana",language.name_fixed_length(num_syllables=3,capitalize=False))
                self.assertEqual("nananana",language.name_fixed_length(num_syllables=4,capitalize=False))
                self.assertEqual("nanananana",language.name_fixed_length(num_syllables=5,capitalize=False))

    def test_with_few_syllables(self):
        examples = ['nanu','nena','ninino','nenuno']

        for seed in xrange(10):
            language = Language.language_from_samples(examples,frac_2s=1.0,frac_3s=0.0,seed=seed)
            name = language.name_fixed_length(num_syllables=1,capitalize=False)
            self.assertTrue(name in ["na","ne","ni","no","nu"])
            name = language.name_fixed_length(num_syllables=2,capitalize=False)
            self.assertTrue(name[0:2] in ["na","ne","ni","no","nu"])
            self.assertTrue(name[2:4] in ["na","ne","ni","no","nu"])
            name = language.name_fixed_length(num_syllables=3,capitalize=False)
            self.assertTrue(name[0:2] in ["na","ne","ni","no","nu"])
            self.assertTrue(name[2:4] in ["na","ne","ni","no","nu"])
            self.assertTrue(name[4:6] in ["na","ne","ni","no","nu"])
            name = language.name_fixed_length(num_syllables=4,capitalize=False)
            self.assertTrue(name[0:2] in ["na","ne","ni","no","nu"])
            self.assertTrue(name[2:4] in ["na","ne","ni","no","nu"])
            self.assertTrue(name[4:6] in ["na","ne","ni","no","nu"])
            self.assertTrue(name[6:8] in ["na","ne","ni","no","nu"])
            name = language.name_fixed_length(num_syllables=5,capitalize=False)
            self.assertTrue(name[0:2] in ["na","ne","ni","no","nu"])
            self.assertTrue(name[2:4] in ["na","ne","ni","no","nu"])
            self.assertTrue(name[4:6] in ["na","ne","ni","no","nu"])
            self.assertTrue(name[6:8] in ["na","ne","ni","no","nu"])
            self.assertTrue(name[8:10] in ["na","ne","ni","no","nu"])
