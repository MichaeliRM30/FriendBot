import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable"]

starter_encouragements = [
  "It’s hard to beat a person who never gives up.",
  "If you can't fly then run, if you can't run then walk, if you can't walk then crawl, but whatever you do you have to keep moving forward.",
  "If you're going through hell - keep going.", 
  "I believe in you. And you have to believe in you too.",
  "People care about you - even if it doesn't always seem like it.",
  "Inch by Inch, Life's a Cinch. Yard by Yard, Life is Hard",
  "If “Plan A” didn’t work. The alphabet has 25 more letters! Stay cool.", 
  "You carry so much love in your heart. Give some to yourself.",
  "Hardships often prepare ordinary people for an extraordinary destiny.",
  "It’s just a bad day not a bad life."
]

if "responding" not in db.keys():
  db["responding"] = True

def get_inspirational_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]["q"] + " - " + json_data[0]["a"]
  return(quote)

def get_stoic_quote():
  response = requests.get("https://stoic-server.herokuapp.com/random")
  json_data = json.loads(response.text)
  quote = json_data[0]["body"] + " - " + json_data[0]["author"]
  return(quote)

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragment(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
  db["encouragements"] = encouragements

@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content.lower()

  if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
  
  if message.content.startswith('$hi'):
        await message.channel.send('Wazzup!')

  if msg.startswith("$inspire"):
    quote = get_inspirational_quote()
    await message.channel.send(quote)

  if msg.startswith("$stoic"):
    quote = get_stoic_quote()
    await message.channel.send(quote)

  if db["responding"]:
    options = starter_encouragements
    if "encouragements" in db.keys():
      options.extend(db["encouragements"])

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

  if msg.startswith("$new"):
    encouraging_message = msg.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")

  if msg.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del",1)[1])
      delete_encouragment(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("$list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)
    
  if msg.startswith("$responding"):
    value = msg.split("$responding ",1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on.")
    else:
      db["responding"] = False
      await message.channel.send("Responding is off.")

keep_alive()
client.run(os.getenv("TOKEN"))