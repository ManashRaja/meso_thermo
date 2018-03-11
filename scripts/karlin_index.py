import sys
import math

sep = " "

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


def getKIbyResType(residue_name, SS, SA, feature, frequency, T, data_matrix):
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
			print num_feature, num_total*frequency

def main():
	resp_filename = sys.argv[1]

	#open file
	resp_f = open(resp_filename,'r')
	resp_data_lines = resp_f.readlines()
	data_matrix = getDataMatrix(resp_data_lines)
	#print getNumResByName("ALA", data_matrix)
	hydro_f = getFeatureFrequency("HYDRO", data_matrix)
	getKIbyResType("ARG", "L", "I", "HYDRO", hydro_f, 5.0, data_matrix)

main()