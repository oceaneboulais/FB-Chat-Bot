from django.shortcuts import render
from django.views import generic
from django.http.response import HttpResponse
from pprint import pprint
import json, requests, random, re
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from fb_seesobot.bot import Bot

#from requests_toolbelt import MultipartEncoder
#from pymessenger.graph_api import FacebookGraphApi
#import pymessenger.utils as utils

class Element(dict):
    __acceptable_keys = ['title', 'item_url', 'image_url', 'subtitle', 'buttons']
    def __init__(self, *args, **kwargs):
        kwargs = {k:v for k, v in kwargs.items() if k in self.__acceptable_keys}
        super(Element, self).__init__(*args, **kwargs)

payloads = {'commands': 'Say any of the following key words to get the scoop on SeeSo: Show Release Dates(R), Show Summaries(S), Freakin\' Funny Fact of the Day (F)'}
inputs = {
	'hey': [ """Welcome to SeeSo! Say 'commands' to get chatting!"""],	
        'yo': ["""mama! Jk. Say 'commands' to get chatting!"""],
        'help': ["""Try saying 'commands'!"""],
        'snl': ["""A late-night comedy show featuring several short skits, parodies of television commercials, a live guest band, and a pop-cultural guest host each week."""],
         
        'flowers': ["""The eccentric Flowers family are struggling to hold themselves together. Maurice Flowers (Barratt) is the author of the twisted children's books "The Grubbs", he and his wife Deborah (Colman) are barely together but yet to divorce."""],
    
        'thingstarter': ["""A young startup company creates ridiculous products that users have submitted and the community has voted on. They then conduct focus groups on real, unwitting consumers and professionals."""],

        'hidden': ["""A comedic take on the travel show that follows comedian Jonah Ray on his misadventures as he travels from city to city visiting neighborhood hot spots, meeting local heroes and tasting the cuisine."""],

        'bajillion': ["""This Seeso original series follows Platinum Realty, Los Angeles' premiere realty group. A group of realtors must compete for a partner postion in the firm by selling as much property as possible."""],

        'commands': ["""Say any of the following key words to get the scoop on SeeSo: Show Release Dates(R), Show Summaries(S), Freakin' Funny Fact of the Day (F)"""],

        'r': ["""'Gentlemen Lobsters' 6.16 \n'Night Train with Wyatt Cenac' 6.30 \n'HarmonQuest' 7.14"""],

        's': ["""Say snl, flowers, thingstarter, hidden, or bajillion for a brief summmary on our top shows at SeeSo!"""],

        'f': ["""Dan Harmon, co-creator of Rick&Morty and HarmonQuest,started playing Dungeons and Dragons for the first time when he was 13 years old."""]

          }



# Create your views here.
class SeeSoBotView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == '00768521308x':    
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)
    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events 
                if 'message' in message:
                    attachment = 1
                    for k, v in message.items():
                        try:                    
                            for key, value in v.items():
                                if type(value) == list:
                                   attachment = 2
                        except:
                            pass
                    pprint(message)
                    if attachment == 2:
                        fbid = message['sender']['id']
                        user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid
                        user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':'EAADpiol7ZCHgBAOyg6AN32tgOVGHJsVLRnGzZAX2Q6KlxUOqYXzgLylqGwnIPKkckbYAYWLtOatI7itsFcpnYqLj0rGijdwWV3WmBtQphfmZB4QJWyqT2uKv9334Xsa969BstdyMZCgwmA2qJXDEBUx6NFfvP1YuyuAoZBjtfNwZDZD'}
                        user_details = requests.get(user_details_url, user_details_params).json()
                        bot_response = 'Hey I didn\'t understand that, trying again.'
                        post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=EAADpiol7ZCHgBAOyg6AN32tgOVGHJsVLRnGzZAX2Q6KlxUOqYXzgLylqGwnIPKkckbYAYWLtOatI7itsFcpnYqLj0rGijdwWV3WmBtQphfmZB4QJWyqT2uKv9334Xsa969BstdyMZCgwmA2qJXDEBUx6NFfvP1YuyuAoZBjtfNwZDZD'
                        response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":'Sorry! I didn\'t catch that.'}})
                        status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
                        post_facebook_message(message['sender']['id'],'Attachment')
                    # Print the message to the terminal
                    else:
                        post_facebook_message(message['sender']['id'], message['message']['text'])
                    pprint(message)

                elif 'postback' in message:
                    payload = message['postback']['payload']
                    fbid = message['sender']['id']
                    if payload in payloads:
                        inputs_text = str(payloads[payload])
                        response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":inputs_text}})
                        post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=EAADpiol7ZCHgBAOyg6AN32tgOVGHJsVLRnGzZAX2Q6KlxUOqYXzgLylqGwnIPKkckbYAYWLtOatI7itsFcpnYqLj0rGijdwWV3WmBtQphfmZB4QJWyqT2uKv9334Xsa969BstdyMZCgwmA2qJXDEBUx6NFfvP1YuyuAoZBjtfNwZDZD'
                        status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
                    pprint(status.json())

        return HttpResponse()

def post_facebook_message(fbid, recevied_message):           
    # Remove all punctuations, lower case the text and split it based on space
    tokens = re.sub(r"[^a-zA-Z0-9\s]",' ',recevied_message).lower().split()
    inputs_text = ''
    for token in tokens:
        if token in inputs:
            inputs_text = random.choice(inputs[token])
            break
        elif not inputs_text:
            inputs_text = "I didn't understand! Send 'SNL', 'flowers', 'thingstarter','hidden america','bajillion dollar propertie$' for a quick summary of these SeeSo shows!"  
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=EAADpiol7ZCHgBAOyg6AN32tgOVGHJsVLRnGzZAX2Q6KlxUOqYXzgLylqGwnIPKkckbYAYWLtOatI7itsFcpnYqLj0rGijdwWV3WmBtQphfmZB4QJWyqT2uKv9334Xsa969BstdyMZCgwmA2qJXDEBUx6NFfvP1YuyuAoZBjtfNwZDZD'
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":inputs_text}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())

