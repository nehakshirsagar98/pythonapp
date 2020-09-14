#Resume Phrase Matcher code

  
#importing all required libraries

import PyPDF2
import os
from os import listdir
from os.path import isfile, join
from io import StringIO
from nltk_operation import *
import pandas as pd
from collections import Counter
import spacy
normalize_sapcy = spacy.load("en_core_web_sm")
from spacy.matcher import PhraseMatcher
import matplotlib
from parsedocx import *
import textract
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import docx2txt
import docx   

matplotlib.use('Agg')
skills = "Sills :"
def sysout(msgLine,data):
    print('\n--------',msgLine,' Start ----------\n');
    print(data);
    print('\n--------',msgLine,' End ----------\n');
#function to read resume Start 
def pdfextract(file):
    # Read Pdf File 
    fileReader = PyPDF2.PdfFileReader(open(file,'rb'))
    #fileReader = PyPDF2.PdfFileReader(open(file,'w', encoding="utf-8"))
    # Check for the pages int Pdf and read all pages
    countpage = fileReader.getNumPages()
    count = 0
    text = []
    while count < countpage:    
        pageObj = fileReader.getPage(count)
        count +=1
        t = pageObj.extractText()
        #print (t)
        text.append(t)
    return text

#function to read resume ends



#function that does phrase matching and builds a candidate profile
def create_profile(file):
	filename, file_extension = os.path.splitext(file)
	print('filename: ' + filename);
	print('file_extension: ' + file_extension);
	
	if file_extension=='.pdf':
		text = pdfextract(file) 
	else:
		text = getText(file)
		
	text = str(text)
	text = text.replace("\\n", " ")
	text = text.lower()
	
	
	sysout('Input Text',text.encode("utf-8"))    
	
	#below is the csv where we have all the keywords, you can customize your own
	keyword_dict = pd.read_csv('template.csv',sep=",", encoding="iso-8859-1")
	print('template.csv readed and stored data in keyword_dict');
	sysout('keyword_dict',keyword_dict)    
	header = keyword_dict.columns
	sysout("header ",header)
	#genTFIDF(keyword_dict,header)
	collDict = {}
	#print(keyword_dict)
	for coll in header:
		collDict[coll] = [normalize_sapcy(text) for text in keyword_dict[coll].dropna(axis = 0)]
		#normalize_sapcy_words = [normalize_sapcy(text) for text in keyword_dict['normalize_sapcy'].dropna(axis = 0)]
		#ML_words = [normalize_sapcy(text) for text in keyword_dict['Machine Learning'].dropna(axis = 0)]
		#DL_words = [normalize_sapcy(text) for text in keyword_dict['Deep Learning'].dropna(axis = 0)]
		#R_words = [normalize_sapcy(text) for text in keyword_dict['R Language'].dropna(axis = 0)]
		#python_words = [normalize_sapcy(text) for text in keyword_dict['Python Language'].dropna(axis = 0)]
		#Data_Engineering_words = [normalize_sapcy(text) for text in keyword_dict['Data Engineering'].dropna(axis = 0)]
    
	sysout("collDict ",collDict)
	print('Matching sequences of tokens, based on documents using PhraseMatcher');
	#Match sequences of tokens, based on documents using PhraseMatcher
	matcher = PhraseMatcher(normalize_sapcy.vocab)
	# Add Collumns to phrase matcher wich you want to match with documents
    # the data format should be in lower case for more accurate match.
	for coll in header:
		matcher.add(coll, None, *collDict[coll])
	#matcher.add('Stats', None, *stats_words)
	#matcher.add('NLp', None, *normalize_sapcy_words)
	#matcher.add('ML', None, *ML_words)
	#matcher.add('DL', None, *DL_words)
	#matcher.add('R', None, *R_words)
	#matcher.add('Python', None, *python_words)
	#matcher.add('DataEngineering', None, *Data_Engineering_words)
	
    
	doc = preprocess(text)
	sysout('Input Text After Preprocesses',doc.encode("utf-8")) 
	doc = normalize_sapcy(doc)
	#sysout('Input Text After Applyting normalize_sapcy',doc) 
	#doc = spacy.tokens.doc.Doc(normalize_sapcy.vocab, words=doc, spaces=[False, False])
    
	global  skills 
	d = []  
	#Give document to matcher in lower case to match with the created criteria    
	matches = matcher(doc)
	print('A list of (match_id, start, end) tuples, describing the matches.');
	sysout("matches for data ",matches)
	

    #PhraseMatcher Return the 3 values :
	#A list of (match_id, start, end) tuples, describing the matches. 
	#A match tuple describes a span doc[start:end]. 
	#The match_id is the ID of the added match pattern.
    #In our case Match_Id will be collumn names of template.csv [DataEngineering, DL, ML, normalize_sapcy ]	
	for match_id, start, end in matches:
        
		rule_id = normalize_sapcy.vocab.strings[match_id]  # get the unicode ID, i.e. 'COLOR'
		span = doc[start : end]  # get the matched slice of the doc.
		#res = findTFIDF(header,span.text)
		print("TFIDF is %d ",(start)," %d ",(end)," %s ",span)
		skills = skills + span.text +","
		#print(span.text)
		d.append((rule_id, span.text))      
	keywords = ""
	
	sysout('Mathces of Input Text After Applying PhraseMatcher',d)
	
	# "\n".join(f'{i[0]} {i[1]} ({j})' for i,j in Counter(d).items())
	for i,j in Counter(d).items():
		keywords = keywords + "\n" + str(i[0]) +' ' + str(i[0]) +' (' + str(j)+")"
	
	## convertimg string of keywords to dataframe
	df = pd.read_csv(StringIO(keywords),names = ['Keywords_List'])
	df1 = pd.DataFrame(df.Keywords_List.str.split(' ',1).tolist(),columns = ['Subject','Keyword'])
	df2 = pd.DataFrame(df1.Keyword.str.split('(',1).tolist(),columns = ['Keyword', 'Count'])
	df3 = pd.concat([df1['Subject'],df2['Keyword'], df2['Count']], axis =1) 
	df3['Count'] = df3['Count'].apply(lambda x: x.rstrip(")"))
	
	base = os.path.basename(file)
	filename = os.path.splitext(base)[0]
	
	name = filename.split('_')
	name2 = name[0]
	name2 = name2.lower()
	## converting str to dataframe
	name3 = pd.read_csv(StringIO(name2),names = ['Candidate Name'])
    
	dataf = pd.concat([name3['Candidate Name'], df3['Subject'], df3['Keyword'], df3['Count']], axis = 1)
	dataf['Candidate Name'].fillna(dataf['Candidate Name'].iloc[0], inplace = True)

	return(dataf)
        
