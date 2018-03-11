import sys
from os import listdir
from os.path import isfile, join

def main():
	pair_dir_name = sys.argv[1]
	thermo_dir_name = sys.argv[2]
	meso_dir_name = sys.argv[3]

	allfiles = [f for f in listdir(pair_dir_name) if isfile(join(pair_dir_name, f))]
	counter = 0
	for file in allfiles:
		isMeso = False
		filename = join(pair_dir_name, file)
		print "Running for file ", filename
		pair_f = open(filename,'r')
		parts = file.split('.')
		thermo_pdb_filename = join(thermo_dir_name, str(counter) + "_" + parts[1]+".pdb")
		meso_pdb_filename = join(meso_dir_name, str(counter) + "_" + parts[2]+".pdb")
		t_f = open(thermo_pdb_filename, 'w+')
		m_f = open(meso_pdb_filename, 'w+')

		for line in pair_f:
			if(line[0:4] == "ATOM"):
				if(isMeso):
					m_f.write(line)
				else:
					t_f.write(line)
			elif("TER" in line):
				isMeso = True
		t_f.close()
		m_f.close()
		pair_f.close()
		counter = counter+1
		

main()
