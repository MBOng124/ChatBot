import os, slackclient, time
import random

#delay in seconds before checking for new events
SOCKET_DELAY = 1
#SLACK ENVIRONMENT VARIABLES
VALET_SLACK_NAME = os.environ.get('VALET_SLACK_NAME')
VALET_SLACK_TOKEN = os.environ.get('VALET_SLACK_TOKEN')
VALET_SLACK_ID = os.environ.get('VALET_SLACK_ID')
valet_slack_client = slackclient.SlackClient(VALET_SLACK_TOKEN)
def is_private(event):
	"""checks if event is a private slack channel"""
	return event.get('channel').startswith('D')

def is_for_me(event):
	"""checking if message is for me"""
	type = event.get('type')
	if type and type == 'message' and not (event.get('user')==VALET_SLACK_ID) :
		if is_private(event):
			return True
		text = event.get('text')
		channel = event.get('channel')
		if valet_slack_mention in text.strip().split():
			return True
def handle_message(message, user, channel):
	if is_hi(message):
		user_mention = get_mention(user)
		post_message(message=say_hi(user_mention), channel=channel)
	elif is_bye(message):
		user_mention = get_mention(user)
		post_message(message=say_bye(user_mention), channel=channel)
def post_message(message, channel):
	valet_slack_client.api_call('chat.postMessage', channel=channel,
					text=message, as_user=True)
def is_hi(message):
	tokens = [word.lower() for word in message.strip().split()]
	return any(g in tokens
			for g in ['hello', 'bonjour', 'nihao', 'hi', 'hey', 'yo', 'how are you', 'sup', 'morning', 'evening', 'afternoon', 'hi there'])

def is_bye(message):
	tokens = [word.lower() for word in message.strip().split()]
	return any(g in tokens
			for g in ['bye', 'goodbye', 'adios', 'later', 'till next time', 'farewell'])
def say_hi(user_mention):
	"""Says hi to the user by formatting their mention"""
	response_template = random.choice(['Sup, {mention}...',
										'Yo! {mention}',
										'Ni hao'])
	return response_template.format(mention=user_mention)
def say_bye(user_mention):
	"""Says goodbye to the user"""
	response_template = random.choice(['See you later drunken beever',
										'Bye, {mention}',
										'Godspeed'])
	return response_template.format(mention=user_mention)
def run() :
	if valet_slack_client.rtm_connect():
		print('[.] Starter bot is ready to troll')
		while True:
			event_list = valet_slack_client.rtm_read()
			if len(event_list) > 0:
				for event in event_list:
					if is_for_me(event):
						handle_message(message=event.get('text'), user=event.get('user'), channel=event.get('channel'))
			time.sleep(SOCKET_DELAY)
	else:
		print('[!] Connection Failed.')
		
def get_mention(user):
	return '<@{user}>'.format(user=user)
	
valet_slack_mention = get_mention(VALET_SLACK_ID)

if __name__=='__main__':
	run()