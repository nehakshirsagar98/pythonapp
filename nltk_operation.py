from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk import pos_tag
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from nltk import word_tokenize, pos_tag, ne_chunk
import re
import pickle
from nltk.corpus import stopwords 
import spacy
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
nlp = spacy.load("en_core_web_sm")
def Lemmatizer(input_word,pos_tag):
    lemmatiser = WordNetLemmatizer()
    #print(lemmatiser.lemmatize(input_word, pos=pos_tag))
    return lemmatiser.lemmatize(input_word, pos=pos_tag)
def word_tokens(text):
	clean_text = text.replace('\n','').replace('\t','').replace('  ',' ')
	return word_tokenize(clean_text)  
def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None # for easy if-statement 
def get_synonyms(word): 
    syns = wordnet.synsets("program") 
    # An example of a synset: 
    #print(syns) 
    list=[]
    i=1
    for lemmavalue in syns:
        list.insert(i,lemmavalue.lemmas()[0].name())
        i=i+1
        #list.insert(i,fm)
    # Just the word: 
    #print(syns[0].lemmas()[0].name()) 
    # Definition of that first synset: 
    #print(syns[0].definition()) 
    # Examples of the word in use in sentences: 
    #print(syns[0].examples()) 
    return list
def pos_tagging(input_data):
    tokens = word_tokenize(input_data) # Generate list of tokens
    tokens_pos = pos_tag(tokens) 
    #print("POS Tag :"+str(tokens_pos))
    return tokens_pos;

def Lemmatizer_Sentence(input_sentence):
    output_str="";
    lemmatizer = WordNetLemmatizer()
    tagged=pos_tagging(input_sentence)
    for word, tag in tagged:
        wntag = get_wordnet_pos(tag)
        if wntag is None:# not supply tag in case of None
            output_str+= " "+lemmatizer.lemmatize(word) 
        else:
            output_str+= " "+lemmatizer.lemmatize(word, pos=wntag)
    #print("Lemmatizing Sentence :"+str(output_str))
    return output_str
    
def removeStopWords(text):
    stop_words = set(stopwords.words('english')) 
    word_tokens = word_tokenize(text) 
    filtered_sentence = [w for w in word_tokens if not w in stop_words] 
    output_sentense = ""
    for w in word_tokens: 
        if w not in stop_words: 
            output_sentense += w+" " 
    return output_sentense
    
def NER_Chunker(sentence):
    ners=ne_chunk(pos_tag(word_tokenize(sentence)))
    output_str="";
    for chunk in ners:
        if hasattr(chunk, 'label'):
            data=chunk.label(), ' '.join(c[0] for c in chunk)
            output_str+=data[0]+"_"+data[1]+","
    return output_str
   
def genTFIDF(keyword_dict,header):
    keyword_dict = keyword_dict.dropna()
    for col_name in header:
        count_vect = CountVectorizer(max_features=1)
        count_model = count_vect.fit(keyword_dict[col_name])
        keyword_dict.dropna()
        counts  = count_model.transform(keyword_dict[col_name])
        transformer = TfidfTransformer().fit(counts)
        counts = transformer.transform(counts)
        pickle.dump(transformer, open("TfidfTransformer_"+col_name, 'wb'))
        pickle.dump(count_model, open("CountVectorizer_"+col_name, 'wb'))
def findTFIDF(header,text):
    output = []
    #import pdb
    for coll_name in header:
        transformer = pickle.load(open("TfidfTransformer_"+coll_name, 'rb'))
        count_model = pickle.load(open("CountVectorizer_"+coll_name, 'rb'))
        test = word_tokenize(text)
        test = ' '.join(test)
        print(test)
        counts1  = count_model.transform([test])
        counts = transformer.transform(counts1)
        #pdb.set_trace()
        print(counts)
        output.append(counts)
    return output
def preprocess(text):
    text = Lemmatizer_Sentence(text)
    text = re.sub(r'^https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
    text = text.replace('@', " ")
    text = text.replace('#', " ")
    text = text.replace('\\', " ")
    text = text.replace('/', " ")
    text = text.replace(',', " ")
    text = removeStopWords(text)
    return text
    
''' 
print("----------------Input Question----------------")
stentence="How a Pentagon deal became an identifying  crisis for Google"
print(stentence)
print("----------------POS tagging----------------")
print(preprocess(stentence))
#print("----------------POS tagging----------------")
#print(pos_tagging(stentence))
'''