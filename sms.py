import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

accountSid = os.getenv('TWILIO_ACCOUNT_SID')
authToken = os.getenv('TWILIO_AUTH_TOKEN')

client = Client(accountSid, authToken)

message = client.messages \
    .create(
         body='Sending from Python',
         from_= '+13133074053',
         to= '+18608997108'
     )

print(message.sid)
