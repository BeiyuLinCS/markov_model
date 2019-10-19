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
import sys
from mc_class import MarkovModel
from gen_mc_transition import GenMarkovTransitionProb

# https://www.datasciencecentral.com/profiles/blogs/some-applications-of-markov-chain-in-python
# input_sequence = ['abc', 'abc', 'acd', 'ecs', 'adf', 'dafae', 'dafae', 'dafae', 'adf', 'abc', 'dafae', 'dafae', 'dafae', 'adf', 'abc']

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

def percentage_order_category(selected_order, order_i, percentage_order):
	for measure in selected_order.keys():
		# print("measure", measure)
		if selected_order[measure] < order_i:
			percentage_order[measure]["under_estimate"] =  percentage_order.get(measure, 0).get("under_estimate", 0) + 1
		elif selected_order[measure] == order_i:
			percentage_order[measure]["equal"] =  percentage_order.get(measure, 0).get("equal", 0) + 1
		else: 
			percentage_order[measure]["over_estimate"] =  percentage_order.get(measure, 0).get("over_estimate", 0) + 1
	return percentage_order

def calculate_measure_values(readin_data, order_i, percentage_order):
	# header = ["order", "aic", "bic", "hqic", "edc", "new1", "new2", "new3"]
	measure_names = ["aic", "bic", "hqic", "edc", "new1", "new2", "new3"]
	mini_meausre = defaultdict(float)
	selected_order = defaultdict(float)
	for i in range(0, 7):
		m = MarkovModel(readin_data, i)
		for measure in measure_names:
			measure_value = round(m.measure_values(measure), 2)
			if measure not in mini_meausre.keys() or measure_value < mini_meausre[measure]:
				mini_meausre[measure] =	measure_value
				selected_order[measure] = i 
	percentage_order = percentage_order_category(selected_order, order_i, percentage_order)
	return percentage_order

def calculate_measure_values_sh(readin_data, fout_file_path):
	header = ["order", "aic", "bic", "hqic", "edc", "new1", "new2", "new3"]
	order_measure = defaultdict(float)

	for i in range(0, 7):
		m = MarkovModel(readin_data, i)
		mini_meausre = defaultdict(float)
		for measure in measure_names:
			measure_value = round(m.measure_values(measure), 2)
			if measure not in mini_meausre.keys():
				mini_meausre[measure] =	measure_value
			elif measure_value < mini_meausre[measure]:
					mini_meausre[measure] = measure_value
		order_measure[i] = mini_meausre
	write_into_csv(order_measure, fout_file_path)
	
	# with open(fout_file_path, "wb") as f:
	#     w = csv.DictWriter(f, header)
	#     w.writeheader()
	#     for order in order_measure:
	#         w.writerow({h: order_measure[order].get(h) or order for h in header})

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
		calculate_measure_values_sh(flatten, fout_file_path)

def calculate_percentage(percentage_order):
	for measure in percentage_order.keys():
		total_count = 0 
		for k in percentage_order[measure].keys():
			total_count += percentage_order[measure][k]
		for k in percentage_order[measure].keys():
			percentage_order[measure][k] = round(100*percentage_order[measure][k]/float(total_count), 2)
	return percentage_order

def write_into_csv(percentage_order, fout_file_path):	
	header = ["measures", "under_estimate", "equal", "over_estimate"]
	measure_names = ["aic", "bic", "hqic", "edc", "new1", "new2", "new3"]	
	with open(fout_file_path, "wb") as f:
	    w = csv.DictWriter(f, header)
	    w.writeheader()
	    for measure in measure_names:
	    	temp_row = {}
	    	for h in header: 
	    		if h not in percentage_order[measure].keys():
	    			temp_row[h] = measure
	    		else:
	    			temp_row[h] = percentage_order[measure].get(h)
	    	w.writerow(temp_row)

def init_percent_order():
	percentage_order = {"aic":{"under_estimate": 0, "equal": 0, "over_estimate": 0}, 
			"bic":{"under_estimate": 0, "equal": 0, "over_estimate": 0}, 
			"hqic":{"under_estimate": 0, "equal": 0, "over_estimate": 0}, 
			"edc":{"under_estimate": 0, "equal": 0, "over_estimate": 0}, 
			"new1":{"under_estimate": 0, "equal": 0, "over_estimate": 0}, 
			"new2":{"under_estimate": 0, "equal": 0, "over_estimate": 0}, 
			"new3":{"under_estimate": 0, "equal": 0, "over_estimate": 0	}}
	return percentage_order

def syn2_paper(root_dir, states_temp, order_i, start_sample_size, end_sample_size):
	percentage_order = init_percent_order()
	for s in range(start_sample_size, end_sample_size, 500):
		for h  in range(1, 1000):
			print("generate sampel size %s with iteration %s"%(s-5000, h))
			gen_m = GenMarkovTransitionProb(states_temp, order_i)
			gen_sequence = gen_m.gen(tuple(states_temp[0:order_i]), s)
			percentage_order = calculate_measure_values(gen_sequence[5000:], order_i, percentage_order)
		fout_file_path = create_output_file_path(root_dir, "syn_data/syn2_order_"+str(order_i) + "/"  , (s-5000))
		percentage_order = calculate_percentage(percentage_order)
		write_into_csv(percentage_order, fout_file_path)

if __name__ == '__main__':
	
	syn1 = False
	syn2 = True
	syn3 = False
	sample_size_syn1 = 10000
	# root_dir = "/Users/BeiyuLin/Desktop/five_datasets/"
	root_dir = "./"
	order_i = int(sys.argv[1])
	start_sample_size = int(sys.argv[2])
	end_sample_size = int(sys.argv[3])

	# calculate the order of each subgroup from smart home datasets
	if not syn1 and not syn2 and not syn3:
		print("process smart home data")
		# directories = ["cluster_no_start_end", "cluster_start_end", "location_data", "labelled_after_cpd"]
		directories = ["location_data"]
		for directory in directories:
			smart_home_datasets(root_dir, directory)
		print("finished smart home data")

	elif syn2:
		print("generate syn2 data")
		# based on randomly generated transition matrix.
		# http://www.iaeng.org/publication/WCECS2014/WCECS2014_pp899-901.pdf
		# each case is the order of the synthetic data
		states_temp = ['a','b','c','d','e','f','g','h','u']
		# generate 1000 random transition matrix 
		syn2_paper(root_dir, states_temp, order_i, start_sample_size, end_sample_size)
		print("finished syn2")

	else:
		print("generate syn1 or syn3 data")
		# based on binomial distributions.
		# https://arxiv.org/pdf/0910.0264.pdf
