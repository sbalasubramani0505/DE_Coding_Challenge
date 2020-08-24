#!/usr/bin/env python
# ----------------------------------------------------------------------------
# Author: Srilekha Balasubramani
# ----------------------------------------------------------------------------

import os
import csv
from functools import reduce
import time
import re

fileIndex = {}
WordMapDict = {}
uniq_ident = 0

def index_one_file(termlist,filename,fileIndex,uniq_ident):
	"""
	Split a text in to words. Builds word to id mapping 
	Builds document id mapping to word id
	"""
	filename_cnv = int(filename)
	for word in termlist:
		if word not in WordMapDict.keys():
			WordMapDict[word] = uniq_ident
			uniq_ident +=1

	for word in termlist:
		word_id = WordMapDict[word]
		if word_id not in fileIndex.keys():
			fileIndex[word_id]=[filename_cnv]
		else:
			if filename_cnv not in fileIndex[word_id]:
				fileIndex[word_id].append(filename_cnv)	
	return (fileIndex,uniq_ident)

def make_indices(termlists,fileIndex,uniq_ident):
	""" 
        Iterates through filename,file content key value pair to build word id map and word id to document map
	"""
	for filename in termlists.keys():
		fileIndex,uniq_ident=index_one_file(termlists[filename],filename,fileIndex,uniq_ident)
	return (WordMapDict,fileIndex)


def process_files(directory):
	"""        
        Iterates through files in dataset directory and create file_to_terms
	Cleansing of text + lower casing happens here  
        """
	file_to_terms = {}
	fileList = os.listdir(directory)
	for file in fileList:
		pattern = re.compile('[\W_]+')
		file_to_terms[file] = open(file, 'r',encoding='latin1').read().lower()
		file_to_terms[file] = pattern.sub(' ',file_to_terms[file])
		re.sub(r'[\W_]+','', file_to_terms[file])
		file_to_terms[file] = file_to_terms[file].split()
	wordmapdict,inverted_index_out = make_indices(file_to_terms,fileIndex,uniq_ident)
	return (wordmapdict,inverted_index_out) 


def writeToFile(file_type,out_dict):
	"""        
        Writes outputs to csv files 
        """
	if file_type == "Word_Mapping":
		with open('word-id-file.csv', 'w') as wordFile:
                	#declaring the fieldnames for the CSV file
                	fieldNames = ['word', 'word_id']
                	#creating a DictWriter object
                	csvWriter = csv.DictWriter(wordFile, fieldnames= fieldNames)
                	#writing the header
                	csvWriter.writeheader()
                	for word, word_id in out_dict.items():
                		#writing the row
                		csvWriter.writerow({'word': word, 'word_id': word_id})
	elif file_type == "Inverted_Index":
		with open('index-file.csv', 'w') as indexFile:
        		fieldNames = ['word_id', 'document_id_list']
        		csvWriter = csv.DictWriter(indexFile, fieldnames= fieldNames)
        		csvWriter.writeheader()
        		for word, doc_ids in out_dict.items():
		                doc_ids.sort() ## Alternatively sort files by doc_id before file read/processing to eliminate this 
		                csvWriter.writerow({'word_id': word, 'document_id_list': doc_ids})

def main():
	directory = 'G:\\Coding\\dataset'
	wordmapdict,inverted_index_out=process_files(directory)

	writeToFile("Word_Mapping",wordmapdict)
	writeToFile("Inverted_Index",inverted_index_out)

if __name__ == '__main__':
    main()
