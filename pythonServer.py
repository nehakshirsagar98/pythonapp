from flask import Flask
from sklearn.ensemble import RandomForestClassifier
import pickle
from ResumeClassify import *
app = Flask(__name__)
#input filename no extension

@app.route('/')
def index():
    return "No Data Forwarded"

@app.route('/<filename>')
def predictAttrition(filename):
    print(filename)
    result = predict(filename)
    return "{}".format(result)

if __name__ == '__main__':
    app.run(host= '0.0.0.0')