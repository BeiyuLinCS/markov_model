############################################################
################## Markov Model Order Selection ############
############ Beiyu Lin @ Washing State University ##########
#################### beiyu.lin@wsu.edu #####################
############################################################
#!/usr/bin/python
from collections import defaultdict  
from mc_class import MarkovModel

# https://www.datasciencecentral.com/profiles/blogs/some-applications-of-markov-chain-in-python

input_sequence = ['abc', 'abc', 'acd', 'ecs', 'adf', 'dafae', 'dafae', 'dafae', 'adf', 'abc', 'dafae', 'dafae', 'dafae', 'adf', 'abc']

for i in range(0, 7):
	m = MarkovModel(input_sequence, i)
	prob_tran_matrix = m.prob_tran()
	# prob_tran_matrix: {(('adf', 'dafae', 'dafae'), 'dafae'): 0.5}
	



