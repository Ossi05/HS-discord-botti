import requests
from bs4 import BeautifulSoup
import discord

intents = discord.Intents.all()
intents.members = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.content.startswith('!uutiset'):
        url = 'https://www.hs.fi/rss/tuoreimmat.xml'
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'xml')
            articles = soup.findAll('item')[:5]  # Näyttää 5 artikkelia
            if articles:
                for article in articles:
                    title = article.title.text
                    link = article.link.text
                    message_text = f'{title}\n{link}\n\n'
                    await message.channel.send(message_text)
            else:
                await message.channel.send('Uutisia ei löytynyt')
        except requests.exceptions.RequestException as e:
            await message.channel.send(f'Pyyntö epäonnistui: {e}')

bot_token = "" #Botin tokeni tähän
client.run(bot_token)
