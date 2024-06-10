import os
import discord
from discord.ext import commands
import asyncio

from myserver import server_on

# รหัสช่องแจ้งเตือน (แทนที่ด้วยรหัสช่องจริง)
NOTIFICATION_CHANNEL_ID = 1159149849539788932

intents = discord.Intents.default()
intents.members = True
intents.voice_states = True
intents.message_content = True  # เปิดการใช้งาน intent การเนื้อหาข้อความ

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_voice_state_update(member, before, after):
    # ตรวจสอบว่ามีการย้ายห้องเสียง
    if before.channel != after.channel:
        if before.channel is not None and after.channel is not None:
            # รับช่องเสียงก่อนหน้าและช่องเสียงปัจจุบันของสมาชิก
            before_channel = before.channel
            after_channel = after.channel
            
            # Check for recent audit logs to find out who moved the member
            async for entry in member.guild.audit_logs(limit=10, action=discord.AuditLogAction.member_move):
                if entry.target and entry.target.id == member.id:
                    mover = entry.user
                    notification_channel = bot.get_channel(NOTIFICATION_CHANNEL_ID)
                    if notification_channel:
                        await notification_channel.send(
                            f'{member.name} ถูกย้ายจากห้อง {before_channel.name} ไปยังห้อง {after_channel.name} โดย {mover.name}'
                        )
                    break

server_on()

bot.run(os.getenv('BOT_TOKEN'))
