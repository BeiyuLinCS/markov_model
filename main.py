############################################################
################## Markov Model Order Selection ############
############ Beiyu Lin @ Washing State University ##########
#################### beiyu.lin@wsu.edu #####################
############################################################
#!/usr/bin/python
from collections import defaultdict  
import itertools
import csv
import itertools
import pandas as pd
import os
import glob
import re
import numpy
from mc_class import MarkovModel
from gen_mc_transition import GenMarkovTransitionProb
from gen_syn_mc import GenMarkovChainSample

def make_dir(path):
	try:
		os.stat(path)
	except:
		os.makedirs(path)

def create_output_file_path(root_dir, dir_name, sample_size):
	output_dir = root_dir + "measure_results/"+ dir_name + "/"
	make_dir(output_dir)
	fout_file_path = output_dir + "/syn_" + str(sample_size) + ".csv"
	return fout_file_path

def gen_syn1(sample_size):
	## generate 9 states for 9 transition matrix for MC from 0th order - 6th order. 
	data = numpy.random.random(sample_size)
	bins = numpy.linspace(0, 1, 10) # digitized 1 - 9
	digitized = numpy.digitize(data, bins)
	bin_means = [data[digitized == i].mean() for i in range(1, len(bins))]
	# print(data)
	res = [str(x) for x in digitized]
	return res


def calculate_measure_values(readin_data, fout_file_path):
	header = ["order", "aic", "bic", "hqic", "edc", "new1", "new2", "new3"]
	order_measure = defaultdict(float)

	for i in range(0, 7):
		m = MarkovModel(readin_data, i)
		mini_meausre = defaultdict(float)
		for measure in measure_names:
			measure_value = round(m.measure_values(measure), 2)
			if measure not in mini_meausre.keys():
				mini_meausre[measure] =	measure_value
			else: 
				if measure_value < mini_meausre[measure]:
					mini_meausre[measure] = measure_value
		order_measure[i] = mini_meausre
	
	with open(fout_file_path, "wb") as f:
	    w = csv.DictWriter(f, header)
	    w.writeheader()
	    for order in order_measure:
	        w.writerow({h: order_measure[order].get(h) or order for h in header})

def smart_home_datasets(root_dir, directory):
	finput_dir = root_dir + directory + "/"
	output_dir = root_dir + "measure_results/"+ directory + "/"
	make_dir(output_dir)
	
	for file in glob.glob(os.path.join(finput_dir, '*.txt')):
		# cluster_no_start_end: ' ', 5; "cluster_0"; location: ' ', 2; labelled: '\t';
		df = pd.read_csv(file, sep = " ", usecols=(2,)) 
		df = df.values.tolist() #a list of list [["cluster_0"], ]
		flatten = list(itertools.chain(*df))
		fin_file_name = re.split(r'\/', file)
		print(directory, fin_file_name[-1])
		fout_file_path = output_dir + "/" + fin_file_name[-1] + ".csv"
		calculate_measure_values(flatten, fout_file_path)

def syn1_cook(root_dir, input_sequence):
	for i in range(1, 7):
		for s in range(15000, 85000, 10000):

			fout_file_path = create_output_file_path(root_dir, "syn1_order_" + str(i), s)
			m = MarkovModel(input_sequence, i)
			gen_sequence = m.gen(tuple(input_sequence[0:i]), s)
			calculate_measure_values(gen_sequence[5000:], fout_file_path)
			print("Calculated measure values for syn1 with order %ssample size %s"%i%s)


def syn2_paper(root_dir, states_temp):	
	for i in range(1, 7):
		gen_m = GenMarkovTransitionProb(states_temp, i)
		for s in range(5500, 8500, 1000):
			gen_sequence = gen_m.gen(tuple(states_temp[0:i]), s)
			fout_file_path = create_output_file_path(root_dir, "syn2_order_"+str(i), s)
			calculate_measure_values(gen_sequence[5000:], fout_file_path)
			print("Calculated measure values for syn2 with order %ssample size %s"%i%s)


if __name__ == '__main__':

	measure_names = ["aic", "bic", "hqic", "edc", "new1", "new2", "new3"]
	syn1 = False
	syn2 = True
	syn3 = False
	sample_size_syn1 = 10000
	root_dir = "/Users/BeiyuLin/Desktop/five_datasets/"

	# calculate the order of each subgroup from smart home datasets
	if not syn1 and not syn2 and not syn3:
		print("process smart home data")
		# directories = ["cluster_no_start_end", "cluster_start_end", "location_data", "labelled_after_cpd"]
		directories = ["location_data"]
		for directory in directories:
			smart_home_datasets(root_dir, directory)
		print("finished smart home data")

	elif syn1:
		print("generate syn1 data")
		input_sequence = gen_syn1(sample_size_syn1)
		syn1_cook(root_dir, input_sequence)
		print("finished syn1")

	elif syn2:
		print("generate syn2 data")
		# based on randomly generated transition matrix.
		# http://www.iaeng.org/publication/WCECS2014/WCECS2014_pp899-901.pdf
		# each case is the order of the synthetic data
		states_temp = ['a','b','c','d','e','f','g','h','u']
		syn2_paper(root_dir, states_temp)
		print("finished syn2")

	else:
		print("generate syn3 data")
		# based on binomial distributions.
		# https://arxiv.org/pdf/0910.0264.pdf



			





