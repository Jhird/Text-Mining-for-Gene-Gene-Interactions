#!/usr/bin/env python

f = open('/root/ATHEROSCLEROSIS_app/udf/human_genes.tsv','r')
genes = f.read().splitlines()
f.close()



from deepdive import *
import re


@tsv_extractor
@returns(lambda
        mention_id       = "text",
        mention_text     = "text",
        doc_id           = "text",
        sentence_index   = "int",
        word_index       = "int",
    :[])
def extract(
        doc_id         = "text",
        sentence_index = "int",
        tokens         = "text[]",
        lemmas         = "text[]",
    ):
    """
    Finds tokens that are mentions of genes is human_genes.tsv.
    """
    num_tokens = len(tokens)
    # find all indexes of gene mentions
    indexes = (i for i in xrange(num_tokens) if tokens[i] in genes)
    for begin_index in indexes:
        # generate a mention identifier
        mention_id = "%s_%d_%d" % (doc_id, sentence_index, begin_index)
        mention_text = str(tokens[begin_index])
        # Output a tuple for each GENE phrase
        yield [
            mention_id,
            mention_text,
            doc_id,
            sentence_index,
            begin_index,
        ]
