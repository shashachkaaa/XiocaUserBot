from utils.imports import *
from utils.func import *
from utils.misc import *

@Client.on_message(filters.command('info', prefixes=prefix) & filters.user(allowed))
async def info(client, message):
	m = await answer(message, '<emoji id=5372905603695910757>🌙</emoji> <b>Загружаю инфо...</b>')
	try:
		cpu = f'{psutil.cpu_percent()}%'
	except:
		cpu = 'Неизвестно'
	try:
		ram = psutil.virtual_memory().used / (1024 * 1024)
		ram = f'{ram:.2f}'
	except:
		ram = 'Неизвестно'
	me = await client.get_me()
	name = me.first_name
	end_time = time.time() - start_time
	hours, rem = divmod(end_time, 3600)
	minutes, seconds = divmod(rem, 60)
	
	if system == "Windows":
		platform_name = "<emoji id=5316891065423241127>🖥</emoji> Windows"
	elif system == "Linux":
	       if "termux" in sys.argv[0]:
	       	platform_name = "<emoji id=5407025283456835913>📱</emoji> Termux"
	       elif "p3droid" in sys.argv[0]:
	       	platform_name = "<emoji id=5407025283456835913>📱</emoji> Pydroid3"
	       else:
	       	platform_name = "<emoji id=5361541227604878624>🐧</emoji> Linux"
	elif system == "Darwin":
	 	platform_name = "<emoji id=5431376038628171216>💻</emoji> MacOS"
	elif system == "FreeBSD":
		platform_name = "<emoji id=5431376038628171216>💻</emoji> FreeBSD"
	else:
		platform_name = "<emoji id=5330115548900501467>🔑</emoji> Unknown"

	try:
		subprocess.run("rm -rf version.txt", shell=True, capture_output=True)
		subprocess.run("wget https://raw.githubusercontent.com/shashachkaaa/XiocaUserBot/refs/heads/main/version.txt", shell=True, capture_output=True)
	except:
		await message.edit_text('<emoji id=5373310679241466020>🌀</emoji> <b>Установка пакетов...</b>')
		subprocess.run("pkg install wget -y", shell=True, capture_output=True)
		subprocess.run("wget https://raw.githubusercontent.com/shashachkaaa/XiocaUserBot/refs/heads/main/version.txt")
	ver = cursor.execute(f'SELECT version from settings').fetchone()[0]
	with open("version.txt", "r") as file:
			v = file.readline().strip()
			v = v.replace('v = ', '')
	vv = ver.replace("'", '')
	if ver == v:
		tv = f'<emoji id=5469741319330996757>💫</emoji> Версия: {vv} актуальная'
	else:
		tv = f'<emoji id=5237993272109967450>❌</emoji> Версия: {vv} устаревшая. Введите <code>{prefix}update</code> для обновления.'
	
	itext = f'''
<emoji id=5372905603695910757>🌙</emoji> <b>Xioca

<emoji id=5373141891321699086>😎</emoji> Владелец: {name}
{tv}

<emoji id=5472111548572900003>⌨️</emoji> Префикс: «{prefix}»
<emoji id=5451646226975955576>⌛️</emoji> Аптайм: {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}

<emoji id=5258203794772085854>⚡️</emoji> Использование CPU: <i>~{cpu}</i>
<emoji id=5359785904535774578>💼</emoji> Использование RAM: <i>~{ram} MB</i>

{platform_name}</b>'''
	
	type = db.get("core.main", 'type_info', 'xioca')
	dildo = db.get('core.main', "info")
	
	if type == 'xioca':
		await answer(message, animation=True, chat_id=message.chat.id, response="xioca.mp4", caption=itext)
	elif type == 'photo':
		await answer(message, photo=True, chat_id=message.chat.id, response=dildo, caption=itext)
	elif type == 'animation':
		await answer(message, animation=True, chat_id=message.chat.id, response=dildo, caption=itext)
	else:
		await answer(message, video=True, chat_id=message.chat.id, response=dildo, caption=itext)
	await client.delete_messages(message.chat.id, m[0].id)

modules_help["info"] = {
	f"info": "Информация о юзерботе"
}