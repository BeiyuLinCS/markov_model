import numpy as np 
from collections import defaultdict  

class MarkovModel:      

	def __init__(self, text, k):          
		'''create a Markov model of order k from given activities         
		Assume that text has length at least k.'''
		self.k = k
		self.tran = defaultdict(float)
		self.alph = list(set(list(text)))
		self.kgrams = defaultdict(int)
		n = len(text)
		text += text[:k]
		for i in range(n):
			self.tran[tuple(text[i:i+k]),text[i+k]] += 1
			self.kgrams[tuple(text[i:i+k])] += 1    

	def order(self):
		# order k of Markov model
		return self.k

	def freq(self, kgram):
		# number of occurrences of kgram in text
		assert len(kgram) == self.k    
		# (check if kgram is of length k)
		return self.kgrams[kgram]

	def freq2(self, kgram, c):
		# number of times that character c follows kgram
		assert len(kgram) == self.k
		# (check if kgram is of length k)
		return self.tran[kgram,c]

	def prob_tran(self):
		# transition matrix with probability
		prob_tran_matrix = defaultdict(float)
		for key, value in self.tran.items():
			# key[0]: k-successive activities
			# key[1]: k+1th activity
			# value: the count from k-successive activities to the k+1th activity
			prob_tran_matrix[key] = value/self.freq(key[0])
		return prob_tran_matrix


