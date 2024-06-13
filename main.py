import os
import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import random
from myserver import server_on

# Notification channel ID (replace with the actual channel ID for notifications)
NOTIFICATION_CHANNEL_ID = 1159149849539788932

# List of authorized user IDs
AUTHORIZED_USER_IDS = [767056525708492840, 978601165174472755]

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

async def disconnect_user(member, wait_time, original_channel, count):
    while count != 0:
        await asyncio.sleep(wait_time)
        if member.voice and member.voice.channel:
            await member.edit(voice_channel=None)  # Disconnect the user from the voice channel
            embed = discord.Embed(
                title="ภารกิจตัดการเชื่อมต่อ",
                description=f"ไอ <@{member.id}> ถูกตัดการเชื่อมต่อ 😈.",
                color=discord.Color.red()
            )
            embed.add_field(name="โดนตัดการเชื่อมต่อจากห้อง", value=f"<#{original_channel.id}>", inline=True)
            embed.add_field(name="เวลาที่เชื่อมต่อ", value=f"{wait_time} วินาที", inline=True)
            embed.set_footer(text="ตัดการเชื่อมต่อคนปากหมาจำกัด")

            notification_channel = bot.get_channel(NOTIFICATION_CHANNEL_ID)
            if notification_channel:
                await notification_channel.send(embed=embed)
            
            if count > 0:
                count -= 1
                if count == 0:
                    break
        else:
            break

@bot.event
async def on_voice_state_update(member, before, after):
    if member.id in bot.pending_disconnects:
        disconnect_info = bot.pending_disconnects[member.id]
        if after.channel:
            wait_time = disconnect_info['wait_time']
            count = disconnect_info['count']
            original_channel = after.channel
            await disconnect_user(member, wait_time, original_channel, count)
            if count == 0:
                bot.pending_disconnects.pop(member.id, None)

@bot.tree.command(name='hellobot', description='ไว้ให้บอททักทาย')
async def hellocommand(interaction: discord.Interaction):
    await interaction.response.send_message("Hello กูเป็นบอทของเซิฟซิสเต้ม")

@bot.tree.command(name='name', description='ไว้ให้บอททักทายแต่มีชื่อด้วย')
@app_commands.describe(name="คุณชื่ออะไร ?")
async def namecommand(interaction: discord.Interaction, name: str):
    await interaction.response.send_message(f"หวัดดีไอ{name}")

@bot.tree.command(name='disconnect', description='เลือกผู้ใช้ที่จะถูกตัดการเชื่อมต่อ')
@app_commands.describe(name="ชื่อของคนที่ต้องการตัดการเชื่อมต่อ", randomtime_from="เวลาสุ่มเริ่มต้น (วินาที)", randomtime_to="เวลาสุ่มสิ้นสุด (วินาที)", count="จำนวนครั้งที่จะตัดการเชื่อมต่อ (ถ้าไม่ระบุจะตัดเรื่อยๆ)")
async def disconnect(interaction: discord.Interaction, name: str, randomtime_from: int, randomtime_to: int, count: int = -1):
    if interaction.user.id not in AUTHORIZED_USER_IDS:
        await interaction.response.send_message("คุณไม่มีสิทธิ์ใช้คำสั่งนี้", ephemeral=True)
        return

    guild = interaction.guild
    member = discord.utils.find(lambda m: m.name == name, guild.members)

    if member:
        wait_time = random.randint(randomtime_from, randomtime_to)
        bot.pending_disconnects[member.id] = {'wait_time': wait_time, 'count': count}
        await interaction.response.send_message(f"ตั้งค่าให้ {name} ถูกตัดการเชื่อมต่อใน {wait_time} วินาทีหลังจากที่เข้าห้องเสียง")

        # Disconnect immediately if the user is already in a voice channel
        if member.voice and member.voice.channel:
            original_channel = member.voice.channel
            await disconnect_user(member, wait_time, original_channel, count)
    else:
        await interaction.response.send_message(f"ไม่พบผู้ใช้ที่ชื่อ {name}")

@bot.tree.command(name='stop', description='หยุดการตัดการเชื่อมต่อสำหรับผู้ใช้ที่เลือก')
@app_commands.describe(name="ชื่อของคนที่ต้องการหยุดการตัดการเชื่อมต่อ")
async def stop(interaction: discord.Interaction, name: str):
    if interaction.user.id not in AUTHORIZED_USER_IDS:
        await interaction.response.send_message("คุณไม่มีสิทธิ์ใช้คำสั่งนี้", ephemeral=True)
        return

    guild = interaction.guild
    member = discord.utils.find(lambda m: m.name == name, guild.members)

    if member and member.id in bot.pending_disconnects:
        bot.pending_disconnects.pop(member.id, None)
        await interaction.response.send_message(f"หยุดการตัดการเชื่อมต่อสำหรับ {name} แล้ว")
    else:
        await interaction.response.send_message(f"ไม่พบผู้ใช้ที่ชื่อ {name} หรือไม่มีการตัดการเชื่อมต่อที่ต้องหยุด")

# Initialize the dictionary to keep track of pending disconnects
bot.pending_disconnects = {}

server_on()

bot.run(os.getenv('BOT_TOKEN'))
