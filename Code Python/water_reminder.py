import datetime
from pushbullet import Pushbullet
import random

##Using the Pushbullet API


API_KEY = "o.JsVONJAs0PScc4C8fNPyeYMSee5O7LXf"

file = 'Reminder to Drink Water.txt'

# Read all the quotes from the text file
with open(file, mode='r') as f:
    quotes = [line.strip() for line in f if line.strip()]

#Making sure that the list is not empty
if not quotes:
    raise ValueError("The quotes file is empty.")

#Get the current hour of the day
current_hour = datetime.datetime.now().hour

#Push a quote at each time of the day

if 5 <= current_hour < 12 and len(quotes) > 0:
    #Morning quote
    quote = random.choice(quotes)
elif 12 <= current_hour < 18 and len(quotes) > 1:
    #Afternoon quote
    quote = random.choice(quotes)
elif 18 <= current_hour < 22 and len(quotes) > 2:
    #Evening quote
    quote = random.choice(quotes)
else:
    # Night quote 
    quote = random.choice(quotes)  

pb = Pushbullet(API_KEY)

# Send the notification
title = "A Gentle Reminder to Drink Water"
push = pb.push_note(title, quote)