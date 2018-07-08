#!usr/bin/env python

# Import Biopython Entrez library
from Bio import Entrez
import os

# Set directory
os.chdir(os.getcwd())

# Tell NCBI who I am
Entrez.email = "jahir.brokenkite@gmail.com"


# Search terms:
search_terms = ["atherosclerosis"]

# Get PUBMED ID numbers

pubmed_ids = []

for term in search_terms:

    handle = Entrez.esearch(db="pubmed", term=term,retmax='100000')
    record = Entrez.read(handle)
    pubmed_ids = pubmed_ids + record['IdList']

pubmed_ids = list(set(pubmed_ids)) 

# Get PUBMED Titles and Abstracts

f = open('articles.tsv','w')

for i in range(len(pubmed_ids)):

    try:
        handle = Entrez.efetch(db="pubmed", id=pubmed_ids[i], retmode="xml")
    except:
        continue
    try:
        record = Entrez.read(handle,validate=False)
    except:
        continue
    try:
        title = record[0]['MedlineCitation']['Article']['ArticleTitle']
    except:
        title = "NOT FOUND"
    try:
        abstract = record[0]['MedlineCitation']['Article']['Abstract']['AbstractText'][0]
    except:
        abstract = "NOT FOUND"

    if title == "NOT FOUND" or abstract == "NOT FOUND":
        continue
    else:
        f.write(str(pubmed_ids[i]))
        f.write('\t')
        f.write(title.encode('ascii','ignore') + ' : ' + abstract.encode('ascii','ignore'))
        f.write('\n')

f.close()
