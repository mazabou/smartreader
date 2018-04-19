# Perform the necessary imports
from bokeh.io import curdoc
from bokeh.layouts import column, widgetbox, row, layout
from bokeh.plotting import figure
from bokeh.palettes import PuBu
from bokeh.io import show, output_notebook, output_file
from bokeh.models import ColumnDataSource, ranges, LabelSet, HoverTool, Select, FactorRange, CheckboxGroup, Slider, Button
from bokeh.models.widgets import Paragraph, TableColumn, DataTable, RangeSlider, Tabs, Panel

import math
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from math import pi
import preprocess as pp
from openers import *

# Loading data
articledf = open_metadata()

words = open_words()
words2 = dict([(v,k) for k,v in words.iteritems()])

col,data = open_data()

#Generating colnames
colnames = words.items()
colnames.sort(key=lambda x: x[1])
colnames = [x[0] for x in colnames]

#Generating row
row = [[i for j in range(len(col[i]))] for i in range(len(col))]

#Creating global variables
data1 = []
col1 = []
colnames1 = []
data2 = []
data3=[]
source = ColumnDataSource(dict(x=[words2[l] for l in col[0]], y=data[0]))


# Create plots and widgets
hover = HoverTool(tooltips=[('word', '@x'),('occ','@y'),])
plot = figure(plot_width=len(col[0])*10, plot_height=350,x_minor_ticks=2,x_range = source.data["x"],y_range= ranges.Range1d(start=0,end=20),tools=[hover,'xpan','box_zoom','reset'],toolbar_location='left')

sourcea = ColumnDataSource(dict(x=[words2[l] for l in col[0]], y=data[0]))

plot.vbar(source=sourcea,x='x',top='y',bottom=0,width=0.7,color=PuBu[7][2],alpha=0.3)
plot.vbar(source=source,x='x',top='y',bottom=0,width=0.7,color=PuBu[7][2],alpha=0.6)

plot.xaxis.major_label_orientation = math.pi/2

articles = articledf.title.tolist()
art2i = dict(zip(articles,range(len(articles))))

menu = Select(options=articles,value=articles[0], title='Article')

par = Paragraph(text="""Status""",width=200, height=50)

i = 0

# Add callback to widgets
def callback(attr, old, new):
	global data1,data2,col1,colnames1
	i = art2i[menu.value]
	par.text = "Computing..."
	sourcea.data = ColumnDataSource(dict(x=[words2[l] for l in col[i]], y=data[i])).data
	if menu_proc.value == "Raw":
		source.data = ColumnDataSource(dict(x=[words2[l] for l in col[i]], y=data[i])).data
		plot.x_range.factors = [words2[l] for l in col[i]]
		plot.width = len(col[i])*10

		arr = np.array(data[art2i[menu.value]])
		top10 = [words2[l] for l in [col[art2i[menu.value]][p] for p in arr.argsort()[-10:][::-1]]]
		source1.data = ColumnDataSource(dict(words=top10,)).data
	elif menu_proc.value == "Prunning":
		updated = []
		j = 0
		for l in col[i]:
			if l in colnames1: 
				updated.append(data1[i][j])
				j+=1
			else:
				updated.append(0)
		source.data = ColumnDataSource(dict(x=[words2[l] for l in col[i]], y=updated)).data
		plot.x_range.factors = [words2[l] for l in col[i]]
		plot.width = len(col[i])*10

		arr = np.array(data1[art2i[menu.value]])
		top10 = [words2[l] for l in [colnames1[j] for j in [col1[art2i[menu.value]][p] for p in arr.argsort()[-10:][::-1]]]]
		source1.data = ColumnDataSource(dict(words=top10,)).data
	elif menu_proc.value == 'Prunning+tfidf':
		updated = []
		j = 0
		for l in col[i]:
			if l in colnames1:
				updated.append(data2[i][j])
				j+=1
			else:
				updated.append(0)
		source.data = ColumnDataSource(dict(x=[words2[l] for l in col[i]], y = updated)).data

		arr = np.array(data2[art2i[menu.value]])
		top10 = [words2[l] for l in [colnames1[j] for j in [col1[art2i[menu.value]][p] for p in arr.argsort()[-10:][::-1]]]]
		source1.data = ColumnDataSource(dict(words=top10,)).data

	elif menu_proc.value == "tfidf":
		source.data = ColumnDataSource(dict(x=[words2[l] for l in col[i]], y=data2[i])).data
		arr = np.array(data2[art2i[menu.value]])
		top10 = [words2[l] for l in [col[art2i[menu.value]][p] for p in arr.argsort()[-10:][::-1]]]
		source1.data = ColumnDataSource(dict(words=top10,)).data
	par.text = "Finished!"

