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
async def on_voice_state_update(member, before, after):
    # ตรวจสอบว่ามีการย้ายห้องเสียง
    if before.channel != after.channel:
        if before.channel is not None and after.channel is not None:
            # Get the member's previous and current channels
            before_channel = before.channel
            after_channel = after.channel
            
            # Check for recent audit logs to find out who moved the member
            async for entry in member.guild.audit_logs(limit=1, action=discord.AuditLogAction.member_move):
                if entry.target and isinstance(entry.target, discord.Member) and entry.target.id == member.id:
                    mover = entry.user
                    notification_channel = bot.get_channel(NOTIFICATION_CHANNEL_ID)
                    if notification_channel:
                        await notification_channel.send(
                            f'{member.name} ถูกย้ายจากห้อง {before_channel.name} ไปยังห้อง {after_channel.name} โดย {mover.name}'
                        )
                    break

server_on()

bot.run(os.getenv('BOT_TOKEN'))
