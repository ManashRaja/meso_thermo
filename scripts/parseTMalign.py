import re
import sys
from os import listdir
from os.path import isfile, join

def main():
	tmalign_dir = sys.argv[1]
	score_thres = float(sys.argv[2]) # 0.7
	out_filename = sys.argv[3]

	out_file = open(out_filename, 'w+')

	allfiles = [f for f in listdir(tmalign_dir) if isfile(join(tmalign_dir, f))]
	for file in allfiles:
		print "Running for filename ", file
		tmalign_filename = join(tmalign_dir, file)

		#open file
		tmalign_f = open(tmalign_filename,'r')
		
		pdb1_name = None
		pdb2_name = None
		score = None
		for line in tmalign_f:
			if "Name of Chain_1: " in line:
				parts = line.split('/')
				pdb1_name = parts[len(parts)-1].rstrip()
			elif "Name of Chain_2: " in line:
				parts = line.split('/')
				pdb2_name = parts[len(parts)-1].rstrip()
			elif "TM-score= " in line and score == None:
				digits = re.findall(r'\d+\.\d+', line)
				score = float(digits[0])
		print pdb1_name, pdb2_name, score
		if (score >= score_thres):
			out_text = pdb1_name + "," + pdb2_name + "," + str(score) + "\n"
			out_file.write(out_text)
		tmalign_f.close()
	out_file.close()
main()