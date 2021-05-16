import os
import re
import csv
import json
import time
import pickle
import textdistance
import numpy as np

from math import log
from tqdm import tqdm
from rank_bm25 import BM25Okapi

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

def read_text(filename):
	raw_text = ''
	with open(filename) as file:
		for line in file:
			raw_text += line
	return raw_text

def write_text(text, filename):
	with open(filename, 'w') as file:
		for line in text:
			file.write(line)
			
def read_json(filename):
	with open(filename) as file:
		data = json.load(file)
	return data

def write_json(data, filename):
	with open(filename, 'w') as file:
		json.dump(data, file)

def read_csv(filename):
	with open(filename, encoding="utf8") as file:
		reader = csv.reader(file)
		data = []
		for row in reader:
			data.append(row)
	return data

def write_csv(data, filename):
	with open(filename, 'w') as file:
		writer = csv.writer(file)
		for row in data:
			writer.writerow(row)

def read_pickle(filename):
	with open(filename,'rb') as f:
		data = pickle.load(f)
	return data

def clean(text):
	global lemmatizer
	global stop_words

	text = text.lower().strip()
	text = re.sub(r'[^a-z\s]', '', text)
	text = ' '.join([w for w in word_tokenize(text) if not w in stop_words])
	text = ' '.join([lemmatizer.lemmatize(w) for w in word_tokenize(text) if not w in stop_words])
	
	return text

# bm25_corpus = pickle.load(open('./data/bm25_corpus1.pkl','rb'))
# bm25_corpus2 = pickle.load(open('./data/bm25_corpus2.pkl','rb'))
# bm25_corpus = bm25_corpus + bm25_corpus2
docs = read_pickle('./data/docs.pkl')
index = read_pickle('./data/index.pkl')
sentences = read_json('./data/corpus1.json')
sentences2 = read_json('./data/corpus2.json')
bm25 = pickle.load(open('./data/bm25.pkl','rb'))
company = read_pickle('./data/updated_Docs.pkl')
company_index = read_pickle('./data/company_index.pkl')
matrix = pickle.load(open('./data/matrix.pkl','rb'))
companies = read_json('./data/companies')['company_names']
vocabulary = list(index.keys())
graph = read_pickle('./data/new_graph_data.pkl')
table_index = read_pickle('./data/table_index.pkl')


def TF_IDF_doc(query):
	query_vec = [0]*len(vocabulary)
	query_words = clean(query).split()
	
	for i in query_words:
		if i in vocabulary:
			query_vec[vocabulary.index(i)]+=1
			
	for i in range(len(query_vec)):
		query_vec[i]*=log((len(docs)/len(index[vocabulary[i]])+1),10)

	query_vec = np.array(query_vec).reshape(len(query_vec),1)
	scores = matrix.dot(query_vec)
	result = [(scores[i][0],i) for i in range(len(scores))]
	return result

def TF_IDF_sentence(query,sentence):
	query_words = clean(query).split()
	sentence_words = clean(sentence).split()
	score = 0
	if not len(sentence_words): 
		return 0
	for i in query_words:
		if i in index:
			tf = sentence_words.count(i)/len(sentence_words)
			idf = log(1+(len(docs)/len(index[i])),10)
			score+= tf*idf
	return score

def cosine_similarityF_sentence(query,sentence):
	return textdistance.cosine.normalized_similarity(clean(query),sentence)

def BM25_sentence(query,doc_id):
	for i in sentences2:
		sentences[i] = sentences2[i]

	doc_corpus = sentences[str(doc_id)]
	bm25_sen = BM25Okapi([i.split() for i in doc_corpus])
	top_sentences =  bm25_sen.get_top_n(query,doc_corpus, n=10)
	return top_sentences

def BM25_doc(query, number_of_records, page_no):

	query = list(clean(query).split())
	scores = bm25.get_scores(query)
	results = sorted( [(scores[i],i) for i in range(len(scores))], reverse = True)[number_of_records * (page_no - 1) : number_of_records * (page_no)]
	documents = []
	for result in results:
		doc_id = int(docs[result[1]][:-5])
		documents.append({
			'doc_id': doc_id,
			'score': result[0],
			'company': company[str(doc_id)+'.json']['company'],
			'sentences': BM25_sentence(query, doc_id),
			'date_filled': company[str(doc_id)+'.json']['date_filled'],
			'link':company[str(doc_id)+'.json']['link']
		})
	return documents

def retrieve_sentences_from_doc(query, doc_id):

	for i in sentences2:
		sentences[i] = sentences2[i]
	sentence_ranking = []
	
	for sentence in sentences[str(doc_id)]:
		sentence_ranking.append({'score': TF_IDF_sentence(query,sentence),'sentence': sentence})

	top_sentences = sorted(sentence_ranking, reverse=True, key= lambda x: x['score'])[:10]
	top_sentences = [i['sentence'] for i in top_sentences]
	return top_sentences

