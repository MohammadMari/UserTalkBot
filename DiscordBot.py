import discord
import os
from discord.ext import commands
import random

client = commands.Bot(command_prefix=">")
class human:
    def __init__(self, countIn, randomIn, messageIn, nameIn, numWords):
        self.count = countIn
        self.random = randomIn
        self.message = messageIn
        self.name = nameIn
        self.numPhrase = numWords

homie = []

def addition_of_phrase(user,message, write):
    found = False
    for guy in homie:
        if(guy.name == str(user)):
            guy.numPhrase += 1
            guy.message.append(message)
            if write:
                f = open("PhraseSaves.txt", "a")
                f.write(str(guy.name) + " " + str(message) + "\n")
                f.close()
            found = True
    
    if not found:
        if(write):
            f = open("PhraseSaves.txt", "a")
            f.write(str(user) + " " + str(message) + "\n")
            f.close()
        homie.append(human(0,random.randint(5,10), [message], user, 1))

def removal_of_phrase(user,message, write):
    for guy in homie:
        if(guy.name == str(user)):
            for phrase in guy.message:
                if(phrase == message):
                    guy.numPhrase -= 1
                    guy.message.remove(message)
            
@client.command()
async def add (ctx, user, message):
    addition_of_phrase(user,message, True)

@client.command()
async def listp (ctx, user):
    for guy in homie:
        if guy.name == str(user):
            for phrases in guy.message:
                await ctx.send(phrases)

@client.event
async def on_message(message):
    for person in homie:
        if (person.name == "<@!" + str(message.author.id) + ">"):
            person.count += 1
            if(person.count > person.random):
                await message.channel.send(person.message[random.randint(0, person.numPhrase - 1)].format(message.author.mention))
                person.count = 0
                person.random = random.randint(15,25)

    await client.process_commands(message)

@client.event
async def on_ready():
    f = open("PhraseSaves.txt", "a")
    f.write("")
    f.close()
    f = open("PhraseSaves.txt", "r")
    Lines = f.readlines()

    for line in Lines:
        found_space = False
        rest_line = ""
        user_line = ""
        for char in range(len(line)):
            if line[char].isspace() and not found_space:
                found_space = True
            elif found_space:
                rest_line += line[char]
            else:
                user_line += line[char]
        addition_of_phrase(user_line,rest_line,False)
    f.close()
    print("Bot is ready")
    
client.run("DISCORD TOKEN")