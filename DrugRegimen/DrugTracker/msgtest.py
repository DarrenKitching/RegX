import os
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'AC73a67427b5b1c17fdc40d048672b66a4'
auth_token = 'd923a71abd421deb2882ec297c18453d'
client = Client(account_sid, auth_token)

message = client.messages \
	.create(
	 body="REMINDER - Please upload your prescription video at http://www.QRX.com.",
	 from_='+12013319681',
	 to='+353XXXXXXXXX' # replace X's with phone number to send message to.
	)