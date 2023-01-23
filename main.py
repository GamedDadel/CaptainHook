from dotenv import load_dotenv
import discord
from discord import Intents
#from twilio.rest import Client
from discord.ext import commands
import os
import requests

load_dotenv()

digitalocean_token = os.getenv("DIGITALOCEAN_TOKEN")
discord_token = os.getenv("DISCORD_TOKEN")
my_guild = os.getenv("DISCORD_GUILD")

#discord_allowed_role_id = os.environ.get("discord_allowed_role_id")
# digitalocean_droplet_id = os.environ.get("digitalocean_droplet_id")
"""
twilio_token = os.environ.get("twilio_token")
twilio_account = os.environ.get("twilio_account")
twilio_phone_number = os.environ.get("twilio_phone_number")
user_phone_number = os.environ.get("user_phone_number")
"""
intents = Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
#twilio_client = Client(twilio_account, twilio_token)


def reboot_digitalocean():
    data = {"type": "reboot"}
    endpoint = f'https://api.digitalocean.com/v2/droplets/{digitalocean_droplet_id}/actions'
    headers = {"Authorization": f"Bearer {digitalocean_token}"}
    response = requests.post(endpoint, data=data, headers=headers)
    if (response.status_code == 201):
        print("Success")
    else:
        print(response.status_code)

def list_droplets():
    endpoint = f'https://api.digitalocean.com/v2/droplets?page=1&per_page=10'
    headers = {"Authorization": f"Bearer {digitalocean_token}", "Content-Type": "application/json"}
    response = requests.get(endpoint, headers=headers)
    if (response.status_code == 200):
        return response.text[:1950]
    else:
        return response.status_code

"""
def text_message():
    message = twilio_client.messages \
        .create(
            body = 'Check Haze Discord.', # Customize the message 
            from_ = twilio_phone_number, 
            to = user_phone_number 
        )
    return message.status
"""

@client.event
async def on_message(message):
    if message.content.startswith('^reboot'):
        author_role_ids = [y.id for y in message.author.roles]
        if int(discord_allowed_role_id) in author_role_ids:
            reboot_digitalocean()
            await message.channel.send('Rebooting...')
        else:
            print(author_role_ids)
    elif message.content.startswith('^ping'):
        author_role_ids = [y.id for y in message.author.roles]
        if int(discord_allowed_role_id) in author_role_ids:
            sms_message = text_message()
            await message.channel.send(
                f'Texting Invictus. Message status: {sms_message}' # Customize to your name
            )  
    elif message.content.startswith('^test'):
        author_role_ids = [y.id for y in message.author.roles]
        if int(discord_allowed_role_id) in author_role_ids:
            await message.channel.send('I am awake...')

    elif message.content.startswith('^list'):
        droplets = list_droplets()
        await message.channel.send(f"""```json
{droplets}
```""")
        

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == my_guild:
            break

    print(
        f"{client.user} is connected to the following guild:\n"
        f"{guild.name}(id: {guild.id})"
    )

client.run(discord_token)