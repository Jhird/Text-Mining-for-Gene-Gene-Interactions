#!/usr/bin/env python
from deepdive import *
import random
from collections import namedtuple

def makeSentence(list_of_words):
	s = ""
	for word in list_of_words:
		s = s + word + " "
	return s[0:len(s)-1]

GenePairLabel = namedtuple('GenePairLabel', 'g1_id, g2_id, label, type')

@tsv_extractor
@returns(lambda
        g1_id   = "text",
        g2_id   = "text",
        label   = "int",
        rule_id = "text",
    :[])
# heuristic rules for finding positive/negative examples of gene-gene interactions
def supervise(
        g1_id="text", g1_index="int",
        g2_id="text", g2_index="int",
        doc_id="text", sentence_index="int", sentence_text="text",
        tokens="text[]", lemmas="text[]", pos_tags="text[]", ner_tags="text[]",
        dep_types="text[]", doc_offsets="int[]",
    ):

    ## Constants
        
    GENE_WORDS = ["gene","genes"]

    PHRASAL_INTERACTIONS = ["interacts with","interaction with","interact","gene-gene interaction","genetic interaction"]

    REGULATION_WORDS = ["downregulates","downregulated","downregulate","upregulates","upregulated","upregulate"]
    
    MAX_DIST = 10

    # Common data objects
    g1_start_idx = min(g1_index, g2_index)
    g2_start_idx = max(g1_index, g2_index)
    

    # Find words before and after gene mentions and form sentences
    head_tokens = tokens[0:g1_start_idx]
    intermediate_tokens = tokens[g1_start_idx+1:g2_start_idx]
    tail_tokens = tokens[g2_start_idx+1:]
    sentence_before_genes = makeSentence(tokens[0:g1_start_idx]).lower()
    sentence_between_genes = makeSentence(tokens[g1_start_idx+1:g2_start_idx]).lower()
    sentence_after_genes = makeSentence(tokens[g2_start_idx+1:]).lower()
    full_sentence = makeSentence(tokens).lower()
   
    genepair = GenePairLabel(g1_id=g1_id, g2_id=g2_id, label=None, type=None)
   

# len([media_names[i] for i in range(len(media_names)) if media_names[i] in sentence])

    # RULE 1 (POSITIVE): A PHRASAL_INTERACTION appears in between genes
    if len([PHRASAL_INTERACTIONS[i] for i in range(len(PHRASAL_INTERACTIONS)) if PHRASAL_INTERACTIONS[i] in sentence_between_genes])>0:
        yield genepair._replace(label=2, type='POS:geneticInteraction_between_genes')

    # RULE 2 (POSITIVE): A PHRASAL_INTERACTION appears before genes
    if len([PHRASAL_INTERACTIONS[i] for i in range(len(PHRASAL_INTERACTIONS)) if PHRASAL_INTERACTIONS[i] in sentence_before_genes])>0:
        yield genepair._replace(label=1, type='POS:geneticInteraction_before_genes')

    # RULE 3 (NEGATIVE): Not a single GENE_WORD appears in sentence
    if len([GENE_WORDS[i] for i in range(len(GENE_WORDS)) if GENE_WORDS[i] in full_sentence])==0:
        yield genepair._replace(label=-1, type='NEG:noGENE_WORD_in_sentence')

    # RULE 4 (NEUTRAL): REGULATION word in sentence
    if len([REGULATION_WORDS[i] for i in range(len(REGULATION_WORDS)) if REGULATION_WORDS[i] in full_sentence])>0:
        yield genepair._replace(label=0, type='NULL:regulation')
    	
    # RULE 5 (NEGATIVE): Sentences that are too long between two geness
    if len(intermediate_tokens) > MAX_DIST:
        yield genepair._replace(label=-1, type='neg:Too_Far_Apart')

