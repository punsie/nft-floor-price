import asyncio
import requests
import discord
import os

from discord import (
    Activity,
    ActivityType,
    Client,
    errors,
)
from datetime import datetime as dt

################################################################################
# Your bot's token goes here. This can be found on the Discord developers
# portal.
################################################################################
BOT_TOKEN = os.environ['DISCORD_BOT_TOKEN']
################################################################################

print('\n---------- V² DISCORD x PASSAGE MARKETPLACE BOT ----------\n')

################################################################################
# Sanity check for PASSAGE API
################################################################################
print(f'{dt.utcnow()} | Checking Passage marketplace for floor price.')
r = requests.get(f'https://market-api.passage3d.com/v1/nft/getNFTs?sortBy=price&sortOrder=asc&page=1&collectionName=62c704b5eaf81634ad1a1c90')
if r.status_code > 400:
    print(f'{dt.utcnow()} | Could not reach API. Exiting...\n')
    exit()
else:
    floor_price = r.json()['nftsWithFilteredDetails'][0]['price']
    floor_price = str(round((int(floor_price)/1000000),1)) + ' ATOM'
    print(f'{dt.utcnow()} | Found {floor_price}.')

################################################################################
# Start client.
################################################################################
print(f'{dt.utcnow()} | Starting Discord client.')
client = discord.Client(intents=discord.Intents.default())
################################################################################


################################################################################
# Client's on_ready event function. We do everything here.
################################################################################
@client.event
async def on_ready():
    errored_guilds = []
    await client.change_presence(
        activity=Activity(
            name=f'Kira',
            type=ActivityType.watching,
        ),
    )
    print(f'{dt.utcnow()} | Discord client is running.\n')
    while True:
        try:
            price = requests.get(
                f'https://market-api.passage3d.com/v1/nft/getNFTs?sortBy=price&sortOrder=asc&page=1&collectionName=62c704b5eaf81634ad1a1c90'
            ).json()['nftsWithFilteredDetails'][0]['price']
            for guild in client.guilds:
                try:
                    await guild.me.edit(
                        nick=f'{floor_price}'
                    )
                except errors.Forbidden:
                    if guild not in errored_guilds:
                        print(f'{dt.utcnow()} | {guild}:{guild.id} hasn\'t set '
                              f'nickname permissions for the bot!')
                    errored_guilds.append(guild)
                except Exception as e:
                    print(f'{dt.utcnow()} | Unknown error: {e}.')
        except requests.exceptions.HTTPError as e:
            print(f'{dt.utcnow()} | HTTP error: {e}.')
        finally:
            await asyncio.sleep(1500)
################################################################################

################################################################################
# Run the client.
################################################################################
client.run(BOT_TOKEN)
################################################################################
