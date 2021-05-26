from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from wtforms import Form, TextAreaField, validators
from werkzeug.utils import secure_filename
import pickle
import sqlite3
import os
import numpy as np
import pandas as pd 
import csv
from sklearn.externals import joblib
from keras.preprocessing.sequence import pad_sequences
loaded_model=joblib.load("./pkl_objects/model.pkl")
loaded_stop=joblib.load("./pkl_objects/stopwords.pkl")
loaded_tokenizer=joblib.load("./pkl_objects/tokenizer.pkl")

app = Flask(__name__)

# UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '\\uploads\\'
UPLOAD_FOLDER = 'C:\\Users\\Administrator\\Desktop\\Sem 4\\NLP\\assignment\\toxicCommentClassifier\\uploads\\'

ALLOWED_EXTENSIONS = {'csv'}
def allowed_file(filename):
   return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class ReviewForm(Form):
    comment = TextAreaField('',[validators.DataRequired()])

@app.route('/', methods=['GET', 'POST'])
def index():
   form = ReviewForm(request.form)
   # return render_template('upload.html', form=form) 
   if request.method == 'POST':
       if 'file' not in request.files:
           print('No file attached in request')
           return redirect(request.url)
       file = request.files['file']
       if file.filename == '':
           print('No file selected')
           return redirect(request.url)
       if file and allowed_file(file.filename):
           filename = secure_filename(file.filename)
           file.save(os.path.join(UPLOAD_FOLDER, filename))
           process_file(os.path.join(UPLOAD_FOLDER, filename), filename)
           return redirect(url_for('uploaded_file', filename=filename))
   # return render_template('upload.html')
   return render_template('upload.html', form=form) 

DOWNLOAD_FOLDER = 'C:\\Users\\Administrator\\Desktop\\Sem 4\\NLP\\assignment\\toxicCommentClassifier\\downloads\\'

def classify(userInput):
    tokenlist = []
    tokenlist.append(userInput)
    loaded_tokenizer.fit_on_texts(tokenlist)
    input_sequences = loaded_tokenizer.texts_to_sequences(tokenlist)
    userinput_data = pad_sequences(input_sequences, maxlen=250)
    y = loaded_model.predict(userinput_data)
    return y

def process_file(path, filename):
   classifier(path, filename)

def classifier(path, filename):
   inputlist = []
   toxicComm = []
   severeToxicComm = []
   obsceneComm = []
   threatComm = []
   insultComm = []
   identityHateComm = []
   with open(path,'r',encoding='utf-8-sig') as csv_file:
       csv_reader = csv.reader(csv_file)
       for line in csv_reader:
           # print(line)
           # for i in line[1:]:
           #     print(i)
           inputlist.append(line[1])
       print(inputlist)
       for comment in inputlist:
           category = classify(comment)
           percentage = []
           for eachperc in category[0]:
               # print(eachperc)
               percentage.append(eachperc)
           toxicComm.append(str(np.round(percentage[0]*100, 2)))
           severeToxicComm.append(str(np.round(percentage[1]*100, 2)))
           obsceneComm.append(str(np.round(percentage[2]*100, 2)))
           threatComm.append(str(np.round(percentage[3]*100, 2))) 
           insultComm.append(str(np.round(percentage[4]*100, 2))) 
           identityHateComm.append(str(np.round(percentage[5]*100, 2)))        
           # print(toxicComm)
       csv_file.close() 
   
   with open(DOWNLOAD_FOLDER + filename,'w', newline='',encoding='utf-8-sig') as close_csv:
       wr = csv.writer(close_csv)
       fields = ['Comment', 'Toxic', 'Severe Toxic', 'Obscene', 'Threat', 'Insult', 'Identity Hate']
       wr.writerow(fields)
       for eachinfo in range(len(inputlist)):
           info = []
           info.append(inputlist[eachinfo])
           info.append(toxicComm[eachinfo])
           info.append(severeToxicComm[eachinfo])
           info.append(obsceneComm[eachinfo])
           info.append(threatComm[eachinfo])
           info.append(insultComm[eachinfo])
           info.append(identityHateComm[eachinfo])
           wr.writerow(info)
       close_csv.close()

   
@app.route('/uploads/<filename>')
def uploaded_file(filename):
   return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

@app.route('/results', methods=['POST'])
def results():
    form = ReviewForm(request.form)
    if request.method == 'POST' and form.validate():
        review = request.form['comment']
        y = classify(review)
        percentage = []
        for i in y[0]:
            print(i)
            percentage.append(i)
            
        toxicComm = "Toxic : " + str(np.round(percentage[0]*100, 2))
        severe_toxicComm = "Severe Toxic : " + str(np.round(percentage[1]*100, 2))
        obsceneComm = "Obscene : " + str(np.round(percentage[2]*100, 2))
        threatComm = "Threat : " + str(np.round(percentage[3]*100, 2))
        insultComm = "Insult : " + str(np.round(percentage[4]*100, 2))
        identity_hateComm = "Identity hate : " + str(np.round(percentage[5]*100, 2))
        return render_template('results.html', content=review, toxic=toxicComm, severe=severe_toxicComm, obscene=obsceneComm, threat=threatComm, insult=insultComm, identityHate=identity_hateComm )
        return render_template('upload.html', form=form)


if __name__ == '__main__':
    # app.run(host='0.0.0.0',port=50000, debug=False)
    app.run(debug=False,threaded=False)