menu.on_change('value', callback)


range_slider = RangeSlider(start=0, end=1, value=(0,0.3), step=.01, title="Threashold")

button = Button(label='Set threashold values')

def update():
	global data1,col1,colnames1
	par.text = "Computing..."
	i = art2i[menu.value]
	if menu_proc.value == "Prunning":
		data1,col1,colnames1 = pp.pruning(data,col,colnames,range_slider.value[0],range_slider.value[1])
		updated = []
		j = 0
		for l in col[i]:
			if l in colnames1: 
				updated.append(data1[i][j])
				j+=1
			else:
				updated.append(0)
		source.data = ColumnDataSource(dict(x=[words2[l] for l in col[i]], y=updated)).data
		arr = np.array(data1[art2i[menu.value]])
		top10 = [words2[l] for l in [colnames1[j] for j in [col1[art2i[menu.value]][p] for p in arr.argsort()[-10:][::-1]]]]
		source1.data = ColumnDataSource(dict(words=top10,)).data
	elif menu_proc.value == 'Prunning+tfidf':
		data1,col1,colnames1 = pp.pruning(data,col,colnames,range_slider.value[0],range_slider.value[1])
		data2 = pp.tfidf(data1,col1,len(colnames1))
		updated = []
		j = 0
		for l in col[i]:
			if l in colnames1: 
				updated.append(data2[i][j])
				j+=1
			else:
				updated.append(0)
		source.data = ColumnDataSource(dict(x=[words2[l] for l in col[i]], y=updated)).data
		arr = np.array(data2[art2i[menu.value]])
		top10 = [words2[l] for l in [colnames1[j] for j in [col1[art2i[menu.value]][p] for p in arr.argsort()[-10:][::-1]]]]
		source1.data = ColumnDataSource(dict(words=top10,)).data
	par.text = "Finished!"

button.on_click(update)

menu_proc = Select(options=["Raw","Prunning","tfidf","Prunning+tfidf","Prunning+tfidf+Normalization"],value="Raw", title='Pre-Processing')

# Add callback to widgets
def callback_proc(attr, old, new):
	global data1,col1,colnames1,data2,data3
	i = art2i[menu.value]
	par.text = "Computing..."
	if menu_proc.value == "Raw":
		source.data = ColumnDataSource(dict(x=[words2[l] for l in col[i]], y=data[i])).data
		plot.x_range.factors = [words2[l] for l in col[i]]
		plot.width = len(col[i])*10
		arr = np.array(data[art2i[menu.value]])
		top10 = [words2[l] for l in [col[art2i[menu.value]][p] for p in arr.argsort()[-10:][::-1]]]
		source1.data = ColumnDataSource(dict(words=top10,)).data
	elif menu_proc.value == "Prunning":
		data1,col1,colnames1 = pp.pruning(data,col,colnames,range_slider.value[0],range_slider.value[1])
		updated = []
		j = 0
		for l in col[i]:
			if l in colnames1: 
				updated.append(data1[i][j])
				j+=1
			else:
				updated.append(0)
		source.data = ColumnDataSource(dict(x=[words2[l] for l in col[i]], y=updated)).data
		arr = np.array(data1[art2i[menu.value]])
		top10 = [words2[l] for l in [colnames1[j] for j in [col1[art2i[menu.value]][p] for p in arr.argsort()[-10:][::-1]]]]
		source1.data = ColumnDataSource(dict(words=top10,)).data
	elif menu_proc.value == 'Prunning+tfidf':
		data1,col1,colnames1 = pp.pruning(data,col,colnames,range_slider.value[0],range_slider.value[1])
		data2 = pp.tfidf(data1,col1,len(colnames1))
		updated = []
		j = 0
		for l in col[i]:
			if l in colnames1: 
				updated.append(data2[i][j])
				j+=1
			else:
				updated.append(0)
		source.data = ColumnDataSource(dict(x=[words2[l] for l in col[i]], y=updated)).data

		arr = np.array(data2[art2i[menu.value]])
		top10 = [words2[l] for l in [colnames1[j] for j in [col1[art2i[menu.value]][p] for p in arr.argsort()[-10:][::-1]]]]
		source1.data = ColumnDataSource(dict(words=top10,)).data
	elif menu_proc.value == "tfidf":
		data2 = pp.tfidf(data,col,len(colnames))
		source.data = ColumnDataSource(dict(x=[words2[l] for l in col[i]], y=data2[i])).data

		arr = np.array(data2[art2i[menu.value]])
		top10 = [words2[l] for l in [col[art2i[menu.value]][p] for p in arr.argsort()[-10:][::-1]]]
		source1.data = ColumnDataSource(dict(words=top10,)).data
	elif menu_proc.value == "Prunning+tfidf+Normalization":
		data1,col1,colnames1 = pp.pruning(data,col,colnames,range_slider.value[0],range_slider.value[1])
		data2 = pp.tfidf(data1,col1,len(colnames1))
		data3 = pp.normalization(data2)
		updated = []
		j = 0
		for l in col[i]:
			if l in colnames1: 
				updated.append(data3[i][j])
				j+=1
			else:
				updated.append(0)
		source.data = ColumnDataSource(dict(x=[words2[l] for l in col[i]], y=updated)).data

		arr = np.array(data3[art2i[menu.value]])
		top10 = [words2[l] for l in [colnames1[j] for j in [col1[art2i[menu.value]][p] for p in arr.argsort()[-10:][::-1]]]]
		source1.data = ColumnDataSource(dict(words=top10,)).data


	par.text = "Finished!"

