#python karlin_index.py ../data/meso_resp/ ../data/matrices/ _z_meso
import sys
import math
from os import listdir
from os.path import isfile, join

sep = ','
list_aa = ["ALA", "CYS", "ASP", "GLU", "PHE", "GLY", 
		   "HIS", "ILE", "LYS", "LEU", "MET", "ASN", 
		   "PRO", "GLN", "ARG", "SER", "THR", "VAL", "TRP", "TYR"]
list_ss = ["H", "S", "L"]
list_sa = ["B", "I", "E"]

def getDataMatrix(data_lines):
	m = []
	for line in data_lines:
		parts = line.split(sep)
		m_l = []
		m_l.append(int(parts[0])) #res_id
		m_l.append(parts[1]) #res_name
		m_l.append(parts[2]) #chain_id
		m_l.append(float(parts[3])) #x
		m_l.append(float(parts[4])) #y
		m_l.append(float(parts[5])) #z
		m_l.append(parts[6]) #ss
		m_l.append(parts[7][0]) #sa
		m.append(m_l)
	return m

def getNumResByName(residue_name, data_matrix):
	counter = 0
	for i in range(len(data_matrix)):
		if (residue_name in data_matrix[i][1]):
			counter = counter+1
	return counter

def getDistanceBRes(id1, id2, data_matrix):
	dist = math.sqrt((data_matrix[id2][3]-data_matrix[id1][3])**2 + 
				    (data_matrix[id2][4]-data_matrix[id1][4])**2 +
				    (data_matrix[id2][5]-data_matrix[id1][5])**2)
	return dist

def getResFeature(residue_name):
	aro_list = ["PHE", "TYR", "TRP", "HIS"]
	pos_list = ["LYS", "ARG"]
	neg_list = ["ASP", "GLU"]
	pol_list = ["SER", "THR", "LYS", "ASN", "GLN", "ALA", "GLY"]
	hyd_list = ["VAL", "LEU", "ILE", "MET", "PRO"]
	
	if residue_name in aro_list:
		return "ARO"
	elif residue_name in pos_list:
		return "POS"
	elif residue_name in neg_list:
		return "NEG"
	elif residue_name in pol_list:
		return "POL"
	elif residue_name in hyd_list:
		return "HYD"

def getFeatureFrequency(feature, data_matrix):
	counter = 0
	for i in range(len(data_matrix)):
		if( getResFeature(data_matrix[i][1])  == feature ):
			counter = counter +1
	frequency = float(counter)/len(data_matrix)
	return frequency

def getNumFeatureTotalInNeighbor(ci, T, feature, data_matrix):
	num_feature = 0
	num_total = 0
	for i in range(len(data_matrix)):
		if i==ci:
			continue
		if(getDistanceBRes(ci, i, data_matrix) < T):
			num_total = num_total+1
			#check is residue belong to feature
			if(getResFeature(data_matrix[i][1])  == feature):
				num_feature = num_feature+1
	return [num_feature, num_total]


def getKIByResType(residue_name, SS, SA, feature, frequency, T, data_matrix):
	numerator = 0.0
	denominator = 0.0
	for i in range(len(data_matrix)):
		#find residue by type
		if(residue_name in data_matrix[i][1] and 
		   SS == data_matrix[i][6] and
		   SA == data_matrix[i][7]):
			#in a radius T around it find num
			#of residues of particular feature
			[num_feature, num_total] = getNumFeatureTotalInNeighbor(i, T, feature, data_matrix)
			#print num_feature, num_total
			numerator = numerator+num_feature
			denominator = denominator+(num_total*frequency)
	return [numerator, denominator]

def getNumByResType(residue_name, SS, SA, data_matrix):
	counter = 0
	for i in range(len(data_matrix)):
		#find residue by type
		if(residue_name in data_matrix[i][1] and 
		   SS == data_matrix[i][6] and
		   SA == data_matrix[i][7]):
			counter = counter+1
	return counter

