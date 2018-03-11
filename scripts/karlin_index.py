import sys

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

def main():
	resp_filename = sys.argv[1]

	#open file
	resp_f = open(resp_filename,'r')
	resp_data_lines = resp_f.readlines()
	data_matrix = getDataMatrix(resp_data_lines)
	print getNumResByName("ALA", data_matrix)
	#print data_matrix

main()