import sys
from os import listdir
from os.path import isfile, join

def getTotalArea(residue_name):
	if("ALA" in residue_name):
		return 106.0;
	elif("CYS" in residue_name):
		return 135.0;
	elif("ASP" in residue_name):
		return 163.0;
	elif("GLU" in residue_name):
		return 194.0;
	elif("PHE" in residue_name):
		return 197.0;
	elif("GLY" in residue_name):
		return 84.0;
	elif("HIS" in residue_name):
		return 184.0;
	elif("ILE" in residue_name):
		return 169.0;
	elif("LYS" in residue_name):
		return 205.0;
	elif("LEU" in residue_name):
		return 164.0;
	elif("MET" in residue_name):
		return 188.0;
	elif("ASN" in residue_name):
		return 157.0;
	elif("PRO" in residue_name):
		return 136.0;
	elif("GLN" in residue_name):
		return 198.0;
	elif("ARG" in residue_name):
		return 248.0;
	elif("SER" in residue_name):
		return 130.0;
	elif("THR" in residue_name):
		return 142.0;
	elif("VAL" in residue_name):
		return 142.0;
	elif("TRP" in residue_name):
		return 227.0;
	elif("TYR" in residue_name):
		return 222.0;
	else:
		return -1.0;

def getSA(SA_ratio):
	SA = None
	if(SA_ratio <= 0.09):
		SA = "B"
	elif (SA_ratio > 0.09 and SA_ratio < 0.64):
		SA = "I"
	else:
		SA = "E"
	return SA

def main():
	pdb_dir = sys.argv[1]
	stride_dir = sys.argv[2]
	resp_dir = sys.argv[3]
	sep = ','

	allfiles = [f for f in listdir(pdb_dir) if isfile(join(pdb_dir, f))]
	for file in allfiles:
		print "Running for filename ", file
		pdb_filename = join(pdb_dir, file)
		stride_filename = join(stride_dir, file)
		out_filename = join(resp_dir, file)

		#open file
		pdb_f = open(pdb_filename,'r')
		o_f = open(out_filename, 'w+')

		avg_x = 0.0
		avg_y = 0.0
		avg_z = 0.0
		counter = 0
		prev_res_num = None
		prev_res_name = None
		prev_chain_id = None
		start = True

		#iterate through all lines
		for line in pdb_f:
			#check if line starts with atom
			if (line[0:4] == "ATOM"):
				residue_number = int(line[22:26])
				residue_name = line[17:20]
				chain_id = line[21:22]
				#if(chain_id == "A"):
				#	start = True
				if(not start):
					continue
				x = float(line[30:38])
				y = float(line[38:46])
				z = float(line[46:54])
				#print residue_number, residue_name, chain_id, x, y, z
				if(prev_res_num!=None and residue_number!=prev_res_num):
					#find avg and write to file
					avg_x = avg_x/counter
					avg_y = avg_y/counter
					avg_z = avg_z/counter
					out_string = (str(prev_res_num) + sep +
								  prev_res_name + sep +
								  prev_chain_id + sep +
								  str(avg_x) + sep +
								  str(avg_y) + sep +
								  str(avg_z) + "\n")
					o_f.write(out_string)
					#reset
					avg_x = 0.0
					avg_y = 0.0
					avg_z = 0.0
					counter = 0
				avg_x = avg_x + x
				avg_y = avg_y + y
				avg_z = avg_z + z
				counter = counter+1
				prev_res_num = residue_number
				prev_res_name = residue_name
				prev_chain_id = chain_id
		# Write the last residue
		avg_x = avg_x/counter
		avg_y = avg_y/counter
		avg_z = avg_z/counter
		out_string = (str(prev_res_num) + sep +
					  prev_res_name + sep +
					  prev_chain_id + sep +
					  str(avg_x) + sep +
					  str(avg_y) + sep +
					  str(avg_z) + "\n")
		o_f.write(out_string)
		pdb_f.close()
		o_f.close()
		
		# Now process the stride file
		stride_f = open(stride_filename,'r')
		o_f = open(out_filename, 'r')
		of_lines = o_f.readlines()
		o_f.close()
		o_f = open(out_filename, 'w+')

		#get first residue number
		parts = of_lines[0].split(sep)
		of_res_num = int(parts[0])
		counter = 0

		#iterate through all lines
		for line in stride_f:
			#check if line starts with ASG
			if (line[0:3] == "ASG"):
				residue_number = None
				try:
					residue_number = int(line[11:15])
				except:
					residue_number = int(line[11:14])
				residue_name = line[5:8]
				SS = line[24:25]
				SS_short = "N"
				if("H" in SS or "G" in SS or "I" in SS):
					SS_short = "H"
				elif("E" in SS):
					SS_short = "S"
				elif("b" in SS or "B" in SS or "T" in SS or "C" in SS):
					SS_short = "L"
				SA_ratio = float(line[64:69])/getTotalArea(residue_name)
				SA = getSA(SA_ratio)			
				if(residue_number == of_res_num):
					out_string = of_lines[counter][0:len(of_lines[counter])-1] + sep + SS_short + sep + SA + "\n"
					counter = counter + 1
					of_res_num = of_res_num + 1
					o_f.write(out_string)
		o_f.close()


main()
