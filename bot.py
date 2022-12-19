import slack 
import os 
import json
import re
from pathlib import Path 
from dotenv import load_dotenv
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__) # configure flask app
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'], '/slack/events', app)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
BOT_ID = client.api_call("auth.test")['user_id']

global users_votes #= {} # key, val = player, vote
global input_users #= []
global votes #= []
global estimation_method 

users_votes = {}
input_users = []
votes = []
estimation_method = ""
fib = ":one:  :two:  :three:  :five:  :eight:  :coffee:  :grey_question:"

@slack_event_adapter.on('app_mention')
def app_mention(payload):
    event = payload.get('event', {})
    type = event.get('type')
    PARTY_CHANNEL = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')

    response = "Thanks for using PokerBot! Here's how you can start your own Scrum Poker Party: \n /invite @users - invite users to a poker planning party \n /start - start the poker party"

    if BOT_ID != user_id: 
        client.chat_postMessage(channel=PARTY_CHANNEL, text=response)

@app.route('/players', methods=['POST'])
def players():
    data = request.form
    text = data.get('text').split(' ')
    channel_id = data.get('channel_id')
    for str in text:
        id = re.search('<@(.+?)\|', str)
        users_votes[id.group(1)] = 0
        input_users.append(str)
    response = ""
    print(users_votes)
    print(input_users)
    for x in input_users:
        response = response + x + "\n"
    client.chat_postMessage(channel=channel_id, text="The users joining this poker planning party are: \n" + response)
    return Response(), 200

@app.route('/method', methods=['POST'])
def method():
    data = request.form
    estimation_method = data.get('text')
    print(users_votes)
    print(input_users)
    channel_id = data.get('channel_id')
    client.chat_postMessage(channel=channel_id, text="Your estimation method is: " + estimation_method, icon_url=":coffee:")
    n = client.conversa
    #client.reactions_add(channel=channel_id, )
    return Response(), 200

@app.route('/start', methods=['POST'])
def start():
    data = request.form
    title = data.get('text')
    channel_id = data.get('channel_id')
    print(users_votes)
    print(input_users)
    users = ""
    for x in input_users:
        users = users + x + ":red_circle: \n"
    client.chat_postMessage(channel=channel_id,text= title + "\n\n" + users + "\n" + fib)
    return Response(), 200

if __name__ == "__main__":
    app.run(debug=True) # default is 5000, might have to change it to port=3001