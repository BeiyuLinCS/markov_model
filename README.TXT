This package is to select the order of Makrov models for both smart home dataset and synthetic data. 
The orders of Markov models ranges from 0 to 6th. 
The measures to select orders are AIC, BIC, EDC, and HQIC. 

The mc_class.py has the class MarkovModel with below properties. 
m.alph is a list of unique activities. 
print("m.alph",  m.alph)

m.tran is a dictionary that shows the transtion matrix (with count not probability)
#e.g.: {(('adf', 'dafae', 'dafae'), 'dafae'): 1.0}
print("m.tran",  m.tran, len(m.tran))

m.kgrams is a dictionary that shows the count of each k successive activities
#e.g.: {('abc', 'abc', 'abc'): 1}
print("m.kgrams",  m.kgrams)

m.freq shows the count of each k successive activities: 
#e.g.: ('abc', 'abc', 'abc'): 1
#call from m.kgrams
print("m.freq", m.freq(('dafae', 'adf', 'abc')))

m.freq2(('dafae', 'adf', 'abc'), 'abc') shows the count of the transition to 'abc'
#call from m.tran
print("m.freq2", m.freq2(('dafae', 'adf', 'abc'), 'abc'))