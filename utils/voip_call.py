'''Script that makes a VoIP call
Put this script into /home/homeassistant/.homeassistant
Use it as shell_command in configuration.yaml (python voip_call.py)
'''

import sys
# CHANGE THIS TO MATCH YOUR EXISTING VIRTUAL ENVIRONMENT
# Import virtual environment
sys.path.insert(0, '/srv/homeassistant/lib/python3.11/site-packages')
#####################################################################
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

# Twilio Account credentials
account_sid = ''
auth_token = ''

# Message to play on call
msg_content = 'Office Alarm'
from_number = ''
recipients = ['']
tts_language = 'Carla'

client_conn = Client(account_sid, auth_token)

try:
    for recipient in recipients:
        client_conn.calls.create(
            to=recipient,
            from_=from_number,
            twiml=f"""
            <Response>
                <Say voice='Polly.{tts_language}'>{msg_content}</Say>
            </Response>""",
        )
except TwilioRestException as e:
    print(str(e))
    raise ProviderError() from e
