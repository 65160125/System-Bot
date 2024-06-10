import os
import discord
from discord.ext import commands
from discord import app_commands
import asyncio

from myserver import server_on

# Target user ID (replace with the actual user ID)
TARGET_CHANNEL_ID = 1249285760713232424

# Notification channel ID (replace with the actual channel ID for notifications)
NOTIFICATION_CHANNEL_ID = 1159149849539788932

intents = discord.Intents.default()
intents.members = True
intents.voice_states = True
intents.message_content = True  # Enable message content intent

bot = commands.Bot(command_prefix='/', intents=intents)

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

@bot.event
async def on_voice_state_update(member, before, after):
    # ตรวจสอบว่ามีการย้ายห้องเสียง
    if before.channel != after.channel:
        if before.channel is not None and after.channel is not None:
            notification_channel = bot.get_channel(NOTIFICATION_CHANNEL_ID)
            if notification_channel:
                await notification_channel.send(
                    f'{member.name} ถูกย้ายจากห้อง {before.channel.name} ไปยังห้อง {after.channel.name} โดย {member.guild.me.display_name}'
                )

server_on()

bot.run(os.getenv('BOT_TOKEN'))
