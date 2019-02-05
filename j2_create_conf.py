#!/usr/bin/env python

import re
import pandas as pd
import sys
import numpy
import pyexcel as pe
from jinja2 import Environment, FileSystemLoader
import os

def file_check(input_file,template):
	template = bool(re.search(r'.j2',template))
	input_file = bool(re.search(r'(?:.xls|.xlsx)',input_file))
	if template == False:
		print('\nHalted - template file needs extension of .j2')
		raise SystemExit(0)
	if input_file == False:
		print('\nHalted - excel file needs either a .xls or .xlsx file extension')
		raise SystemExit(0)
	print('all file extensions are acceptable, moving forward')

def input(input_file):
	xls = pd.ExcelFile('{}'.format(input_file))
	df_var = pd.read_excel(xls, 'var')
	df_var.set_index('var_name', inplace=True)
	duplicated = df_var[df_var.index.duplicated(keep=False)]
	duplicated = str(duplicated)
	if 'Empty DataFrame' not in duplicated:
		print ('duplicated var IDs found in the pandas index, must be unique, stopping..')
		exit()
	df_var_index_list = df_var.index.tolist()
	df_var_index_list = [str(r) for r in df_var_index_list]
	values = {}
	for i in df_var_index_list:
		v = df_var.loc[i,'var_values']
		v = str(v)
		values[i] = v
	return values,df_var_index_list

def check_vars(df_var_index_list,template):
	f = open('{}'.format(template),'r')
	file = f.readlines()
	print(file)
	file = str(file)
	vars_from_template =  re.findall(r"{{([a-zA-Z0-9_]+)}}", file)
	extra_var_in_template = [i for i in vars_from_template if i not in df_var_index_list]
	extra_var_in_excel = [i for i in df_var_index_list if i not in vars_from_template]
	if len(extra_var_in_template) > 0:
		print('{} was found in j2 template but not in excel sheet, they must align, stopping...'.format(extra_var_in_template))
		exit()
	if len(extra_var_in_excel) > 0:
		print('{} was found in excel sheet but not j2 template, they must align, stopping...'.format(extra_var_in_excel))
		exit()
	print('All checks are complete')

def create_config(template, values, file_output):
	file_loader = FileSystemLoader('.')
	env = Environment(loader=file_loader)
	template = env.get_template(template)
	j2_write = template.render(values)
	os.system('rm -f {}'.format(file_output))
	with open('{}'.format(file_output), 'a+') as config:
		config.write(j2_write)

def main():
	if '-i' not in sys.argv and '-o' not in sys.argv and '-t' not in sys.argv:
		print("\nHalted - Please provide both input and output file names using - i (for input) -o (for output) and -t (for j2 template)\n\n")
		raise SystemExit(0)
	if '-i' not in sys.argv:
		print("\nHalted - Please provide input file name using -i\n\n")
		raise SystemExit(0)
	if '-o' not in sys.argv:
		print("\nHalted - Please provide output file name using -o\n\n")
		raise SystemExit(0)
	if '-t' not in sys.argv:
		print("\nHalted - Please provide template file name using -t\n\n")
		raise SystemExit(0)
	for index,argument in enumerate(sys.argv):
		if argument == '-o':
			if (index+1) < len(sys.argv):
				file_output = sys.argv[index+1]
				print(file_output)
			else:
			# Need a valid output file after the -o argument
				print("\nHalted - No Output file provided\n\n")
				raise SystemExit(0)
		if argument == '-i':
			if (index+1) < len(sys.argv):
				input_file = sys.argv[index+1]
				print(input_file)
			else:
			# Need a valid input file after the -i argument
				print("\nHalted - No Input file provided\n\n")
				raise SystemExit(0)
		if argument == '-t':
			if (index+1) < len(sys.argv):
				template = sys.argv[index+1]
				print(template)
			else:
			# Need a valid input file after the -t argument
				print("\nHalted - No template file provided\n\n")
				raise SystemExit(0)
		if argument == '-s':
			if (index) < len(sys.argv):
				send = True
	file_check(input_file,template)
	values,df_var_index_list = input(input_file)
	check_vars(df_var_index_list,template)
	create_config(template,values,file_output)

if __name__ == '__main__':
  main()

#for testing
#input_file = 'j2_test.xlsx'
#file_output = 'output.txt'
#template = 'template.j2'

