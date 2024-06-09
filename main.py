import os
import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import random  # Import the random module
from myserver import server_on

# Target user ID (replace with the actual user ID)
TARGET_USER_ID = 767056525708492840

# Target text channel ID (replace with the actual channel ID)
TARGET_CHANNEL_ID = 1249285760713232424

intents = discord.Intents.default()
intents.members = True
intents.voice_states = True
intents.message_content = True  # Enable message content intent

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f"Bot {bot.user} is online!")
    await bot.tree.sync()
    print("Commands synced")

@bot.event
async def on_voice_state_update(member, before, after):
    if member.id == TARGET_USER_ID and after.channel:
        await asyncio.sleep(random.randint(1, 10))  # Wait for a random number of seconds between 1 and 10
        if member.voice and member.voice.channel:
            await member.move_to(None)  # Disconnect the user from the voice channel

@bot.tree.command(name='hellobot', description='ไว้ให้บอททักทาย')
async def hellocommand(interaction: discord.Interaction):
    await interaction.response.send_message("Hello กูเป็นบอทของเซิฟซิสเต้ม")

@bot.tree.command(name='name', description='ไว้ให้บอททักทายแต่มีชื่อด้วย')
@app_commands.describe(name="คุณชื่ออะไร ?")
async def namecommand(interaction: discord.Interaction, name: str):
    await interaction.response.send_message(f"หวัดดีไอ{name}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # Ignore messages from the bot itself

    # Check if the message is in the target channel
    if message.channel.id == TARGET_CHANNEL_ID:
        mes = message.content
        if mes == 'สวัสดี':
            await message.channel.send("สวัสดีจ้า " + str(message.author.name))
        else:
            await message.channel.send("เราเพิ่งถูกพึ่งสร้างวันนี้ อย่าคาดหวังให้มันพิมพ์อะไรเยอะสิ อีกอย่าง เราไม่ใช่ Ai ด้วย !!!")

server_on()

bot.run(os.getenv('BOT_TOKEN'))
