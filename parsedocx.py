import PyPDF2
import textract
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import docx2txt
import docx   
from test2 import * 

def getText(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    path = get_tables(filename,'\n'.join(fullText))
    f = open(path, "r")
    return f.read()

if __name__ == '__main__':
    filename='D:\\work\\project\\ResumeClassification\\rc\\resume\\neha.docx';  #docx file name
    fullText=getText(filename)
    print (fullText)
