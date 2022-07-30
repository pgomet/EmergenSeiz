var twilio = require('twilio');

// Find your account sid and auth token in your Twilio account Console.
var client = new twilio('TWILIO_ACCOUNT_SID', 'TWILIO_AUTH_TOKEN');

// Send the text message.
client.messages.create({
  to: 'YOUR_NUMBER',
  from: 'YOUR_TWILIO_NUMBER',
  body: 'Hello from Twilio!'
});