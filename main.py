#import modules
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

import ssl
import urllib

# load environment variables 
load_dotenv()

# initialize flask app
app = Flask(__name__)

# connect to Twilio API
accountSid = os.getenv('TWILIO_ACCOUNT_SID')
authToken = os.getenv('TWILIO_AUTH_TOKEN')
client = Client(accountSid, authToken)


# Read in the data
def prep_data(csv_url):

	# need to open ssl to access https urls
	ssl._create_default_https_context = ssl._create_unverified_context
	urllib.request.urlopen(csv_url)

	# read dataframe from github csv url
	df = pd.read_csv(csv_url)

	# drop first column
	df.drop(["Unnamed"], axis=1, inplace=True)

	# create feature matrix
	X = pd.DataFrame(df.iloc[:,0:-1])

	# create outcome array
	y = df['y']

    # split up dataset into training and test sets
	X_train, X_test, y_train, y_test = train_test_split(X,y)

	return X_train, X_test, y_train, y_test

# train model with random forest
def train_model(X_train, y_train):
	rf = RandomForestClassifier()
	model = rf.fit(X_train, y_train)
	return model

# transpose pandas series array and transform into pandas dataframe
def transform(X_test):
	transform = pd.DataFrame(X_test).T 
	return transform

# run prediction on new row of data
def predict(model, X_test):
	pred = model.predict(X_test)
	return pred

# train model at global scope before opening web app
X_train, X_test, y_train, y_test = prep_data('https://raw.githubusercontent.com/pgomet/EmergenSeiz/main/Epileptic%20Seizure%20Recognition.csv') #open source eeg dataset for seizures
model = train_model(X_train, y_train)


@app.route('/', methods = ['GET', 'POST'])
def index():
	if request.method == 'POST':
		# get new data from button click
		if request.form.get('predict') == 'Send New Data and Run Prediction':
			n = random.randint(0,len(X_test)) # mock way of "producing" data since we lack actual BCI hardware
			X_test_transform = transform(X_test.iloc[n])
			pred = predict(model, X_test_transform)
			if pred == 1: # seizure predicted
				
				label = "High Risk of Seizure Predicted for Winnie"

				numbers_to_message = ['+18608997108', '+17817754603'] # set of phone numbers to. contact through twilio

				for number in numbers_to_message: # message each number that Winnie is at high risk of seizure
				    message = client.messages \
                        .create(
                            body='High Risk of Seizure Predicted',
                            from_= '+13133074053',
                            to = number
                        )
			else:
				label = "No Seizure Predicted"
			return render_template('index.html', variable = label) # render template with predictiono

	elif request.method == 'GET': # default template
		return render_template('index.html')

	return render_template('index.html') # default template

	
# main 
if __name__ == "__main__":
    app.run(port=5000, debug=True)