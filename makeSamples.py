#!/usr/env/bin python

import os

#os.system('deepdive sql eval "SELECT hsi.g1_id, hsi.g2_id, s.doc_id, s.sentence_index, hsi.label, hsi.expectation, s.tokens, gp.g1_name AS g1_text, gm1.word_index AS g1_index, gp.g2_name AS g2_text, gm2.word_index AS g2_start FROM do_genes_interact_label_inference hsi, gene_pair gp, gene_mention gm1, gene_mention gm2, sentences s WHERE hsi.g1_id = gm1.mention_id AND gm1.doc_id = s.doc_id AND gm1.sentence_index = s.sentence_index AND hsi.g2_id = gm2.mention_id AND gm2.doc_id = s.doc_id AND gm2.sentence_index = s.sentence_index AND hsi.expectation >= 0.85 ORDER BY random() LIMIT 300" format=csv header=1 > do_genes_intereact_high_sample.csv')

#os.system('deepdive sql eval "SELECT hsi.g1_id, hsi.g2_id, s.doc_id, s.sentence_index, hsi.label, hsi.expectation, s.tokens, gp.g1_name AS g1_text, gm1.word_index AS g1_index, gp.g2_name AS g2_text, gm2.word_index AS g2_start FROM do_genes_interact_label_inference hsi, gene_pair gp, gene_mention gm1, gene_mention gm2, sentences s WHERE hsi.g1_id = gm1.mention_id AND gm1.doc_id = s.doc_id AND gm1.sentence_index = s.sentence_index AND hsi.g2_id = gm2.mention_id AND gm2.doc_id = s.doc_id AND gm2.sentence_index = s.sentence_index AND hsi.expectation >= 0.40 AND hsi.expectation <= 0.80 ORDER BY random() LIMIT 300" format=csv header=1 > do_genes_intereact_medium_sample.csv')

os.system('deepdive sql eval "SELECT hsi.g1_id, hsi.g2_id, s.doc_id, s.sentence_index, hsi.label, hsi.expectation, s.tokens, hsi.g1_name AS g1_text, gm1.word_index AS g1_index, hsi.g2_name AS g2_text, gm2.word_index AS g2_index FROM do_genes_interact_label_inference hsi, gene_mention gm1, gene_mention gm2, sentences s WHERE hsi.g1_id = gm1.mention_id AND gm1.doc_id = s.doc_id AND gm1.sentence_index = s.sentence_index AND gm1.mention_text = hsi.g1_name AND gm2.mention_text = hsi.g2_name AND hsi.g2_id = gm2.mention_id AND gm2.doc_id = s.doc_id AND gm2.sentence_index = s.sentence_index AND hsi.expectation >= 0.85 LIMIT 400" format=csv header=1 > do_genes_intereact.csv')


#os.system('deepdive sql eval "SELECT hsi.p1_id, hsi.p2_id, s.doc_id, s.sentence_index, hsi.label, hsi.expectation, s.tokens, pm1.mention_text AS p1_text, pm1.begin_index AS p1_start, pm1.end_index AS p1_end, pm2.mention_text AS p2_text, pm2.begin_index AS p2_start, pm2.end_index AS p2_end FROM is_beneficial_fungus_label_inference hsi, plant_mention pm1, fungus_mention pm2, sentences s WHERE hsi.p1_id = pm1.mention_id AND pm1.doc_id = s.doc_id AND pm1.sentence_index = s.sentence_index AND hsi.p2_id = pm2.mention_id AND pm2.doc_id = s.doc_id AND pm2.sentence_index = s.sentence_index AND expectation >= 0.65 ORDER BY random() LIMIT 250" format=csv header=1 > is_beneficial_fungus_sample.csv')

#os.system('deepdive sql eval "SELECT hsi.p1_id, hsi.p2_id, s.doc_id, s.sentence_index, hsi.label, hsi.expectation, s.tokens, pm1.mention_text AS p1_text, pm1.begin_index AS p1_start, pm1.end_index AS p1_end, pm2.mention_text AS p2_text, pm2.begin_index AS p2_start, pm2.end_index AS p2_end FROM is_beneficial_prokaryote_label_inference hsi, plant_mention pm1, prokaryote_mention pm2, sentences s WHERE hsi.p1_id = pm1.mention_id AND pm1.doc_id = s.doc_id AND pm1.sentence_index = s.sentence_index AND hsi.p2_id = pm2.mention_id AND pm2.doc_id = s.doc_id AND pm2.sentence_index = s.sentence_index AND expectation >= 0.65 ORDER BY random() LIMIT 250" format=csv header=1 > is_beneficial_prokaryote_sample.csv')

#os.system('deepdive sql eval "SELECT hsi.p1_id, hsi.p2_id, s.doc_id, s.sentence_index, hsi.label, hsi.expectation, s.tokens, pm1.mention_text AS p1_text, pm1.begin_index AS p1_start, pm1.end_index AS p1_end, pm2.mention_text AS p2_text, pm2.begin_index AS p2_start, pm2.end_index AS p2_end FROM is_pathogenic_fungus_label_inference hsi, plant_mention pm1, fungus_mention pm2, sentences s WHERE hsi.p1_id = pm1.mention_id AND pm1.doc_id = s.doc_id AND pm1.sentence_index = s.sentence_index AND hsi.p2_id = pm2.mention_id AND pm2.doc_id = s.doc_id AND pm2.sentence_index = s.sentence_index AND expectation >= 0.65 ORDER BY random() LIMIT 250" format=csv header=1 > is_pathogenic_fungus_sample.csv')

#os.system('deepdive sql eval "SELECT hsi.p1_id, hsi.p2_id, s.doc_id, s.sentence_index, hsi.label, hsi.expectation, s.tokens, pm1.mention_text AS p1_text, pm1.begin_index AS p1_start, pm1.end_index AS p1_end, pm2.mention_text AS p2_text, pm2.begin_index AS p2_start, pm2.end_index AS p2_end FROM is_pathogenic_prokaryote_label_inference hsi, plant_mention pm1, prokaryote_mention pm2, sentences s WHERE hsi.p1_id = pm1.mention_id AND pm1.doc_id = s.doc_id AND pm1.sentence_index = s.sentence_index AND hsi.p2_id = pm2.mention_id AND pm2.doc_id = s.doc_id AND pm2.sentence_index = s.sentence_index AND expectation >= 0.65 ORDER BY random() LIMIT 250" format=csv header=1 > is_pathogenic_prokaryote_sample.csv')
