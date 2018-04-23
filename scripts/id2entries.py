#python id2entries.py ../data/matrices/z_NKfeatures_id.txt ../data/matrices/tmeanKI_z_thermo_homo.txt test.txt
import sys
from os import listdir
from os.path import isfile, join

def stringLinesToMatrix(lines):
	mat = []
	for line in lines:
		this_row = []
		parts = line.split(',')
		for i in range(45):
			this_row.append(float(parts[i]))
		mat.append(this_row)
	return mat

def stringLinesToDict(lines):
	this_dict = {}
	counter = 0
	for line in lines:
		parts = line.split(',')
		for i in range(45):
			this_dict[counter] = float(parts[i])
			counter = counter+1
	return this_dict

def main():
	id_file_name = sys.argv[1]
	entry_file_name = sys.argv[2]
	out_file_name = sys.argv[3]

	id_file = open(id_file_name, 'r')
	entry_file = open(entry_file_name, 'r')
	out_file = open(out_file_name, 'w+')

	entry_dict = stringLinesToDict(entry_file.readlines())

	for i in id_file:
		print entry_dict[int(i)]
		out_file.write(str(entry_dict[int(i)]) + "\n")
	out_file.close()
	entry_file.close()
main()