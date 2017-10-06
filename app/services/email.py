import requests
from app.services.config import MAILGUN
from django.template.loader import render_to_string

def send(sender, recipient, subject, html = None, view = None):
	"""
	Send an email message
	
	Arguments:
		sender {String} -- From Email Address
		recipient {String|List} -- To Email Address(es)
		subject {String} -- Email subject
		html {String} -- Email html
		view {Object} -- Template view with data
	
	Returns:
		Mixed -- HTTP Response
	"""

	# build up the view string
	if html:
		view_string = html
	elif view:
		view_string = render_to_string(view['name'], view['data'])
	else:
		raise ValueError("Requires email message to be present!")

	# check recipient
	if isinstance(recipient, str):
		recipient = [ recipient ]
		print recipient

	return requests.post(
        "https://api.mailgun.net/v3/%s/messages" % MAILGUN['domain'],
        auth=("api", MAILGUN['api_key']),
        data={"from": sender,
              "to": recipient,
              "subject": subject,
              "text": view_string}
    )
