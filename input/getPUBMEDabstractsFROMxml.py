# -*- coding: utf-8 -*-
"""
Created on Tue Sep 06 18:45:27 2016

@author: Jahir Gutierrez
"""

from Bio import Entrez
import sys

filename = str(sys.argv[1])
handle = open(filename)
records = Entrez.parse(handle)
out_filename = filename.replace('.xml','.tsv')
f = open(out_filename,'w')
for record in records:
    try:
        pmid = record['MedlineCitation']['PMID'].encode('ascii','ignore')
        title = record['MedlineCitation']['Article']['ArticleTitle'].encode('ascii','ignore')
        abstract_list = record['MedlineCitation']['Article']['Abstract']['AbstractText']
        abstract = ''
    except:
        continue
    for element in abstract_list:
        abstract = abstract + element.encode('ascii','ignore') + ' '
    abstract = abstract[0:len(abstract)-1]
    f.write(pmid)
    f.write('\t')
    f.write(title + " : " + abstract)
    f.write('\n')
f.close()
handle.close()        