def getNDVmatrices(feature, frequency, T, data_matrix):
	N_matrix = []
	D_matrix = []
	V_matrix = []
	for aa in list_aa:
		N_matrix_row = []
		D_matrix_row = []
		V_matrix_row = []
		for ss in list_ss:
			for sa in list_sa:
				[N, D] = getKIByResType(aa, ss, sa, feature, frequency, T, data_matrix)
				N_matrix_row.append(N)
				D_matrix_row.append(D)
				V = 0
				if(N>0.0 and D>0.0):
					V = 1
				V_matrix_row.append(V)
		N_matrix.append(N_matrix_row)
		D_matrix.append(D_matrix_row)
		V_matrix.append(V_matrix_row)
	return [N_matrix, D_matrix, V_matrix]

def writeMatrixToFile(matrix, filename):
	f = open(filename, 'w+')
	for i in range(len(matrix)):
		output_string = ""
		for j in range(len(matrix[i])):
			output_string = output_string + str(round(matrix[i][j],3)) + ","
		output_string = output_string + "\n"
		f.write(output_string)
	f.close()

def addMatrixToDest(src, dest):
	for i in range(len(dest)):
		for j in range(len(dest[i])):
			dest[i][j] = dest[i][j] + src[i][j]
	return dest

def SqDiffMatrix(src, mean):
	dest = src
	for i in range(len(src)):
		for j in range(len(src[i])):
			dest[i][j] =(src[i][j] - mean[i][j]) * (src[i][j] - mean[i][j])
	return dest

def sqruareRootMatrix(src):
	dest = src
	for i in range(len(src)):
		for j in range(len(src[i])):
			dest[i][j] = math.sqrt(src[i][j])
	return dest

def scalarMatrixMult(mat, x):
	for i in range(len(mat)):
		for j in range(len(mat[i])):
			mat[i][j] = mat[i][j]*x
	return mat

def computeKIMatrix(N,D):
	KI = []
	for i in range(len(N)):
		KI_row = []
		for j in range(len(N[i])):
			if(D[i][j] == 0.0):
				KI_row.append(0.0)
			else:
				KI_row.append(N[i][j]/D[i][j])
		KI.append(KI_row)
	return KI

def getFrequencyMatrix(data_matrix):
	freq_m = []
	for aa in list_aa:
		freq_m_row = []
		for ss in list_ss:
			for sa in list_sa:
				num = getNumByResType(aa, ss, sa, data_matrix)
				freq_m_row.append(num)
		freq_m.append(freq_m_row)
	return freq_m

def appendMatrixColumns(src, dest):
	# Loop through all the rows
	counter = 0
	for row in dest:
	  src_row = src[counter]
	  for elems in src_row:
	  	row.append(elems)
	  counter = counter+1


