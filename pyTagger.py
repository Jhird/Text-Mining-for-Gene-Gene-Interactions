#!/usr/env/bin python

import sys
import pandas as pd
import re
import readline # This allows user to backspace and erase answer

"""This program replaces Mindtagger with a python version that allows for the same functionality. The user has the chance to review each sampled sentences and label it as "correct" (1) or "incorrect" (-1)
"""

# Read file and create dataframe
filename = str(sys.argv[1])
df = pd.read_csv(filename,sep=',',header=0)
#df = pd.read_csv('is_beneficial_fungus_sample.csv',sep=',',header=0)
""" The Columns of this dataframe are [u'p1_id', u'p2_id', u'doc_id', u'sentence_index', u'label', u'expectation', u'tokens', u'p1_text', u'p1_start', u'p1_end', u'p2_text', u'p2_start', u'p2_end']"""


# Class to print text in color
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

### STEP 1: Print sentence in color where GREEN is the plant (p1) and BLUE is the microorganism (p2)

def changeComma(word):
	if word == "_COMMA_":
		return ","
	elif word == "-LRB-":
		return "("
	elif word == "-RRB-":
		return ")"
	else:
		return word


# Define a function to create a sentence from tokens
def printSentence(tokens,p1_s,p1_e,p2_s,p2_e):
	list_words = []	
	test = tokens.replace("{","")
	test = test.replace("}","")
	test = test.split(",")
	i = 0
	while i < len(test):
		if i <= len(test)-2 and '"' in test[i] and '"' in test[i+1]:
			list_words.append(test[i]+test[i+1])
			i = i + 2
			continue
		elif i <= len(test) - 3 and '"' in test[i] and '"' not in test[i+1] and '"' in test[i+2]:
			list_words.append(test[i]+test[i+1]+test[i+2])
			i = i + 3		
		elif i <= len(test) - 4 and '"' in test[i] and '"' not in test[i+1] and '"' not in test[i+2] and '"' in test[i+3]:
			list_words.append(test[i]+test[i+1]+test[i+2]+test[i+3])
			i = i + 4		
		else:
			list_words.append(test[i])
			i = i + 1
	for i in range(len(list_words)):
		if list_words[i] == '""':
			list_words[i] = '_COMMA_'
		else:
			continue
	before_first_org = ""
	between_orgs = ""
	after_second_org = ""
	organism_1 = ""
	organism_2 = ""
	has_capital_1 = 0
	has_capital_2 = 0
	if p1_s > 0 and (len(re.findall('[A-Z]',list_words[p1_s - 1])) == 1 or len(re.findall('[A-Z]\.',list_words[p1_s - 1])) == 1):
		has_capital_1 = 1
	else:
		has_capital_1 = 0

	if p2_s > 0 and (len(re.findall('[A-Z]',list_words[p2_s - 1])) == 1 or len(re.findall('[A-Z]\.',list_words[p2_s - 1])) == 1):
		has_capital_2 = 1
	else:
		has_capital_2 = 0 
	
	if p1_s < p2_s:
		org_1s, org_2s = p1_s-has_capital_1, p2_s-has_capital_2
		org_1e, org_2e = p1_e, p2_e			

	else:
		org_1s, org_2s = p2_s-has_capital_2, p1_s-has_capital_1
		org_1e, org_2e = p2_e, p1_e

	# Org 1
	for i in range(org_1s,org_1e+1):
		organism_1 = organism_1 + changeComma(list_words[i]) + " "
 	organism_1 = organism_1[0:len(organism_1)-1] # Remove last blank space
	
	# Org 2
	for i in range(org_2s,org_2e+1):
		organism_2 = organism_2 + changeComma(list_words[i]) + " "
	organism_2 = organism_2[0:len(organism_2)-1] # Remove last blank space
	
	# Before org 1	
	for i in range(0,org_1s):
		before_first_org = before_first_org + changeComma(list_words[i]) + " "
	
	# Between orgs
	for i in range(org_1e+1,org_2s):
		between_orgs = between_orgs + changeComma(list_words[i]) + " "
	
	# After org 2
	for i in range(org_2e+1,len(list_words)):
		after_second_org = after_second_org + changeComma(list_words[i]) + " "
	
	# Print it all
	if p1_s < p2_s: # If plant is first in sentence
		print before_first_org + bcolors.OKGREEN + bcolors.BOLD + bcolors.UNDERLINE + organism_1 + bcolors.ENDC + " " + between_orgs + bcolors.OKBLUE + bcolors.BOLD + bcolors.UNDERLINE + organism_2 + bcolors.ENDC + " " + after_second_org
		return [organism_1,organism_2]
	
	else: # If plant is second in sentences
		
		print before_first_org + bcolors.OKBLUE + bcolors.BOLD + bcolors.UNDERLINE + organism_1 + bcolors.ENDC + " " + between_orgs + bcolors.OKGREEN + bcolors.BOLD + bcolors.UNDERLINE + organism_2 + bcolors.ENDC + " " + after_second_org
		return [organism_2,organism_1]

