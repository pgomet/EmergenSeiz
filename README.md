# EmergenSeiz

## Overview
For our submission for [NatHacks 2022](https://neuralberta.tech/event/nathack), we thought to ourselves "how can we make a safer world for people with seizures?" As individuals impacted by seizures or with loved ones impacted by seizures, we understand how scary it can be to be alone when prone to seizures or to be away from someone at risk. Seizures are a serious health problem which can result in up to fatal injuries if adequate care is not in place.

The theme of the hackathon was brain-computer interfaces (BCI), but since we did not have BCI hardware, we based our project on an open source dataset from the [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/Epileptic+Seizure+Recognition) that contains EEG (electroencephalogram) data of seizure and non-seizure activity. We trained a random forest model on this dataset to predict if someone was at imminent risk of a seizure. This was connected to a web app where individuals could see their current predicted state and also add phone numbers to receive text messages through the Twilio API. These phone numbers could be themselves, people close to them, etc. -- anyone who would they like to have know about their risk. 

A button is present on the web app to mock collecting data from a sensor and producing a "real-time" prediction since we did not have any BCI hardware. It effectively pulls a random row from our test dataset.

This was a very fun hackathon to do, and if we were to continue working on it we would expand it into a mobile app or smartwatch app and hopefully get access to real BCI hardware to test with!