menu_proc.on_change('value', callback_proc)


arr = np.array(data[art2i[menu.value]])
top10 = [words2[l] for l in [col[art2i[menu.value]][p] for p in arr.argsort()[-10:][::-1]]]
source1 = ColumnDataSource(dict(words=top10,))
data_table = DataTable(source=source1, columns=[TableColumn(field="words", title="Word"),], width=200, height=280)

p1 = Paragraph(text="Top 10 words")


newlayout = layout([menu],[column(menu_proc,widgetbox(range_slider,button,par)),column(p1,data_table)],[plot])

# Create a Panel with a title for each tab
first = Panel(child=newlayout, title='Pre-Processing')

data1,col1,colnames1 = pp.pruning(data,col,colnames,range_slider.value[0],range_slider.value[1])
data2 = pp.tfidf(data1,col1,len(colnames1))
data3 = pp.normalization(data2)

data_pp = data3[:]
col_pp = col1[:]

#Generating row
row_pp = [[i for j in range(len(col_pp[i]))] for i in range(len(col_pp))]

colnames_pp = colnames1[:]
import similarityMeasures as sm
import kmeans

bestmatches,clusters,clusters_col = kmeans.kcluster(col_pp,data_pp,len(colnames_pp),distance = sm.normalizedCosineSimilarity,k=4)
import dimensionreduce
data_csr = [e for v in data_pp for e in v]
col_csr = [e for v in col_pp for e in v]
row_csr = [e for v in row_pp for e in v]

loc = dimensionreduce.reduction(csr_matrix((data_csr,(row_csr, col_csr))).toarray())

rownames = articledf.title
colormap = np.array(["#6d8dca", "#69de53", "#723bca", "#c3e14c", "#c84dc9", "#68af4e", "#6e6cd5","#e3be38", "#4e2d7c", "#5fdfa8", "#d34690", "#3f6d31", "#d44427", "#7fcdd8", "#cb4053", "#5e9981","#803a62", "#9b9e39", "#c88cca", "#e1c37b", "#34223b", "#bdd8a3", "#6e3326", "#cfbdce", "#d07d3c","#52697d", "#7d6d33", "#d27c88", "#36422b", "#b68f79"])
plot_kmeans = figure(plot_width=700, plot_height=600, title="KMeans clustering of the news",tools="pan,wheel_zoom,box_zoom,reset,hover,previewsave",x_axis_type=None, y_axis_type=None, min_border=1)

kmeans_df = pd.DataFrame(loc, columns=['x', 'y'])
cluster_list = [0]*len(rownames)
for i in range(1,len(bestmatches)):
    for j in bestmatches[i]:
        cluster_list[j]=i
kmeans_df['cluster'] = pd.DataFrame(cluster_list)
kmeans_df['title'] = pd.DataFrame(rownames)
kmeans_df['color'] = colormap[cluster_list]
kmeans_df['source'] = articledf.source
plot_kmeans.scatter(x='x', y='y',color='color', source=kmeans_df)
hover = plot_kmeans.select(dict(type=HoverTool))
hover.tooltips={"title": "@title","cluster":"@cluster","source":"@source"}

second = Panel(child=plot_kmeans, title='Clustering')

# Put the Panels in a Tabs object
tabs = Tabs(tabs=[first,second])

curdoc().add_root(tabs)