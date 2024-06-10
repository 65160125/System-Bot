import discord
import os
from myserver import server_on

# รหัสช่อง Discord ที่ต้องการแจ้งเตือน
ALERT_CHANNEL_ID = 1159149849539788932

# สร้าง intents
intents = discord.Intents.default()
intents.members = True
intents.voice_states = True

# สร้าง Client Discord โดยใส่ intents เข้าไปในอาร์กิวเมนต์
client = discord.Client(intents=intents)

# เก็บสถานะของสมาชิกในแต่ละห้องเสียง
member_states = {}

# ฟังก์ชันจัดการเหตุการณ์สมาชิกย้ายห้อง
async def on_member_move(before, after):
  # ตรวจสอบว่าสมาชิกย้ายจากห้องเสียงหรือไม่
  if before.voice.channel and after.voice.channel:
    # ตรวจสอบว่าสมาชิกย้ายจากห้องไหนไปห้องไหน
    if before.voice.channel.id != after.voice.channel.id:
      # บันทึกสถานะของสมาชิกก่อนย้าย
      member_states[before.id] = before.voice.channel.id

      # ตรวจสอบว่าใครเป็นผู้ย้าย
      if after.id not in member_states[after.id]:
        mover_id = after.id  # สมาชิกที่ย้าย
      else:
        mover_id = None  # ไม่สามารถระบุผู้ย้ายได้

      # สร้างข้อความแจ้งเตือน
      if mover_id:
        mover = client.get_user(mover_id)
        message = f"{mover.name} ย้าย {before.name} จาก {before.voice.channel.name} ไปยัง {after.voice.channel.name}"
      else:
        message = f"{before.name} ย้ายจาก {before.voice.channel.name} ไปยัง {after.voice.channel.name} (ไม่สามารถระบุผู้ย้ายได้)"

      # ส่งข้อความแจ้งเตือนไปยังช่องที่กำหนด
      alert_channel = client.get_channel(ALERT_CHANNEL_ID)
      await alert_channel.send(message)

# ฟังก์ชัน `on_ready`
@client.event
async def on_ready():
  print(f"Logged in as {client.user}")
  server_on()

# เชื่อมต่อบอทกับ Discord
client.run(os.getenv('BOT_TOKEN'))
