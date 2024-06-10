import discord
from myserver import server_on



# รหัสช่อง Discord ที่ต้องการแจ้งเตือน
ALERT_CHANNEL_ID = 1159149849539788932

# สร้าง Client Discord
client = discord.Client()

# เก็บสถานะของสมาชิกในแต่ละห้องเสียง
member_states = {}

# ฟังก์ชันจัดการเหตุการณ์สมาชิกย้ายห้อง
async def on_member_move(before, after):
  # ตรวจสอบว่าสมาชิกย้ายจากห้องเสียงหรือไม่
  if before.voice_channel and after.voice_channel:
    # ตรวจสอบว่าสมาชิกย้ายจากห้องไหนไปห้องไหน
    if before.voice_channel.id != after.voice_channel.id:
      # บันทึกสถานะของสมาชิกก่อนย้าย
      member_states[before.id] = before.voice_channel.id

      # ตรวจสอบว่าใครเป็นผู้ย้าย
      if after.voice_channel.id not in member_states[after.id]:
        mover_id = after.id  # สมาชิกที่ย้าย
      else:
        mover_id = None  # ไม่สามารถระบุผู้ย้ายได้

      # สร้างข้อความแจ้งเตือน
      if mover_id:
        mover = client.get_user(mover_id)
        message = f"{mover.name} ย้าย {before.name} จาก {before.voice_channel.name} ไปยัง {after.voice_channel.name}"
      else:
        message = f"{before.name} ย้ายจาก {before.voice_channel.name} ไปยัง {after.voice_channel.name} (ไม่สามารถระบุผู้ย้ายได้)"

      # ส่งข้อความแจ้งเตือนไปยังช่องที่กำหนด
      alert_channel = client.get_channel(ALERT_CHANNEL_ID)
      await alert_channel.send(message)

# ฟังก์ชัน `on_ready`
@client.event
async def on_ready():
  print(f"Logged in as {client.user}")
  server_on()

# เชื่อมต่อบอทกับ Discord
bot.run(os.getenv('BOT_TOKEN'))
