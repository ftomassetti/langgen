from os import listdir
from os.path import isfile, join
import random
from random import Random
import itertools

__version__ = "0.1.3"

# Load language samples from the given directory
def load_all_lang_samples(path='lang_samples'):
	lang_files = [ f for f in listdir(path) if isfile(join(path,f)) ]
	lang_samples = {}
	for lf in lang_files:
		with open(join(path,lf)) as f:
			content = f.readlines()
		# remove the extension
		lang_name = lf[0:-4]
		lang_samples[lang_name] = content
	return lang_samples

# Represent a single language, able to generate "similar" names.
class Language:

	@staticmethod
	def language_from_samples(samples,frac_2s=0.2,frac_3s=0.05,seed=None):
		if seed==None:
			seed=random.randint(0,2**16)

		samples = [s.strip().replace(" ","_").lower() for s in samples]
		sample_str = ' '+(' '.join(samples))+ ' '
		syllables = Language._get_best_syllables(2, frac_2s, sample_str)

		# optionally, do the same with 3 letters syllables (slower)
		if frac_3s>0.0:
			syllables.extend(Language._get_best_syllables(3, frac_3s, sample_str))

		(combinations, starts, ends) = Language._count_combinations(syllables, sample_str)
		language = Language(syllables,starts,ends,combinations,seed)
		return language

	def __init__(self, syllables, starts, ends, combinations,seed=None):
		if len(starts)==0:
			raise Exception("No syllable to start the word")

		if seed==None:
			seed=random.randint(0,2**16)
		self.rnd = Random(seed)

		self.syllables = syllables
		self.starts = starts
		self.ends = ends
		self.combinations = combinations
		self.min_syl = 2
		self.max_syl = 4

	def name(self,capitalize=True):
		num_syllables = self.rnd.randint(self.min_syl, self.max_syl)
		
		# turn ends list of tuples into a dictionary
		ends_dict = dict(self.ends)
		
		# we may have to repeat the process if the first "min_syl" syllables were a bad choice
		# and have no possible continuations; or if the word is in the forbidden list.
		word = []; 

		# start word with the first syllable
		syl = self._select_syllable(self.starts, 0)
		word = [self.syllables[syl]]
		while len(word) < (num_syllables-1) and syl!=None:	
			# select next syllable
			syl = self._select_syllable(self.combinations[syl], 0)			
			if syl!=None:
				word.append(self.syllables[syl])
		
		syl = self._select_syllable(self.ends, 0)
		if syl!=None:
			word.append(self.syllables[syl])
			
		word_str = ''.join(word)			
		if capitalize:
			word_str = word_str.capitalize()
		word_str = word_str.replace("_"," ")
		return word_str

	def name_fixed_length(self,num_syllables=None,capitalize=True):
		if num_syllables==None:
			num_syllables = self.rnd.randint(self.min_syl, self.max_syl)
		
		# turn ends list of tuples into a dictionary
		ends_dict = dict(self.ends)
		
		# we may have to repeat the process if the first "min_syl" syllables were a bad choice
		# and have no possible continuations; or if the word is in the forbidden list.
		word = []; 

		# start word with the first syllable
		syl = self._select_syllable(self.starts, 0)
		word = [self.syllables[syl]]
		while len(word) < (num_syllables-1):	
			# select next syllable
			continuations = self.combinations[syl]
			# ok, let's avoid the ending of the word
			if len(continuations)==0:
				continuations = self.starts
			syl = self._select_syllable(continuations, 0, noneAllowed=False)			
			#if syl==None:
			#	raise Exception("None returned while looking in combinations "+str(self.combinations))
			word.append(self.syllables[syl])
		
		# if the word is one syllable long there is no ending
		if num_syllables>1:
			syl = self._select_syllable(self.ends, 0)
			word.append(self.syllables[syl])
			
		word_str = ''.join(word)			
		if capitalize:
			word_str = word_str.capitalize()
		word_str = word_str.replace("_"," ")
		return word_str		

	def _select_syllable(self, counts, end_count, noneAllowed=True):
		if len(counts) == 0: 
			if not noneAllowed:
				raise Exception("No elements, but none is not allowed")
			return None  #no elements to choose from
		
		# "counts" holds cumulative counts, so take the last element in the list
		# (and 2nd in that tuple) to get the sum of all counts
		chosen = self.rnd.randint(0, counts[-1][1] + end_count)
		
		for (syl, count) in counts:
			if count >= chosen:
				return syl

		if not noneAllowed:
			return self._select_syllable(counts,end_count,noneAllowed)
		return None

	@staticmethod
	def _get_count(count_tuple):
		return count_tuple[1]

	@staticmethod
	def _get_best_syllables(num_letters, fraction, sample):
		alphabet = [chr(i) for i in range(ord('a'), ord('z') + 1)]
		
		# get all possible syllables using this number of letters, then count
		# them in the sample. output is list of tuples (syllable, count).
		counts = [(''.join(letters), sample.count(''.join(letters)))
			for letters in itertools.product(alphabet, repeat = num_letters)]
				
		# get only the syllables with the most counts, up to the fraction specified
		counts = [ (l,c) for l,c in counts if c>0 ]
		counts.sort(key = Language._get_count)
		n = int(fraction * len(counts))
		counts = counts[-n:]
		
		#get syllables from the tuples by "unzipping"
		syllables = list(zip(*counts)[0])
		return syllables

	@staticmethod
	def _count_combinations(syllables, sample):	
		combinations = []
		for prefix in syllables:
			combinations.append(Language._count_with_prefix(syllables, prefix, sample))
		
		starts = Language._count_with_prefix( syllables, ' ', sample)
		ends   = Language._count_with_postfix(syllables, ' ', sample)
		
		return (combinations, starts, ends)

	@staticmethod
	def _count_with_prefix(syllables, prefix, sample):
		combinations = []
		total = 0
		for (index, syl) in enumerate(syllables):
			count = sample.count(prefix + syl)
			if count != 0:				
				total += count
				combinations.append([index, total])
		return combinations

	@staticmethod
	def _count_with_postfix(syllables, postfix, sample):
		combinations = []
		total = 0
		for (index, syl) in enumerate(syllables):
			count = sample.count(syl + postfix)
			if count != 0:
				total += count
				combinations.append([index, total])
		return combinations

def mix_two_samples(samples_a,samples_b,sample_size=100):
	n_a = random.randint(0,sample_size)
	n_b = sample_size-n_a 
	sample = []
	for i in xrange(n_a):
		sample.append(random.choice(samples_a).lower().strip())
	for i in xrange(n_b):
		sample.append(random.choice(samples_b).lower().strip())
	return sample

def extract_and_mix_samples(lang_samples,sample_size=100):
	lang_a = random.choice(lang_samples.keys())
	lang_b = random.choice(lang_samples.keys())
	samples_a = lang_samples[lang_a]
	samples_b = lang_samples[lang_b]
	return mix_two_samples(samples_a,samples_b,sample_size)

