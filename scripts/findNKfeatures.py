#python ../../scripts/findNKfeatures.py tstdKI_z_thermo_homo.txt tmeanV_z_thermo_homo.txt tmeanKI_z_thermo_homo.txt tstdKI_z_meso_homo.txt tmeanV_z_meso_homo.txt tmeanKI_z_meso_homo.txt 90 z_NKfeatures_homo.txt z_NKfeatures_homo_id.txt
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

def getTopNThermoIds(sorted_thermo_std_ki, thermo_v_ki, v_thres, n):
	n_ids = []
	counter = 0
	for key,value in sorted_thermo_std_ki:
		if(value > 0.0 and thermo_v_ki[key] >= v_thres):
			n_ids.append(key)
			counter = counter+1
		if(counter >= n):
			break
	return n_ids

def main():
	thermo_file_name = sys.argv[1]
	thermo_v_file_name = sys.argv[2]
	thermoKI_file_name = sys.argv[3]
	meso_file_name = sys.argv[4]
	meso_v_file_name = sys.argv[5]
	mesoKI_file_name = sys.argv[6]
	n = int(sys.argv[7])
	out_file_name = sys.argv[8]
	out_id_file_name = sys.argv[9]
	v_thres = 0.4

	thermo_file = open(thermo_file_name, 'r')
	thermo_v_file = open(thermo_v_file_name, 'r')
	thermoKI_file = open(thermoKI_file_name, 'r')
	meso_file = open(meso_file_name, 'r')
	meso_v_file = open(meso_v_file_name, 'r')
	out_file = open(out_file_name, 'w+')
	out_id_file = open(out_id_file_name, 'w+')
	mesoKI_file = open(mesoKI_file_name, 'r')

	meso_std_ki = stringLinesToDict(meso_file.readlines())
	meso_v_ki = stringLinesToDict(meso_v_file.readlines())
	mesoKI = stringLinesToDict(mesoKI_file.readlines())
	thermo_std_ki = stringLinesToDict(thermo_file.readlines())
	thermo_v_ki = stringLinesToDict(thermo_v_file.readlines())
	thermoKI = stringLinesToDict(thermoKI_file.readlines())

	sorted_meso_std_ki = sorted(meso_std_ki.iteritems(), key=lambda (k,v): (v,k))
	sorted_thermo_std_ki = sorted(thermo_std_ki.iteritems(), key=lambda (k,v): (v,k))

	n_ids = getTopNThermoIds(sorted_thermo_std_ki, thermo_v_ki, v_thres, n)
	k_ids = []
	for i in n_ids:
		print thermo_std_ki[i], meso_std_ki[i], i
		if(meso_std_ki[i] > 0.0 and meso_v_ki[i]>v_thres):
			k_ids.append(i)
			out_text = str(i) + "," + str(thermo_std_ki[i]) + "," + str(meso_std_ki[i]) + "," + str(thermoKI[i]) + "," + str(mesoKI[i]) + "\n";
			out_file.write(out_text)
			out_id_file.write(str(i)+"\n")

	print "K = ", len(k_ids)
	out_file.close()
	out_id_file.close()
	thermo_file.close()
	thermo_v_file.close()
	meso_file.close()
	meso_v_file.close()
main()