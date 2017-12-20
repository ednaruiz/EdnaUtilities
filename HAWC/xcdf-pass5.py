import numpy as np
import os
import sys
import argparse 



parser = argparse.ArgumentParser("Process a given list of xcdf file to apply pass 5 cuts")

parser.add_argument('--files', help="list of files to process", dest = 'files')
parser.add_argument('--cuts', help="cuts to apply",dest = 'cuts')

args = parser.parse_args()


