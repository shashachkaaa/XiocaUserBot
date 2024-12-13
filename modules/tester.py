from utils.imports import *
from utils.func import *
from utils.misc import *

@Client.on_message(filters.command("suspend", prefixes=prefix) & filters.me)
async def suspend(client, message):
	try:
		t = int(message.text.split()[1])
	except:
		return await message.edit('<emoji id=5237993272109967450>❌</emoji> <b>Введите время заморозки в секундах!</b>')
	
	await message.edit(f'<emoji id=5452023368054216810>🥶</emoji> <b>Xioca заморожена на</b> <code>{t}</code> <b>секунд</b>')
	time.sleep(t)

@Client.on_message(filters.command("ping", prefixes=prefix) & filters.me)
async def ping(client, message):
	a = time.time()
	m = await message.edit_text(f'<emoji id=5372905603695910757>🌙</emoji>')
	if m:
		b = time.time()
		end_time = time.time() - start_time
		hours, rem = divmod(end_time, 3600)
		minutes, seconds = divmod(rem, 60)
		await m.edit_text(f'<emoji id=5372905603695910757>🌙</emoji> Пинг: <b>{round((b - a) * 1000)}</b> ms\n<emoji id=5431449001532594346>⚡️</emoji> Прошло времени с момента запуска: <b>{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}</b>')

modules_help["tester"] = {
    "ping": "Проверить скорость отклика Telegram",
    "suspend": "Заморозить юзербота"
}