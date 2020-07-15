#!/usr/local/bin/python3

import json
import sys
import getopt
import os

def main(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print ('test.py -i <inputfile> -o <outputfile>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('test.py -i <inputfile> -o <outputfile>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   if len(outputfile) == 0:
      outputfile = inputfile
   print ('Input file is ', inputfile)
   print ('Output file is ', outputfile)

   try:
      with open(inputfile, 'r') as handle:
         parsed = json.load(handle)
   except IOError:
      print ("Could not read file: ", inputfile)

   try:
      with open(outputfile, "w") as json_file:
         json.dump(parsed, json_file, indent=2)
         json_file.write("\n")  # Add newline cause Py JSON does not
   except IOError:
      print ("Could not write file: ", outputfile)

if __name__ == "__main__":
   main(sys.argv[1:])