#function that does phrase matching and builds a candidate profile ends
        
#code to execute/call the above functions
def predict(filename):
	global  skills 
	skills=""
	#Function to read resumes from the folder one by one
	#mypath='./resume' #enter your path here where you saved the resumes
	#onlyfiles = [os.path.join(mypath, f) for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
	file = "./resume/"+filename
	final_database=pd.DataFrame()
	i = 0 
	#while i < len(onlyfiles):
	#	file = onlyfiles[i]
	dat = create_profile(file)
	final_database = final_database.append(dat)
	i +=1
	sysout('Final Data Extracted From Resume ',final_database)
	#print('data ',final_database)

		
	#code to count words under each category and visulaize it through Matplotlib

	final_database2 = final_database['Keyword'].groupby([final_database['Candidate Name'], final_database['Subject']]).count().unstack()
	final_database2.reset_index(inplace = True)
	final_database2.fillna(0,inplace=True)
	new_data = final_database2.iloc[:,1:]
	new_data.index = final_database2['Candidate Name']
	sysout('new_data', new_data)
	#execute the below line if you want to see the candidate profile in a csv format
	#sample2=new_data.to_csv('sample.csv')
	import matplotlib.pyplot as plt
	
	plt.rcParams.update({'font.size': 10})
	#ax = new_data.plot.barh(title="keywords by category", legend=False, figsize=(25,7), stacked=True)
	labels = []
	axis = []
	dataPlot = []
	for j in new_data.columns:
		for i in new_data.index:
			label = str(j)+" :" + str(new_data.loc[i][j])
			labels.append(label)
			axis.append(str(j))
			dataPlot.append(new_data.loc[i][j])
	#patches = ax.patches
	sysout(' Labes Extracted from Resume ',labels)
	labels.append(";"+skills)
	#print(skills)
	#print(labels)
	sysout(' Skills Extracted from Resume ',skills)
	
	#for label, rect in zip(labels, patches):
	#	width = rect.get_width()
	#	if width > 0:
	#		x = rect.get_x()
	#		y = rect.get_y()
	#		height = rect.get_height()
	#		ax.text(x + width/2., y + height/2., label, ha='center', va='center')
            
	fig = plt.figure()
	ax = fig.add_axes([0,0,1,1])
	ax.axis('equal')
	#langs = ['C', 'C++', 'Java', 'Python', 'PHP']
	#students = [23,17,35,29,12]
	ax.pie(dataPlot, labels = axis,autopct='%1.2f%%')
	#plt.show()
	imgname, file_extension = os.path.splitext(filename)
	print('final to image: ' + imgname);
	plt.savefig("./resume/"+imgname+'.png')
	return labels

print(predict('neha123.docx'))