def retrieve_documents_from_query(query, number_of_records, page_no):

	ranking = TF_IDF_doc(query)
	results = sorted(ranking, reverse=True)[number_of_records * (page_no - 1) : number_of_records * (page_no)]
	documents = []
	for result in results:
		doc_id = int(docs[result[1]][0][:-5])
		documents.append({
			'doc_id': doc_id,
			'score': result[0],
			'company': company[str(doc_id)+'.json']['company'],
			'sentences': BM25_sentence(query, doc_id),
			'date_filled': company[str(doc_id)+'.json']['date_filled'],
			'link':get_link(company[str(doc_id)+'.json']['link'])
		})
	return documents

def get_companies():
	comp = [name.upper() for name in companies]
	comp.sort()
	m3 = comp[0]
	comp[0] = comp[-1]
	comp[-1]=m3
	return comp

def get_summary(doc_id, item_no):
	doc_id = str(doc_id)
	item_no = "item " + str(item_no)
	with open('data/summaries_items.json','r') as f:
		data = json.load(f)
	if item_no in data[doc_id]:
		return data[doc_id][item_no]
	else:
		return "-"

def get_tables_of_doc(doc_id):
	# cmp_id is the name of json i.e. 429.json -> 429 is the input in string
	list_of_files = {}
	cmp_path = "data/table_csv/CSV/"+str(doc_id)+"/"
	for file in os.listdir(cmp_path):
		if file=="cf.csv":
			filename = cmp_path+file
			list_of_files["Cash Flows"] = read_csv(filename)
		elif file=="bs.csv":
			filename = cmp_path+file
			list_of_files["Balance Sheets"] = read_csv(filename)
		elif file=="in.csv":
			filename = cmp_path+file
			list_of_files["Income Statement"] = read_csv(filename)
	return list_of_files

def get_tables_of_doc_html(doc_id):
	# cmp_id is the name of json i.e. 429.json -> 429 is the input in string
	list_of_files = {}
	cmp_path = "data/table_csv/CSV/"+str(doc_id)+"/"
	for file in os.listdir(cmp_path):
		if file=="cf.htm":
			filename = cmp_path+file
			list_of_files["Cash Flows"] = read_csv(filename)
		elif file=="bs.htm":
			filename = cmp_path+file
			list_of_files["Balance Sheets"] = read_csv(filename)
		elif file=="in.htm":
			filename = cmp_path+file
			list_of_files["Income Statement"] = read_csv(filename)
	return list_of_files

def get_link(txt_link):
	# pass link of full txt file ex: edgar/data/320193/000032019320000096/0000320193-20-000096.txt
	html_link = txt_link.replace(".txt","-index.html")
	return "https://www.sec.gov/Archives/"+html_link

# Use to display Options for displaying Graph
graph_features = ["Assets","Liabilities","Equity","Net Income","Return on Assets","Return on Equity","Polarity of Management Discussion","Subjectivity of Management Discussion"]

def grab_features():
	# return the available options for plotting
	return graph_features

def get_plot(cmp_name, feature):
	# Pass the company name, and feature is a string from graph_features -> convert to lower:
	# {"asset","liability","equity","net income","return on assets","return on equity"}
	# returns an x,y coordinates, X-Year, Y-Value
	# Lets keep X values same for all 
	print(graph.keys())
	feature = feature.lower()
	if feature == 'polarity of management discussion' or feature == 'subjectivity of management discussion':
		return [2016,2017,2018,2019,2020], graph[cmp_name][feature]
	X = [2014,2015,2016,2017,2018,2019,2020]
	Y = graph[cmp_name][feature]
	Y.reverse()
	return X[-1*(len(Y)):],Y

def financial_summary(cmp,date_filled):
	# Input: Compnay Name, date filled
	try:
		X = [2014,2015,2016,2017,2018,2019,2020]
		date = int(date_filled.split("-")[0])
		tables = table_index[cmp]
		for t in range(len(tables)):
			if tables[t][1]==date:
			    idx=t+1
			    break
		a = graph[cmp]['assets'][idx]
		a_r = 100*(a-graph[cmp]['assets'][idx-1])/graph[cmp]['assets'][idx]
		l = graph[cmp]['liabilities'][idx]
		l_r = 100*(l-graph[cmp]['liabilities'][idx-1])/graph[cmp]['liabilities'][idx]
		e = graph[cmp]['equity'][idx]
		n = graph[cmp]['net income'][idx]
		n_r = 100*(n-graph[cmp]['net income'][idx-1])/graph[cmp]['net income'][idx]
		hl = "higher" if n_r>0 else "lower"
		hl_a = "grew by" if a_r>0 else "decreased"
		hl_l = "expanded by" if l_r>0 else "reduced by"
		roa = graph[cmp]['return on assets'][idx]
		roe = graph[cmp]['return on equity'][idx]
		summary = "In {}, {} generated a net income of ${} million. This was {:.2f}% {} than the previous year. Assets {} {:.2f}% whereas liabilities {} {:.2f}%. RoA was {:.2f}% and RoE was {:.2f}%".\
		format(date,cmp,n,n_r,hl,hl_a,abs(a_r),hl_l,abs(l_r),roa,roe)
		return summary
	except:
		return "Summary not generated, We'll be back soon."
