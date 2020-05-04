import discord
import asyncio
import requests
import string
from lxml import html
from googlesearch import search
from bs4 import BeautifulSoup

TOKEN = 'NzA2OTAzMzI1Mjg2NzI3NzEw.XrBE4A.8cPcUJ2-9g4B1Ac3k0phr-nPXRs'
client = discord.Client()
# client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    try:
        result = await chatbot_query(message.content[7:])
    except Exception as e:
        result = ""
        print (e)

    if message.content.startswith('!google'):
        msg = result
        #msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('Hi'):
        msg = 'Hey'
        #msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def chatbot_query(query, index=0):
    fallback = 'Sorry, I cannot think of a reply for that.'
    result = ''
    result_list = []

    try:
        for j in search(query, tld="co.in", num=10, stop=10, pause=2): 
            result_list.append(j) 

        search_result_list = list(search(query, tld="co.in", num=10, stop=3, pause=1))

        page = requests.get(search_result_list[index])

        tree = html.fromstring(page.content)

        soup = BeautifulSoup(page.content, features="lxml")

        article_text = ''
        article = soup.findAll('p')
        for element in article:
            article_text += '\n' + ''.join(element.findAll(text = True))
        article_text = article_text.replace('\n', '')
        first_sentence = article_text.split('.')
        first_sentence = first_sentence[0].split('?')[0]

        chars_without_whitespace = first_sentence.translate(
            { ord(c): None for c in string.whitespace }
        )

        if len(chars_without_whitespace) > 0:
            result = first_sentence
        else:
            result = fallback
        result_list.append(result)
        return result_list
    except:
        if len(result) == 0: result = fallback
        return result

client.run(TOKEN)


