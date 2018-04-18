import re
import sys
from os import listdir
from shutil import copyfile
from os.path import isfile, join

def main():
	tmalign_pair_file_name = sys.argv[1]
	file_no = int(sys.argv[2]) # 0 or 1
	src_directory = sys.argv[3]
	dest_directory = sys.argv[4]

	tmalign_pair_file = open(tmalign_pair_file_name, 'r')

	for line in tmalign_pair_file:
		parts = line.split(',')
		target_file_name = parts[file_no]
		src_file_path = join(src_directory, target_file_name)
		dest_file_path = join(dest_directory, target_file_name)
		print "Copying file ", src_file_path, " to ", dest_file_path
		copyfile(src_file_path, dest_file_path)


main()