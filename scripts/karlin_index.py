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
	hydro_list = ["GLY", "ALA", "VAL", "LEU", "ILE", "PRO", "PHE", "MET", "TRY"]
	if residue_name in hydro_list:
		return "HYDRO"

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

def getNDmatrices(feature, frequency, T, data_matrix):
	N_matrix = []
	D_matrix = []
	for aa in list_aa:
		N_matrix_row = []
		D_matrix_row = []
		for ss in list_ss:
			for sa in list_sa:
				[N, D] = getKIByResType(aa, ss, sa, feature, frequency, T, data_matrix)
				N_matrix_row.append(N)
				D_matrix_row.append(D)
		N_matrix.append(N_matrix_row)
		D_matrix.append(D_matrix_row)
	return [N_matrix, D_matrix]

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
				KI_row.append(-1.0)
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


def main():
	dir_name = sys.argv[1]
	matrices_dir_name = sys.argv[2]

	feature = "HYDRO"
	T = 5.0

	mainN = None
	mainD = None
	mainF = None
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
		[N,D] = getNDmatrices(feature, hydro_f, T, data_matrix)
		F = getFrequencyMatrix(data_matrix)
		if(counter == 0):
			mainN = N
			mainD = D
			mainF = F
		else:
			mainN = addMatrixToDest(N, mainN)
			mainD = addMatrixToDest(D, mainD)
			mainF = addMatrixToDest(F, mainF)
		counter = counter+1
	mainKI = computeKIMatrix(mainN, mainD)
	mainD = scalarMatrixMult(mainD, 1.0/counter)
	mainN = scalarMatrixMult(mainN, 1.0/counter)
	mainF = scalarMatrixMult(mainF, 1.0/counter)

	writeMatrixToFile(mainN, join(matrices_dir_name, "N.txt"))
	writeMatrixToFile(mainD, join(matrices_dir_name, "D.txt"))
	writeMatrixToFile(mainKI, join(matrices_dir_name, "KI.txt"))
	writeMatrixToFile(mainF, join(matrices_dir_name, "M1.txt"))

main()