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

import os
from dotenv import load_dotenv
from twilio.rest import Client

# load environment variables 
load_dotenv()

# initialize flask app
app = Flask(__name__)

# connect to Twilio API
accountSid = os.getenv('TWILIO_ACCOUNT_SID')
authToken = os.getenv('TWILIO_AUTH_TOKEN')

client = Client(accountSid, authToken)


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
		if request.form.get('predict') == 'Send New Data and Run Prediction':
			n = random.randint(0,len(X_test))
			X_test_transform = transform(X_test.iloc[n])
			pred = predict(model, X_test_transform)
			if pred == 1:
				
				label = "High Risk of Seizure Predicted for Winnie"

				numbers_to_message = ['+18608997108', '+17817754603']

				for number in numbers_to_message:
				    message = client.messages \
                        .create(
                            body='High Risk of Seizure Predicted',
                            from_= '+13133074053',
                            to = number
                        )
			else:
				label = "No Seizure Predicted"
			return render_template('index.html', variable = label)
			n += 1

	elif request.method == 'GET':
		return render_template('index.html')

	return render_template('index.html')

	

#@app.route('/', methods = ['POST'])
#def post():


if __name__ == "__main__":
    app.run(port=5000, debug=True)