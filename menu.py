import requests
import json



    
def menu():
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    data = {
      "setting_type" : "call_to_actions",
      "thread_state" : "existing_thread",
      "call_to_actions":[
        {
          "type":"postback",
          "title":"Help",
          "payload":"Try typing one of the following commands for Show release dates(R), Show Summaries(S) or Freakin Funny Fact of the Day(F)"
        },
        {
          "type":"web_url",
          "title":"Take me to SeeSo",
          "url": 'https://www.seeso.com/'
        },
        {
          "type":"postback",
          "title":"Commands",
          "payload": 'commands'
        }
      ]
    }

    menu = requests.post('https://graph.facebook.com/v2.6/me/thread_settings?access_token=EAADpiol7ZCHgBAOyg6AN32tgOVGHJsVLRnGzZAX2Q6KlxUOqYXzgLylqGwnIPKkckbYAYWLtOatI7itsFcpnYqLj0rGijdwWV3WmBtQphfmZB4QJWyqT2uKv9334Xsa969BstdyMZCgwmA2qJXDEBUx6NFfvP1YuyuAoZBjtfNwZDZD', headers=headers, data=json.dumps(data))

    print(menu.status_code)
    print(menu.json())

menu()