### STEP 2: Ask the user to label it as correct (1) or incorrect (0)

# Initialize output dataframe
col_names = ["p1_id", "p2_id", "p1_name", "p2_name", "doc_id", "is_correct"]
p1,p2,p1_n,p2_n,doc,label = [],[],[],[],[],[]

#df columns = [u'p1_id', u'p2_id', u'doc_id', u'sentence_index', u'label', u'expectation', u'tokens', u'p1_text', u'p1_start', u'p1_end', u'p2_text', u'p2_start', u'p2_end']

for i in xrange(len(df.iloc[:,0])):

	t = str(df.iloc[i][6]) # tokens
	a = int(df.iloc[i][8]) # p1_start
	b = int(df.iloc[i][8]) # p1_end
	c = int(df.iloc[i][10]) # p2_start
	d = int(df.iloc[i][10]) # p2_end
	a_text = str(df.iloc[i][7]) # p1_text
	c_text = str(df.iloc[i][9]) # p2_text
        expect = str(df.iloc[i][5]) # expectation
	print "----------------------------------------------------------------------------"
	print "\n"
	print bcolors.WARNING + "Expectation = " + expect + bcolors.ENDC
	[candidate_plant, candidate_microbe] = printSentence(t,a,b,c,d)
	print bcolors.FAIL + bcolors.BOLD + str(i+1) + "/" + str(len(df)) + bcolors.ENDC
	print bcolors.HEADER + "\n'1' = Is correct \t '2' = Is incorrect \t '3' = Undetermined \t '4' = Save and quit\n" + bcolors.ENDC
	
	print "File name = " + filename + "\n"
	choice = raw_input("In the above sentence, the gene-gene pair interaction: ")
	
	if choice == '1':
		# Add to final lists
		p1.append(str(df.iloc[i][0]))
		p2.append(str(df.iloc[i][1]))
		p1_n.append(a_text)
		p2_n.append(c_text)
		doc.append(str(df.iloc[i][2]))
		label.append("true")
		
	elif choice == '2':
		# Add to final lists
		p1.append(str(df.iloc[i][0]))
		p2.append(str(df.iloc[i][1]))
		p1_n.append(a_text)
		p2_n.append(c_text)
		doc.append(str(df.iloc[i][2]))
		label.append("false")
	
	elif choice == '3':	
		# Add to final lists
		p1.append(str(df.iloc[i][0]))
		p2.append(str(df.iloc[i][1]))
		p1_n.append(a_text)
		p2_n.append(c_text)
		doc.append(str(df.iloc[i][2]))
		label.append("neutral")

	elif choice == '4':
		break
		
	else:
		print "\n" + bcolors.WARNING + "That's not a valid option!" + bcolors.ENDC + "\n"
		continue
		

### STEP 3: Save results and exit
output_file = "tagged_" + filename
out_df = pd.DataFrame()
out_df["g1_id"] = p1
out_df["g2_id"] = p2
out_df["g1_name"] = p1_n
out_df["g2_name"] = p2_n
out_df["doc_id"] = doc
out_df["is_correct"] = label
out_df.to_csv(output_file,sep=',',index=False)
print "File has been saved as ", output_file

