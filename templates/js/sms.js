require('dotenv').config();
const accountSid = process.env.TWILIO_ACCOUNT_SID;
const authToken = process.env.TWILIO_AUTH_TOKEN;
const Twilio = require('twilio');
const client = new Twilio(accountSid, authToken);

client.messages
  .create({
     body: 'Hign risk of seizure predicted!',
     from: '+13133074053',
     to: '+18608997108'
   })
  .then(message => console.log(message.sid));