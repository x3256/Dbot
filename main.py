#source code for Dbot under dev
import discord
import os
import Token
#from threading import Timer
import asyncio

cl = discord.Client()
#contributers just add your name in the list devs
devs = ["Danish"]
source_link = "https://github.com/x3256/Dbot.git"
polls = {} 

@cl.event
async def on_ready():
  print("Bot {0.user} is connected".format(cl));

@cl.event
async def on_message(msg):
  #msg_parts = msg.content.split()
  #msg_mentions = msg.mentions
  if(msg.content.startswith("$")):
    await command_parser(msg)


#utility classes


#generalized command category

class command():
  cmd = ""
  help_dis = ""
  def __init__(self,cmd,help_dis):
    self.header = cmd
    self.help_dis = help_dis

#*****************command parser *********************
async def command_parser(msg):
  msg_parts = msg.content.split()
  txt = cmds.get(msg_parts[0],None)
  if(txt != None):
    await txt["callback"](msg,msg_parts)
  elif(len(polls)>0):
    check_vote(msg,msg_parts)
  else:
    print("empty command")


#functions

#utility function to compare strings
def compare_str(a,b):
  return (a.lower() == b.lower())

#help function
async def func_help(msg,msg_parts):
  if(len(msg_parts)>1):
    if(compare_str(msg_parts[1],"list")):
      txt2 = "Available commands are"
      ctr = 1
      for i in cmds.keys():
        txt2 += "\n "+str(ctr)+" - "+i
        ctr+=1  
      await msg.channel.send(txt2)
      return

    txt = cmds.get("$"+msg_parts[1],None)
    if(txt != None):
      await msg.channel.send(txt["description"])
    else:
      await msg.channel.send(cmds["$help"]["description"])
  else:
    await msg.channel.send(cmds["$help"]["description"])


#calc function
async def func_cal(msg,msg_parts):
  #val = []
  txt = "Invalid calculations"
  val = "" 
  if(len(msg_parts)>1):
    for i in msg_parts[1:]:
      try:
        val += i+" = "+str(eval(i))+"\n"
      except:
        continue
    if(len(val)>0):
      txt = msg.author.name+"'s calculations are: \n"+ val
  else:
    txt = cmds["$cal"]["description"]
  await msg.channel.send(txt)
  
       
#bot function
async def func_bot(msg,msg_parts):
  if(len(msg_parts)>1):
    if(compare_str(msg_parts[1],"source")):
      await msg.channel.send(source_link)
    elif(compare_str(msg_parts[1],"dev")):
      await msg.channel.send("So far the developers are: \n")
      for i in devs:
        await msg.channel.send(i)
    else:
      await msg.channel.send(cmds["$bot"]["description"])
  else:
    await msg.channel.send(cmds["$bot"]["description"])

#poll funcion
async def func_poll(msg,msg_parts):
  txt = "Invalid poll"
  if(len(polls)<1):
    txt = cmds["$poll"]["description"]
    #timer length
    if(len(msg_parts)>3):
      try:
        timeout = int(msg_parts[1])
        if(timeout>(60*30)):
          await msg.channel.send("Poll duration must be less than 30 mins")
          return
      except:
        await msg.channel.send("Invalid poll command")
        return
      candids = msg.content.split(",")
      l = len(candids)
      #for identical candidates
      for i in range(l): #0 ,1 ,2
        for j in range(i+1,l,1):
          if(candids[i] == candids[j]):
            await msg.channel.send("Identical candidates")
            return
      if(l<2):
        await msg.channel.send("Cannot start for single candidate")
        return
      candids[0] = candids[0][candids[0].find(" ",6)+1:]
      reason = candids[l-1][candids[l-1].find("?")+1:]
      if(len(reason)<1):
        await msg.channel.send("Reason not specified")
        return
      candids[l-1] = candids[l-1][:candids[l-1].find("?")]
      txt = reason
      polls[0]={"candidates":candids,"votes":[0]*l,"reason":reason,"winner":"","voted":[]}
      for i in range(len(candids)):
        txt += "\nType $"+str(i+1)+" for "+ candids[i]
      txt += "\n Warning: poll will end in "+str(timeout)+"s"
  else:
    txt = "Cannot start multiple polls, maybe in future"
  await msg.channel.send(txt)
  if(len(polls)>0):
    await asyncio.sleep(2*timeout/3)
    await msg.channel.send("Hurry up only "+str(int(timeout/3))+"s left, only "+str(len(polls[0]["voted"]))+" votes so far.")
    await asyncio.sleep(timeout/3)
    await end_poll(msg,msg_parts)

def check_vote(msg,msg_parts):
  name = msg.author.name
  if(not(name in polls[0]["voted"])):
    try:
      vote = int(msg_parts[0][1:])-1
    except:
      return
    if(vote in range(len(polls[0]["candidates"]))):
      polls[0]["votes"][vote]+=1
      polls[0]["voted"].append(name)
  print(polls)
  #end_poll(msg,msg_parts)

async def end_poll(msg,msg_parts):
  global polls
  txt = "Results for poll:"+ polls[0]["reason"]
  n = len(polls[0]["votes"])
  for i in range(n):
    txt += "\n"+polls[0]["candidates"][i]+" got : "
    txt += str(polls[0]["votes"][i])
  polls = {}
  await msg.channel.send(txt)

#Create command function 
def func_create(msg,msg_parts):
  return

#list of commands
cmds= {
  "$help":{
    "description":"This is the $help command type $help <command> for further info or $help list for list of commands",
    "callback":func_help
  },

  "$poll":{
    "description":"Creates a simple poll for voting. \nUsage : $poll <timeout> <members sepated by , ? reason>",
    "callback":func_poll
  },

  "$bot":{
    "description":"Fetch info about DBOT. \nUsage: $bot <params>, params can be dev(contributers), source(link to source)", 
    "callback":func_bot
  },
  
  "$cal":{
    "description":"Can evaluate mathematical expressions.\nUsage: $cal 45/9 etc.",
    "callback":func_cal
  },

  "$create":{
    "description":"Create your own commands without programming: \nUsage: $create <name> <some text>.",
    "callback":func_create
  }

  }

cl.run(Token.TOKEN)

  

