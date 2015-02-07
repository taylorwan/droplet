from twilio.rest import TwilioRestClient 
from twilio import twiml

# put your own credentials here 
ACCOUNT_SID="AC56a6ba75f572373427231aeb66e0bc21" 
AUTH_TOKEN = "d2d16fa8f34b9b6db9fb2394b9de7901" 
  
client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 

resp = twiml.Response()


'''
client.messages.create(
	to="3017933261", 
	from_="+14433643176", 
	body="HI IT WORKS",  
)
'''

