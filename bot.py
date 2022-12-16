import slack 
import os 
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
PARTY_CHANNEL = ''
players = {} # players and their votes

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

@app.route('/start', methods=['POST'])
def start():
    data = request.form
    res = client.views_open(
        trigger_id=data["trigger_id"], 
        view={
            "title": {
                "type": "plain_text",
                "text": "Planning Poker Party"
            },
            "submit": {
                "type": "plain_text",
                "text": "Submit"
            },
            "blocks": [
                {
                    "type": "section",
                    "block_id": "section678",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Pick users from the list"
                    },
                    "accessory": {
                        "action_id": "text1234",
                        "type": "multi_users_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select users"
                        }
                    }
                },
                {
                    "type": "input",
                    "element": {
                        "type": "radio_buttons",
                        "options": [
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Fibonacci",
                                    "emoji": True
                                },
                                "value": "1"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "T-shirt sizes",
                                    "emoji": True
                                },
                                "value": "2"
                            }
                        ]
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Estimation Method"
                    },
                    "hint": {
                        "type": "plain_text",
                        "text": "Hint text"
                    }
                }
            ],
            "type": "modal",
            "callback_id": "modal-identifier"
        }
    )
    return Response(), 200

@app.route('/make-room', methods=['POST'])
def make_room():
    data = request.form
    print(request.form['payload'])
    print(PARTY_CHANNEL)
    #client.chat_postMessage(channel=, text="Party created: ")
    return Response(), 200


if __name__ == "__main__":
    app.run(debug=True) # default is 5000, might have to change it to port=3001