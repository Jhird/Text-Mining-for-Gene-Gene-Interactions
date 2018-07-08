import numpy as np
import pandas as pd
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.embed import file_html
from bokeh.resources import CDN

# Read .csv bokeh data
df = pd.read_csv('correct_bokeh_data.csv',sep=',',header=0)

# Create list of all genes, genes_A, genes_B, expectation and pubmed ids
all_genes = list(set(list(df['g1_text']) + list(df['g2_text'])))
genes_A = list(df['g1_text'])
genes_B = list(df['g2_text'])
expectation = list(df['expectation'])
doc_id = list(df['doc_id'])


# Initialize Adjacency matrix (ALL)
adj_matrix = np.zeros([len(all_genes),len(all_genes)])

# Function to get expectation value for a given pair of genes
def mapRelationship(g1,g2):
        if g1 == g2:
                return 1.0
        indexes_A = [i for i in range(len(genes_A)) if genes_A[i] == g1]
        indexes_B = [i for i in range(len(genes_A)) if genes_B[i] == g1]
        count = 0.0
        exp_total = 0.0
        for i in indexes_A:
                if genes_B[i] == g2:
                        count = count + 1.
                        exp_total = exp_total + expectation[i]
        for i in indexes_B:
                if genes_A[i] == g2:
                        count = count + 1.
                        exp_total = exp_total + expectation[i]
        if count == 0:
                return 0.0
        final_exp = float(exp_total) / float(count)
        return final_exp

def mapPublications(g1,g2):
        if g1 == g2:
                return ""
        indexes_A = [i for i in range(len(genes_A)) if genes_A[i] == g1]
        indexes_B = [i for i in range(len(genes_A)) if genes_B[i] == g1]
        appears_in = ""
        for i in indexes_A:
                if genes_B[i] == g2:
                        appears_in = appears_in + str(doc_id[i]) + " "
        for i in indexes_B:
                if genes_A[i] == g2:
                        appears_in = appears_in + str(doc_id[i]) + " "
        final_pubmed = appears_in[0:len(appears_in)-1]
        return final_pubmed

# Fill out matrix with all gene-gene relationships
all_pubmed = []
for i in xrange(len(all_genes)):
        for j in xrange(len(all_genes)):
                    adj_matrix[i,j] = mapRelationship(all_genes[i],all_genes[j])
                    pmid = mapPublications(all_genes[i],all_genes[j])
                    all_pubmed.append(pmid)

import matplotlib.colors as colors

xname = []
yname = []
color = []
alpha = []
for i, node1 in enumerate(all_genes):
        for j, node2 in enumerate(all_genes):
                xname.append(node1)
                yname.append(node2)

                if i == j:
                        color.append(colors.rgb2hex((1.0,0.0,0.0)))
                        alpha.append(1.0)
                else:
                        color.append(colors.rgb2hex((adj_matrix[i,j],0.0,0.0)))
                        alpha.append(adj_matrix[i,j])

source = ColumnDataSource(data=dict(
        xname = xname,
        yname = yname,
        colors = color,
        alphas = alpha,
        count = adj_matrix.flatten(),
        all_pubmed = all_pubmed
))

p = figure(title="Gene-Gene Interactions in Atherosclerosis", x_axis_location = "above", tools="hover,save,box_zoom,reset", y_range=list(reversed(all_genes)), x_range=all_genes)

p.plot_width = 1800
p.plot_height = 1800
p.grid.grid_line_color = None
p.axis.axis_line_color = None
p.axis.major_tick_line_color = None
p.axis.major_label_text_font_size = "7pt"
p.axis.major_label_standoff = 0
p.xaxis.major_label_orientation = np.pi/3

p.rect('xname', 'yname', 0.9, 0.9, source=source,
       color='colors', alpha='alphas', line_color=None,
       hover_line_color='black', hover_color='colors')

p.select_one(HoverTool).tooltips = [
        ('Gene-pair: ', '@yname, @xname'),
        ('Found in: ', '@all_pubmed'),
        ('Probability: ', '@alphas'),
]

output_file("Gene-Gene_Interactions_Atherosclerosis.html", title="Andellor_Genetic_Interactions.py")

show(p)

#html = file_html(p, CDN, "Gene-Gene_Interactions_Andellor")
        
         
