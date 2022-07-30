import numpy as np
import pandas as pd
import matplotlib as plt
import seaborn as sns
import random

from sklearn.preprocessing  import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report,confusion_matrix

from flask import request
from flask import jsonify
from flask import Flask, render_template

app = Flask(__name__)


def prep_data(csv_path):
	df = pd.read_csv(csv_path)
	df.drop(["Unnamed"], axis=1, inplace=True)
	X = pd.DataFrame(df.iloc[:,0:-1])
	y = df['y']

	X_train, X_test, y_train, y_test = train_test_split(X,y)

	return X_train, X_test, y_train, y_test

def train_model(X_train, y_train):
	rf = RandomForestClassifier()
	model = rf.fit(X_train, y_train)
	return model

def transform(X_test):
	transform = pd.DataFrame(X_test).T 
	return transform

def predict(model, X_test):
	pred = model.predict(X_test)
	return pred

X_train, X_test, y_train, y_test = prep_data('Epileptic Seizure Recognition.csv')
model = train_model(X_train, y_train)

#X_test_transform = transform(X_test.iloc[0])
#pred = predict(model, X_test_transform)

@app.route('/', methods = ['GET', 'POST'])
def index():
	if request.method == 'POST':
		if request.form.get('predict') == 'Get New Prediction':
			n = random.randint(0,len(X_test))
			X_test_transform = transform(X_test.iloc[n])
			pred = predict(model, X_test_transform)
			if pred == 1:
				label = "Seizure Predicted"
			else:
				label = "No Seizure Predicted"
			n += 1

	elif request.method == 'GET':
		return render_template('index.html')

	return render_template('index.html', variable = label)

#@app.route('/', methods = ['POST'])
#def post():


if __name__ == "__main__":
    app.run(port=5000, debug=True)