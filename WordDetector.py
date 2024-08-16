#########################################################################
# This Auxilary script compares the file contents and gives us the words #
#  that are different from each other.                                   #
#                                                                        #
# Author: Mahmut Ay < mahmtayy@yahoo.com                                 #             
#   "Peace at home, Peace in the world" M.K.Ataturk                      #       
##########################################################################

import sys

def read_words(file_path):
    with open(file_path, 'r') as file:
        words = set(file.read().splitlines())
    return words

if len(sys.argv) != 3:
    print(" Usage: python WordDetector.py File1.txt File2.txt")
    sys.exit(1)

file1_path = sys.argv[1]
file2_path = sys.argv[2]

file1_words = read_words(file1_path)
file2_words = read_words(file2_path)

# Sadece dosya1'de olan kelimeler / words that are stored ony File1
unique_to_file1 = file1_words - file2_words

# Sadece dosya2'de olan kelimeler / words that are stored ony File2
unique_to_file2 = file2_words - file1_words

# Sonuçları yazdır //Print Results
print(sys.argv[1]+"'Words in File1 that are not in File2:")
print('\n'.join(unique_to_file1))
print("/n"+"###########################################################")
print("\n"+sys.argv[2]+"   "+"Words in File2 that are not in File1:")
print('\n'.join(unique_to_file2))
