The following commands were used to extract the names of all human genes from
the "unigene_result.txt" file

1) Get all lines with the genes names | Remove the Homo sapiens part | Sort | Get unique values > save to file

#Bash#
grep ", Homo sapiens" unigene_result.txt | sed 's/, Homo sapiens/\x/' | sort | uniq -u > human_genes.tsv

You can now read the human_genes.tsv with python as

#Python#
f = open('human_genes.tsv', 'r')
genes = f.read().splitlines()
f.close()