def main():
	dir_name = sys.argv[1]
	matrices_dir_name = sys.argv[2]
	modifier = sys.argv[3]
	T = 5.0

	run_for_features = ["ARO","POS","NEG","POL","HYD"]
	tmeanN = None
	tmeanD = None
	tmeanF = None
	tmeanV = None
	tKIN = None
	tKID = None
	tstdN = None
	tstdD = None
	tstdF = None
	feature_counter = 0
	for feature in run_for_features:
		meanN = None
		meanD = None
		meanF = None
		meanV = None
		KIN = None
		NID = None
		counter = 0
		allfiles = [f for f in listdir(dir_name) if isfile(join(dir_name, f))]
		for file in allfiles:
			#open file
			filename = join(dir_name, file)
			print "Running for file ", filename
			resp_f = open(filename,'r')
			resp_data_lines = resp_f.readlines()
			data_matrix = getDataMatrix(resp_data_lines)
			hydro_f = getFeatureFrequency(feature, data_matrix)
			[N,D,V] = getNDVmatrices(feature, hydro_f, T, data_matrix)
			F = getFrequencyMatrix(data_matrix)
			if(counter == 0):
				meanN = N
				meanD = D
				meanF = F
				meanV = V
			else:
				meanN = addMatrixToDest(N, meanN)
				meanD = addMatrixToDest(D, meanD)
				meanF = addMatrixToDest(F, meanF)
				meanV = addMatrixToDest(V, meanV)
			counter = counter+1
		KIN = meanN[:]
		KID = meanD[:]
		meanD = scalarMatrixMult(meanD, 1.0/counter)
		meanN = scalarMatrixMult(meanN, 1.0/counter)
		meanF = scalarMatrixMult(meanF, 1.0/counter)
		meanV = scalarMatrixMult(meanV, 1.0/counter)
		if(feature_counter == 0):
			tmeanN = meanN[:]
			tmeanD = meanD[:]
			tmeanF = meanF[:]
			tmeanV = meanV[:]
			tKIN = KIN[:]
			tKID = KID[:]
		else:
			appendMatrixColumns(meanN, tmeanN)
			appendMatrixColumns(meanD, tmeanD)
			appendMatrixColumns(meanF, tmeanF)
			appendMatrixColumns(meanV, tmeanV)
			appendMatrixColumns(KIN, tKIN)
			appendMatrixColumns(KID, tKID)

		## Compute Variance and Standard Deviation
		stdN = None
		stdD = None
		stdF = None
		counter = 0
		allfiles = [f for f in listdir(dir_name) if isfile(join(dir_name, f))]
		for file in allfiles:
			#open file
			filename = join(dir_name, file)
			print "Running for file ", filename
			resp_f = open(filename,'r')
			resp_data_lines = resp_f.readlines()
			data_matrix = getDataMatrix(resp_data_lines)
			hydro_f = getFeatureFrequency(feature, data_matrix)
			[N,D,V] = getNDVmatrices(feature, hydro_f, T, data_matrix)
			F = getFrequencyMatrix(data_matrix)
			sqdiffN = SqDiffMatrix(N, meanN)
			sqdiffD = SqDiffMatrix(D, meanD)
			sqdiffF = SqDiffMatrix(F, meanF)
			if(counter == 0):
				stdN = sqdiffN
				stdD = sqdiffD
				stdF = sqdiffF
			else:
				stdN = addMatrixToDest(sqdiffN, stdN)
				stdD = addMatrixToDest(sqdiffD, stdD)
				stdF = addMatrixToDest(sqdiffF, stdF)
			counter = counter+1
		stdD = scalarMatrixMult(stdD, 1.0/counter)
		stdN = scalarMatrixMult(stdN, 1.0/counter)
		stdF = scalarMatrixMult(stdF, 1.0/counter)
		stdD = sqruareRootMatrix(stdD)
		stdF = sqruareRootMatrix(stdF)
		stdN = sqruareRootMatrix(stdN)
		if(feature_counter == 0):
			tstdN = stdN[:]
			tstdD = stdD[:]
			tstdF = stdF[:]
		else:
			appendMatrixColumns(stdN, tstdN)
			appendMatrixColumns(stdD, tstdD)
			appendMatrixColumns(stdF, tstdF)
		feature_counter = feature_counter+1

	tstdKI = computeKIMatrix(tstdN, tstdD)
	tmeanKI = computeKIMatrix(tmeanN, tmeanD)
	tKI = computeKIMatrix(tKIN, tKID)
	writeMatrixToFile(tstdN, join(matrices_dir_name, "tstdN" + modifier + ".txt"))
	writeMatrixToFile(tstdD, join(matrices_dir_name, "tstdD" + modifier + ".txt"))
	writeMatrixToFile(tstdKI, join(matrices_dir_name, "tstdKI" + modifier + ".txt"))
	writeMatrixToFile(tmeanN, join(matrices_dir_name, "tmeanN" + modifier + ".txt"))
	writeMatrixToFile(tmeanD, join(matrices_dir_name, "tmeanD" + modifier + ".txt"))
	writeMatrixToFile(tmeanKI, join(matrices_dir_name, "tmeanKI" + modifier + ".txt"))
	writeMatrixToFile(tmeanV, join(matrices_dir_name, "tmeanV" + modifier + ".txt"))
	writeMatrixToFile(tKI, join(matrices_dir_name, "tKI" + modifier + ".txt"))

main()