import pip, os, re
try:
	from pyrogram import Client, filters
	from pyrogram.types import ChatPermissions
	from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
	from gtts import gTTS
	import sqlite3, logging, time, requests, asyncio, pyttsx3, datetime, random, json, g4f, html, psutil, platform, sys, pyfiglet
#	from config import api_id, api_hash, id
	from datetime import datetime, timedelta
	from time import gmtime, strptime, strftime
	from io import StringIO
	from contextlib import redirect_stdout
	import subprocess
	import speech_recognition as sr
	from pydub import AudioSegment
	from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
	import pytz
	from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
	from pyrogram.raw.functions.account import ReportPeer
	from pyrogram.raw.types import *
	from unidecode import unidecode as ui
	from colorama import Fore, Style
except ImportError:
	pip.main(['install', '-r', 'requirements.txt'])
	if os.name == "nt":
	    os.execvp(
	        "python",
	        [
	            "python",
	            "main.py",
	        ],
	     )
	else:
	    os.execvp(
	        "python3",
	        [
	            "python3",
	            "main.py",
	        ],
	     )

version = '0.0.1 beta'
system = platform.system()
start_time = time.time()

async def get_user_info():
    await client.start()

# Настройка учетных данных API
try:
    # Загрузка данных учетной записи из файла при его наличии
    with open("user_data.txt", "r") as file:
#    	api_id, api_hash = map(int, file.read().split("\n"))
        api_id = file.readline().strip()
        api_hash = file.readline().strip()
        
        api_id = api_id.replace(f'api_id=', '')
        api_hash = api_hash.replace(f'api_hash=', '')
        api_id  = int(api_id[0])
        api_hash = str(api_hash[0])
        
except FileNotFoundError:
    # Если файла нет, запросите данные учетной записи у пользователя
    api_id = int(input("Введите ваш API ID: "))
    api_hash = input("Введите ваш API HASH: ")

    with open("user_data.txt", "w") as file:
        file.write(f"api_id={api_id}\napi_hash='{api_hash}'")

client = Client("session", api_id, api_hash)
app = client
logging.basicConfig(level=logging.INFO)

#asyncio.run(get_user_info())

authed = client.authorize()

if authed:
    print("Пользователь авторизован!")
# Если пользователь не авторизован, запросите код подтверждения
else:
    # Запрос кода подтверждения
    phone_number = input("Введите ваш номер телефона: ")
    code = client.send_code(phone_number)

    # Ввод кода подтверждения
    input_code = input("Введите код подтверждения: ")

    # Подтверждение номера телефона
    client.sign_in(phone_number, input_code)

subprocess.call(['apt', 'install', 'ffmpeg', '-y'])

if os.name == "nt":
        	os.system("cls")
else:
        	os.system("clear")
print(Fore.YELLOW + Style.BRIGHT + '''
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣤⣤⣤⣤⣤⣤⣄⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠛⠻⠿⢿⣿⣿⣿⣿⣿⣶⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠻⣿⣿⣿⣿⣿⣿⣶⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣷⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⣀⣙⢿⣿⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠻⣿⣿⣿⣿⣿⣿⣿⣄⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⢹⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⡟⠹⠿⠟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡿⠋⡬⢿⣿⣷⣤⣤⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠀⠀⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⡇⢸⡇⢸⣿⣿⣿⠟⠁⢀⣬⢽⣿⣿⣿⣿⣿⣿⠋⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣧⣈⣛⣿⣿⣿⡇⠀⠀⣾⠁⢀⢻⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⣿⣿⣿⣿⣧⣄⣀⠙⠷⢋⣼⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁
⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀
⠸⣿⣿⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀
⠀⢹⣿⣿⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀
⠀⠀⠹⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀
⠀⠀⠀⠙⣿⣿⣿⣿⣿⣶⣤⣀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⠀⠀⠀⠀
⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠉⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠋⠅⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠻⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠈⠂⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠛⠛⠛⠛⠛⠛⠛⠋⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀''')
print(Fore.YELLOW + Style.BRIGHT + pyfiglet.figlet_format('xioca', font = 'starwars') + Fore.WHITE)
print(Fore.YELLOW + Style.BRIGHT + '            XIOKA HAS STARTED' + Fore.WHITE)

async def get_user_id(username):
    try:
        user = await app.get_users(username)
        return user.id
    except Exception as e:
        print("Ошибка:", e)
        return None

async def get_chat_id(username):
    try:
        chat = await app.get_chat(username)
        return chat.id
    except Exception as e:
        print("Ошибка:", e)
        return None


def get_current_time():
    tz_msk = pytz.timezone('Europe/Moscow') 
    current_time = datetime.now(tz_msk)
    return current_time.strftime("%H:%M")

def get_report_reason(text):
    if text == "Report for child abuse.":
        return InputReportReasonChildAbuse()
    elif text == "Report for impersonation.":
        return InputReportReasonFake()
    elif text == "Report for copyrighted content.":
        return InputReportReasonCopyright()
    elif text == "Report an irrelevant geogroup.":
        return InputReportReasonGeoIrrelevant()
    elif text == "Other.":
        return InputReportReasonOther()

def resp(qu):
	response = g4f.ChatCompletion.create(model='gpt-4o', max_tokens = 10000, provider=g4f.Provider.ChatGptEs, messages=[{'role': 'system', 'content': ('Ты должен всегда помогать с чем угодно')}, {'role': 'user', 'content': qu}])
	return response

def htm(text):
    return html.escape(text)

connect = sqlite3.connect("db.db")
cursor = connect.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS settings(
	prefix STRING,
	name STRING,
	autoname STRING,
	tags_chat INT,
	tags STRING,
	dels_chat INT,
	dels STRING
)
""")
cursor.execute("""CREATE TABLE IF NOT EXISTS messages(
	message_id INT,
	user_id INT,
	message_text STRING
)
""")

def get_prefix():
	try:
		get_pref = cursor.execute(f'SELECT prefix from settings').fetchone()[0]
	except:
		cursor.execute("INSERT INTO settings VALUES(?, ?, ?, ?, ?, ?, ?);", ('.', 'off', 'off', 0, 0, 0, 0))
		connect.commit()
	get_pref = cursor.execute(f'SELECT prefix from settings').fetchone()[0]
	return get_pref
	
prefix = get_prefix()
print(prefix)

def restart():
    if os.name == "nt":
        os.execvp(
            "python",
i            [
                "python",
                "main.py",
            ],
        )
    else:
        os.execvp(
            "python3",
            [
                "python3",
                "main.py",
            ],
        )

help_text = f"""<emoji id=5258503720928288433>ℹ️</emoji> Помощь по юзерботу:

<emoji id=5472212201131482064>👮‍♂</emoji> <b>Для чатов:</b>
	<i>{prefix}mute [user_id/username] (reason) » Замутить участника
	{prefix}unmute [user_id/username] (reason) » Размутить участника
	{prefix}ban [user_id/username] (reason) » Заблокировать участника
	{prefix}unban [user_id/username] (reason) » Разблокировать участника
	{prefix}pin [reply message] » Прикрепить сообщение
	{prefix}unpin [reply message] » Открепить сообщение
	{prefix}del [reply message] » удалить сообщение
	{prefix}purge [reply message] » удалить сообщения до отвеченного
	{prefix}tagall [string] » отметить всех участников чата</i>

<emoji id=5258096772776991776>⚙</emoji> <b>Утилиты:</b>
	<i>{prefix}join [user_id/chatname] » Зайти в чат
	{prefix}leave [user_id/chatname] » Выйти с чата
	{prefix}ping » Проверить пинг
	{prefix}pmbl [user_id/username] » Заблокировать в ЛС пользователя
	{prefix}unpmbl [user_id/username] » Разблокировать в ЛС пользователя
	{prefix}restart » Перезапустить юезрбота
	{prefix}eval [string] » Интерпретатор Python
	{prefix}terminal [string] » Выполнить команду в терминале
	{prefix}voice [reply voice] » Распознать ГС
	{prefix}creategroup [string] » Создать чат
	{prefix}dels [on/off] » Автосохранение удаленных сообщений
	{prefix}tags [on/off] » Отключить уведомления при упомнинании вас в чатах
	{prefix}shifr (text) » транслит на английский
	{prefix}report (reply) (int) » закидать репортами
	{prefix}gpt [string] » запрос к ChatGPT
	{prefix}setprefix [string] » установить префикс к командам
	{prefix}weather [string] » узнать погоду в городе
	{prefix}serverinfo »  узнать информацию о сервере
	{prefix}info » узнать информацию о юзерботе</i>

<emoji id=5319259490778886242>🤩</emoji> <b>Анимации/плюшки:</b>
	<i>{prefix}magic » Анимация огромного сердечка
	{prefix}love » Анимация из сердечек
	{prefix}autoname [string] » Установить время в ник
	{prefix}stopautoname » Убрать время в нике</i>"""

@app.on_message(filters.command('info', prefixes=prefix))
async def info(client, message):
	m = await message.edit_text('🌙 <b>Загружаю инфо...</b>')
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
		platform_name = "🖥 Windows"
	elif system == "Linux":
	       if "termux" in sys.argv[0]:
	       	platform_name = "🕶 Termux"
	       elif "p3droid" in sys.argv[0]:
	       	platform_name = "📱 Pydroid3"
	       else:
	       	platform_name = "🐧 Linux"
	elif system == "Darwin":
	 	platform_name = "💻 MacOS"
	else:
		platform_name = "❓ Unknown"
	
	await client.send_animation(message.chat.id, animation="xioca.mp4", caption=f'''
🌙 <b>Xioca

😎 Владелец: {name}
💫 Версия: {version}

⌨️ Префикс: «{prefix}»
⌛️ Аптайм: {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}

⚡️ Использование CPU: <i>~{cpu}</i>
💼 Использование RAM: <i>~{ram} MB</i>

{platform_name}</b>''')
	await client.delete_messages(message.chat.id, m.id)

@app.on_message(filters.command('serverinfo', prefixes=prefix))
async def servinfo(client, message):
	try:
		cpu_count = psutil.cpu_count()
		cpu_freq = psutil.cpu_freq()
		cpu_percent = psutil.cpu_percent()
	
		memory_total = psutil.virtual_memory().total
		memory_available = psutil.virtual_memory().available
	
		disk_usage = psutil.disk_usage('/')
	
		net_io_counters = psutil.net_io_counters()
	except Exception as e:
		return await message.edit_text(f'<emoji id=5237993272109967450>❌</emoji> <b>Ошибка: {e}</b>')
	
	await message.edit_text(f'''
	🖥 Информация о сервере:
	
	🎛 Количество ядер процессора: {cpu_count}
	📈 Частота процессора: {cpu_freq.current:.2f} ГГц
	📊 Загрузка процессора: {cpu_percent}%
	💽 Всего памяти: {memory_total / (10243):.2f} ГБ
	💿 Доступно памяти: {memory_available / (10243):.2f} ГБ
	📀 Использование диска: {disk_usage.percent}%
	
	📡 Сетевой ввод/вывод:
		⬅ Входящий трафик: {net_io_counters.bytes_recv / (10243):.2f} ГБ
		➡ Исходящий трафик: {net_io_counters.bytes_sent / (10243):.2f} ГБ''')

@app.on_message(filters.command('weather', prefixes=prefix))
async def weather(client, message):
	try:
		qu = " ".join(message.text.split()[1:])
	except:
		return await message.edit_text(f'<emoji id=5237993272109967450>❌</emoji> <b>Не верно введены аргументы!</b>')
	key = '18f76e3ac0c48dee34905f0c9e2e51d1'
	ed = 'metric'
	lang = 'ru'
	format = 'json'
	url = f"https://api.openweathermap.org/data/2.5/weather?q={qu}&units={ed}&lang={lang}&appid={key}"
	response = requests.get(url)
	if response.status_code == 200:
		data = response.json()
		return await message.edit_text(f'''
		🌇 Город: {data['name']}
		🗺 Страна: {data['sys']['country']}
		🌡 Температура: {data['main']['temp']} °C
		☝️ Ощущается как: {data['main']['feels_like']} °C
		💧 Влажность: {data['main']['humidity']}%
		🌎 Давление: {data['main']['pressure']} гПа
		💨 Ветер: {data['wind']['speed']} м/с
		⛅ Погода: {data['weather'][0]['description']}''')
	else:
		await message.edit_text(f'<emoji id=5237993272109967450>❌</emoji> <b>Ошибка при получении погоды: {response.status_code}</b>')

@app.on_message(filters.command('setprefix', prefixes=prefix))
async def setprefix(client, message):
	try:
		qu = " ".join(message.text.split()[1:])
	except:
		return await message.edit_text(f'<emoji id=5237993272109967450>❌</emoji> <b>Не верно введены аргументы!</b>')
	
	await message.edit_text(f'✅ <b>Префикс "{qu}" успешно установлен!</b>')
	await asyncio.sleep(1)
	await message.edit_text(f'<emoji id=5258420634785947640>🔄</emoji> <code>Перезапускаюсь для установки префикса...</code>')
	cursor.execute(f'UPDATE settings SET prefix = "{qu}"')
	connect.commit()
	restart()

@app.on_message(filters.command('gpt', prefixes=prefix))
async def chatgpt(client, message):
	try:
		qu = " ".join(message.text.split()[1:])
	except:
		return await message.edit_text(f'<emoji id=5237993272109967450>❌</emoji> <b>Не верно введены аргументы!</b>')
	
	await message.edit_text(f'🌐 <b>ChatGPT генерирует ответ, ожидайте...</b>')
	try:
		response = resp(qu)
	except Exception as e:
		return await message.edit_text(f'<emoji id=5237993272109967450>❌</emoji> <b>Ошибка: {e}</b>')
	
	try:
		await message.edit_text(f"❓ <b>Ваш вопрос: {qu}\n🌐 Ответ ChatGPT:</b>\n{htm(response)}")
	except Exception as e:
		return await message.edit_text(f'<emoji id=5237993272109967450>❌</emoji> <b>Ошибка: {e}</b>')

@app.on_message(filters.command('lj', prefixes=prefix))
async def leavejoin(client, message):
	chat_id = message.chat.id
	await client.delete_messages(chat_id, message.id)
	await app.leave_chat(chat_id)
	await app.join_chat(chat_id)

@app.on_message(filters.command('shifr', prefixes=prefix))
async def shifr(client, message):
	try:
		text = " ".join(message.text.split()[1:])
	except:
		return await message.edit_text(f'<emoji id=5237993272109967450>❌</emoji> <b>Не верно введены аргументы!</b>')
	
	await message.edit_text(ui(text))

@app.on_message(filters.command('report', prefixes=prefix))
async def report(client, message):
	r = message.reply_to_message.from_user
	try:
		spam = int(message.text.split()[1])
		print(spam)
	except Exception as e:
		return await message.edit_text(f'<emoji id=5237993272109967450>❌</emoji> <b>Не верно введены аргументы!</b>')
		
	if r:
		us = r.username
		peer = await app.resolve_peer(f"@{us}")
		peer_id = peer.user_id
		access_hash = peer.access_hash
		
		channel = InputPeerChannel(channel_id=peer_id, access_hash=access_hash)
		reason  = get_report_reason("Report for child abuse.")
		report_peer = ReportPeer(peer=channel, reason=reason, message="spam")
		await message.edit_text(f'<b>Жалуюсь...</b>')
		num = 0
		l = []
		for i in range(0, spam):
			try:
				num += 1
				report = await app.send(report_peer)
			except Exception as e:
				l.append(e)
		try:
			lis = '\n'.join(l)
		except:
			lis = 'нет'
		await message.edit_text(f'<emoji id=5237907553152672597>✅</emoji> <b>Отправлено {num} жалоб!</b>')
	else:
		await message.edit_text('<emoji id=5237993272109967450>❌</emoji> <b>Команда должна быть ответом на сообщение!</b>')
		

@app.on_message(filters.command('id', prefixes=prefix))
async def id(client, message):
	r = message.reply_to_message
	cid = message.chat.id
	
	if r:
		id = message.reply_to_message.from_user.id
		name = message.reply_to_message.from_user.first_name
		await message.edit_text(f'<emoji id=5472146462362048818>💡</emoji> <b>ID {name}: <code>{id}</code>\n<emoji id=5818885490065017876>🆔</emoji> Chat ID: {chat_id}</b>')
	else:
		await message.edit_text(f'<emoji id=5818885490065017876>🆔</emoji> <b>Chat ID: {chat_id}</b>')

@app.on_message(filters.command('dels', prefixes=prefix))
async def dels(client, message):
	t = str(message.text.split()[1])
	ty = t.replace(f'{prefix}dels', '')
	type = ty.replace(f'{prefix}dels ', '')
	
	if type == 'on':
		await message.edit_text(f'<emoji id=5339536521009571338>👋</emoji> <b>Теперь удаленные сообщения сохраняются!</b>')
		cursor.execute(f'UPDATE settings SET dels = "on"')
		connect.commit()
		chat_id = cursor.execute(f'SELECT dels_chat FROM settings').fetchone()
		chat_id = int(chat_id[0])
		try:
			await app.send_message(chat_id, f'<emoji id=5237907553152672597>✅</emoji> <b>Сюда будут пересылатся удаленные сообщения с ЛС!</b>')
		except:
			c = await app.create_supergroup('deleted messages')
			chat_id = c.id
			cursor.execute(f'UPDATE settings SET dels_chat = {chat_id}')
			connect.commit()
			await app.send_message(chat_id, f'<emoji id=5237907553152672597>✅</emoji> <b>Сюда будут пересылатся удаленные сообщения с ЛС!</b>')
	elif type == 'off':
		await message.edit_text(f'<emoji id=5472100935708711380>👍</emoji> <b>Теперь удаленные сообщения не сохраняются!</b>')
		cursor.execute(f'UPDATE settings SET dels = "off"')
		connect.commit()
	else:
		await message.edit_text('<emoji id=5237993272109967450>❌</emoji> <b>Не верно введены аргументы!</b>')

@app.on_deleted_messages()
async def dels(client, message):
	dels = cursor.execute(f'SELECT dels from settings').fetchone()
	dels = str(dels[0])
	
	if dels == 'on':
		try:
			message_id = message[0].id
			print(message_id)
			user_id = cursor.execute(f'SELECT user_id from messages WHERE message_id = {message_id}').fetchone()
			message_text = cursor.execute(f'SELECT message_text FROM messages WHERE message_id = {message_id}').fetchone()
			dels_chat = cursor.execute(f'SELECT dels_chat from settings').fetchone()
			dels_chat = int(dels_chat[0])

			user_id = int(user_id[0])
			message_text = str(message_text[0])
			
			user = await app.get_users(user_id)
			first_name = user.first_name
			username = user.username
			await app.send_message(dels_chat, f'''<emoji id=5339536521009571338>👋</emoji> {first_name} (@{username} | <code>{user_id}</code>) удалил сообщение в ЛС!
<emoji id=5417875345804108985>🌍</emoji> Текст » <i>{message_text}</i>
''')
		except Exception as e:
			print(e)
			return
	else:
		return
	
@app.on_message(filters.mentioned)
async def tags(client, message):
	chat_id = cursor.execute(f'SELECT tags_chat FROM settings').fetchone()
	tags = cursor.execute(f'SELECT tags FROM settings').fetchone()
	
	tags = str(tags[0])
	chat_id = int(chat_id[0])
	
	if tags == 'on':
		await app.send_message(chat_id, f'''<emoji id=5242628160297641831>🔔</emoji> <b>Вас тегнули в чате</b> «<code>{message.chat.title}</code>» (@{message.chat.username})
<emoji id=5325770433566359627>😲</emoji> Пользователь » {message.from_user.first_name} (@{message.from_user.username})
<emoji id=5465204283383224325>💬</emoji> Ссылка » {message.link}
<emoji id=5465300082628763143>💬</emoji> Текст сообщения » <i>{message.text}</i>''', disable_web_page_preview = True)
		await app.read_chat_history(message.chat.id, message.id)
	else:
		return

@app.on_message(filters.command('tags', prefixes=prefix))
async def tags(client, message):
	tag = str(message.text.split()[1])
	ta = tag.replace(f'{prefix}tags', '')
	t = ta.replace(f'{prefix}tags ', '')
	
	if t == 'on':
		await message.edit_text('<emoji id=5472100935708711380>👍</emoji> <b>Теперь вас не будут беспокоить теги!</b>')
		cursor.execute(f'UPDATE settings SET tags = "on"')
		connect.commit()
		try:
			chat_id = cursor.execute(f'SELECT tags_chat FROM settings').fetchone()
			chat_id = int(chat_id[0])
			await app.send_message(chat_id, f'<emoji id=5237907553152672597>✅</emoji> <b>Сюда будут пересылатся теги с чатов!</b>')
		except:
			c = await app.create_supergroup('tags')
			chat_id = c.id
			cursor.execute(f'UPDATE settings SET tags_chat = {chat_id}')
			connect.commit()
			await app.send_message(chat_id, f'<emoji id=5237907553152672597>✅</emoji> <b>Сюда будут пересылатся теги с чатов!</b>')
	elif t == 'off':
		await message.edit_text('<emoji id=5472100935708711380>👍</emoji> <b>Вас снова могут тегать пользователи в чатах!</b>')
		cursor.execute(f'UPDATE settings SET tags = "off"')
		connect.commit()
	else:
		await message.edit_text('<emoji id=5237993272109967450>❌</emoji> <b>Не верно введены аргументы!</b>')

@app.on_message(filters.command('ids', prefixes=prefix))
async def ids_group(client, message):
	l = []
	chat_id = message.chat.id
	async for member in app.get_chat_members(chat_id):
		l.append(member.user.id)
	
	await app.send_message(message.chat.id, l)

@app.on_message(filters.command('creategroup', prefixes=prefix))
async def create_group(client, message):
	try:
		title = " ".join(message.text.split())
	except:
		await message.edit_text('<emoji id=5237993272109967450>❌</emoji> <b>Не верно введены аргументы!</b>')
		return
	
	t = title.replace(f'{prefix}creategroup ',  '')
	
	if len(t) >= 100:
		await message.edit_text(f'<emoji id=5237993272109967450>❌</emoji> <b>В названии чата не может быть более 100 символов!</b>')
		return
	
	await message.edit_text(f'<emoji id=5237907553152672597>✅</emoji> <b>Чат «{t}» был успешно создан!</b>')
	await app.create_supergroup(t)

@app.on_message(filters.command('stopautoname', prefixes=prefix))
async def clock(client, message):
	name = cursor.execute(f'SELECT name from settings').fetchone()
	name = str(name[0])
	await message.edit_text(f'<emoji id=5237907553152672597>✅</emoji> <b>Время в нике успешно остановлено!</b>')
	n = name.replace(f'{prefix}autoname ', '')
	nm = n.replace("{time}", '')
	try:
		await app.update_profile(first_name=f"{nm}")
	except:
		await app.update_profile(first_name=f'Введите ник')
	cursor.execute(f'UPDATE settings SET autoname = "off"')
	connect.commit()
	
@app.on_message(filters.command('autoname', prefixes=prefix))
async def clock(client, message):
    # Переводим текст команды в строку
    try:
    	n = " ".join(message.text.split())
    except Exception as e:
    	return await message.edit_text('<emoji id=5237993272109967450>❌</emoji> <b>Ошибка: {e}</b>')
    if '{time}' not in n:
    	return await message.edit_text('<emoji id=5237993272109967450>❌</emoji> <b>В введенном нике отсутсвует "{time}"</b>')
   
    type = cursor.execute('SELECT autoname FROM settings').fetchone()[0]
    if type == 'on':
    	return await message.edit_text('<emoji id=5237993272109967450>❌</emoji> <b>У вас уже установлено время в нике!</b>')
    
    # Отправляем сообщение об успешной установке времени в ник
    await message.edit_text(f'<emoji id=5237907553152672597>✅</emoji> <b>Время в ник успешно установлено!</b>')
    cursor.execute(f'UPDATE settings SET name = "{n}"')
    cursor.execute(f'UPDATE settings SET autoname = "on"')
    connect.commit()

    # Цикл для обновления ника с интервалом в 60 секунд
    while True:
        # Получаем значение autoname из базы данных
        autoname_status = cursor.execute('SELECT autoname FROM settings').fetchone()[0]
        
        # Проверяем, включен ли autoname
        if autoname_status == 'on':
            current_time = get_current_time()
            name = n.replace(f'{prefix}autoname ', '')
            name = name.replace("{time}", current_time)
            # Обновляем профиль с новым именем
            try:
            	await app.update_profile(first_name=f"{name}")
            	await asyncio.sleep(60)
            except:
            	await asyncio.sleep(600)
        else:
            # Если autoname выключен, прерываем цикл
            break

@app.on_message(filters.command('purge', prefixes=prefix))
async def delete_mes(client, message):
    start_message_id = message.id
    end_message_id = message.reply_to_message.id
    chat_id = message.chat.id

    ids = []

    async for message in client.get_chat_history(chat_id):
        if message.id == end_message_id:
            break
        ids.append(message.id)
    ids.append(end_message_id)
    await client.delete_messages(chat_id, ids)

@app.on_message(filters.command('del', prefixes=prefix))
async def delete_mes(client, message):
	try:
		msg = message.reply_to_message.id
	except:
		await message.edit_text(f'<emoji id=5237993272109967450>❌</emoji> <b>Команда должна быть ответом на сообщение!</b>')
		return
	message_id = message.id
	chat_id = message.chat.id
	list = [msg, message_id]
	await client.delete_messages(chat_id, list)

@app.on_message(filters.command('love', prefixes=prefix))
async def love(client, message):
	emoji = ['❤️', '🩷', '🧡', '💛', '💚', '🩵', '💙', '💜', '🖤', '🩶', '🤍', '🤎', '💖', '💝', '💓', '💗', "I", "I ❤️", "I ❤️ U", "I ❤️ U!"]
	for i in emoji:
		await message.edit_text(f'<b>{i}</b>')
		await asyncio.sleep(0.3)

@app.on_message(filters.command('magic', prefixes=prefix))
async def magiclove(client, message):
			arr = ["❤️", "🧡", "💛", "💚", "💙", "💜", "🤎", "🖤", "💖"]
			h = "🤍"
			first = ""		
			for i in "".join([h*9, "\n", h*2, arr[0]*2, h, arr[0]*2, h*2, "\n", h, arr[0]*7, h, "\n", h, arr[0]*7, h, "\n", h, arr[0]*7, h, "\n", h*2, arr[0]*5, h*2, "\n", h*3, arr[0]*3, h*3, "\n", h*4, arr[0], h*4]).split("\n"):
				first += i + "\n"
				await message.edit_text(first)
				await asyncio.sleep(0.2)		
			for i in arr:
				await message.edit_text("".join([h*9, "\n", h*2, i*2, h, i*2, h*2, "\n", h, i*7, h, "\n", h, i*7, h, "\n", h, i*7, h, "\n", h*2, i*5, h*2, "\n", h*3, i*3, h*3, "\n", h*4, i, h*4, "\n", h*9]))
				await asyncio.sleep(0.3)
			for _ in range(8):
				rand = random.choices(arr, k=34)
				await message.edit_text("".join([h*9, "\n", h*2, rand[0], rand[1], h, rand[2], rand[3], h*2, "\n", h, rand[4], rand[5], rand[6], rand[7], rand[8],rand[9],rand[10], h, "\n", h, rand[11], rand[12], rand[13], rand[14], rand[15], rand[16],rand[17], h, "\n", h, rand[18], rand[19], rand[20], rand[21], rand[22], rand[23],rand[24], h, "\n", h*2, rand[25], rand[26], rand[27], rand[28], rand[29], h*2, "\n", h*3, rand[30], rand[31], rand[32], h*3, "\n", h*4, rand[33], h*4, "\n", h*9]))
				await asyncio.sleep(0.3)
			fourth = "".join([h*9, "\n", h*2, arr[0]*2, h, arr[0]*2, h*2, "\n", h, arr[0]*7, h, "\n", h, arr[0]*7, h, "\n", h, arr[0]*7, h, "\n", h*2, arr[0]*5, h*2, "\n", h*3, arr[0]*3, h*3, "\n", h*4, arr[0], h*4, "\n", h*9])
			await message.edit_text(fourth)
			for _ in range(47):
				fourth = fourth.replace("🤍", "❤️", 1)
				await message.edit_text(fourth)
				await asyncio.sleep(0.1)
			for i in range(8):
				await message.edit_text((arr[0]*(8-i)+"\n")*(8-i))
				await asyncio.sleep(0.4)
			for i in ["I", "I ❤️", "I ❤️ U", "I ❤️ U!"]:
				await message.edit_text(f"<b>{i}</b>")
				await asyncio.sleep(0.5)

@app.on_message(filters.command('voice', prefixes=prefix))
async def voice(client, message):
    await message.edit_text('🎤 <b>Распознаю...</b>')
    voice = message.reply_to_message.voice
    if not voice:
        await message.edit_text('<emoji id=5237993272109967450>❌</emoji> <b>Команда должна быть ответом на голосовое сообщение!</b>')
        return
    file_id = voice.file_id
    try:
        voice_file = await client.download_media(file_id)
        
        converted_file = voice_file.replace('.ogg', '.wav')
        AudioSegment.from_file(voice_file).export(converted_file, format='wav')
        
        recognizer = sr.Recognizer()
        with sr.AudioFile(converted_file) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language='ru-RU')
        await message.edit_text(f'✅ <b>Голосовое сообщение распознано:</b> <i>{text}</i>')
        os.remove(voice_file)
        os.remove(converted_file)
    except Exception as e:
        await message.edit_text(f'<emoji id=5237993272109967450>❌</emoji> <b>Не удалось распознать голосовое сообщение:</b> <code>{e}</code>')

@app.on_message(filters.command('tagall', prefixes=prefix))
async def tagall(client, message):
    chat_id = message.chat.id

    num = 0
    await message.edit_text(f'<emoji id=5471930335312747865>💬</emoji> <b>Отмечаю...</b>')
    async for member in app.get_chat_members(chat_id):
        if member.user.username is None:
            pass
        elif member.user.id == message.from_user.id:
        	pass
        elif member.user.is_bot:
        	pass
        else:
            title = " ".join(message.text.split())
            tit = title.replace(f"{prefix}tagall ",  '')
            t = tit.replace(f'{prefix}tagall', '')
            if t == '':
            	tt = f'<b><a href="tg://user?id={member.user.id}">{member.user.first_name}</a></b>'
            else:
            	tt = f'<b><a href="tg://user?id={member.user.id}">{t}</a></b>'
            await app.send_message(chat_id, tt)
            num += 1
    await app.send_message(chat_id, f'<emoji id=5474371208176737086>✉️</emoji> <b>Отмечено {num} участников</b>')

@app.on_message(filters.command(['t', 'terminal'], prefixes=prefix) & filters.me)
async def terminal(client, message):
    code = message.text
    command = code.replace(f"{prefix}terminal ", "").replace(f"{prefix}t ", "")
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if process.returncode == 0:
        await message.edit_text(f'''<emoji id=5339181821135431228>💻</emoji> <b>Команда:</b>
```bash
{command}```

<emoji id=5375360100196163660>🐲</emoji> <b>Вывод:</b>
```bash
{output.decode()}```
''')
    else:
        await message.edit(f'''<emoji id=5339181821135431228>💻</emoji> <b>Команда:</b>
```bash
{command}```

<emoji id=5237993272109967450>❌</emoji> <b>Ошибка:</b>
```bash
{error.decode()}```''')

@app.on_message(filters.command(['t', 'terminal'], prefixes=prefix) & filters.me)
async def terminal(client, message):
	code = message.text
	command = code.replace(f"{prefix}terminal ", "").replace(f"{prefix}t ", "")
	subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, error = process.communicate()
	try:
		await message.edit_text(f'''<emoji id=5339181821135431228>💻</emoji> <b>Команда:</b>
```bash
{command}```

<emoji id=5375360100196163660>🐲</emoji> <b>Вывод:</b>
```bash
{output.decode()}```''')
	except:
		await message.edit_text(f'''<emoji id=5339181821135431228>💻</emoji> <b>Команда:</b>
```bash
{command}```

<emoji id=5375360100196163660>🐲</emoji> <b>Вывод:</b>
```bash
{output.decode()}```''')

@app.on_message(filters.command('restart', prefixes=prefix) & filters.me)
async def res(client, message):
    await message.edit_text(f'<emoji id=5258420634785947640>🔄</emoji> <code>Перезапускаюсь...</code>')
    restart()

@app.on_message(filters.command(["eval", 'e'], prefixes=prefix) & filters.me)
async def ev(client, message):
    	code = message.text.strip()
    	code = code.replace(f"{prefix}eval ", "").replace(f"{prefix}e ", "")
    	try:
    	   f = StringIO()
    	   with redirect_stdout(f):
    	   	exec(code)
    	   out = f.getvalue()
    	   return await message.edit_text(f'''<emoji id=5339181821135431228>💻</emoji> <b>Код:</b>
```python
{code}```

<emoji id=5175061663237276437>🐍</emoji> <b>Вывод:</b>
```python
{str(out).replace(">", "").replace("<", "")}```''')
    	except Exception as ex:
    		return await message.edit_text(f'''<emoji id=5339181821135431228>💻</emoji> <b>Код:</b>
```python
{code}```

<emoji id=5237993272109967450>❌</emoji> <b>Ошибка:</b>
```python
{str(ex).replace(">", "").replace("<", "")}```''')
#await message.reply(str(out).replace("<", "").replace(">", ""))
#await message.reply(str(ex).replace(">", "").replace("<", ""))

@app.on_message(filters.command("unpmbl", prefixes=prefix) & filters.me)
async def unpmbl(client, message):
    try:
        if message.reply_to_message:
            id = message.reply_to_message.from_user.id
            name = message.reply_to_message.from_user.first_name
        else:
            id = message.text.split()[1]
            user = await app.get_users(id)
            name = user.first_name
    except Exception as e:
        await message.edit_text(f"<emoji id=5237993272109967450>❌</emoji> Произошла ошибка: {e}")
        return

    if isinstance(id, int):
    	pass
    else:
    	try:
    		i = id.replace("@", '')
    		i = id.replace("https://t.me/", '')
    		id = await get_user_id(i)
    	except Exception as e:
    		await message.edit_text(f'<emoji id=5237993272109967450>❌</emoji> Не удалось разблокировать пользователя в ЛС: {e}')
    		return
    
    await app.unblock_user(id)
    await message.edit_text(f'<emoji id=5472180551517477902>✅</emoji> <b>{name}</b> был убран из ЧС!')

@app.on_message(filters.command("pmbl", prefixes=prefix) & filters.me)
async def pmbl(client, message):
    try:
        if message.reply_to_message:
            id = message.reply_to_message.from_user.id
            name = message.reply_to_message.from_user.first_name
        else:
            id = message.text.split()[1]
            user = await app.get_users(id)
            name = user.first_name
    except Exception as e:
        await message.edit_text(f"<emoji id=5237993272109967450>❌</emoji> Произошла ошибка: {e}")
        return

    if isinstance(id, int):
    	pass
    else:
    	try:
    		i = id.replace("@", '')
    		i = id.replace("https://t.me/", '')
    		id = await get_user_id(i)
    	except Exception as e:
    		await message.edit_text(f'<emoji id=5237993272109967450>❌</emoji> Не удалось заблокировать пользователя в ЛС: {e}')
    		return
    
    await app.block_user(id)
    await message.edit_text(f'<emoji id=5472030751648127392>🛑</emoji> <b>{name}</b> был добавлен(-а) в ЧС!')

@app.on_message(filters.command("unpin", prefixes=prefix) & filters.me)
async def unpin(client, message):
	chat_id = message.chat.id
	if message.reply_to_message:
		message_id = message.reply_to_message.id
		await app.unpin_chat_message(chat_id, message_id)
		await message.edit_text('<emoji id=5258461531464539536>📌</emoji> Сообщение успешно откреплено!')
	else:
		await message.edit_text(f"<emoji id=5237993272109967450>❌</emoji> Команда должна быть ответом на сообщение!")

@app.on_message(filters.command("pin", prefixes=prefix) & filters.me)
async def pin(client, message):
	chat_id = message.chat.id
	if message.reply_to_message:
		message_id = message.reply_to_message.id
		await app.pin_chat_message(chat_id, message_id)
		await message.edit_text('<emoji id=5258461531464539536>📌</emoji> Сообщение успешно закреплено!')
	else:
		await message.edit_text(f"<emoji id=5237993272109967450>❌</emoji> Команда должна быть ответом на сообщение!")
	
@app.on_message(filters.command("leave", prefixes=prefix) & filters.me)
async def leave(client, message):
    try:
    	id_chat = message.text.split()[1]
    except:
    	await message.edit_text(f"<emoji id=5237993272109967450>❌</emoji> Произошла ошибка: {e}")
    	return

    if isinstance(id_chat, int):
    	pass
    else:
    	try:
    		i = id_chat.replace("@", '')
    		i = id_chat.replace("https://t.me/", '')
    		id = await get_chat_id(i)
    	except Exception as e:
    		await message.edit_text(f'<emoji id=5237993272109967450>❌</emoji> Не удалось выйти с чата: {e}')
    		return
    
    await app.leave_chat(id)
    await message.edit_text(f'<emoji id=5474371208176737086>✉️</emoji> Вы вышли с чата {id_chat}!')

@app.on_message(filters.command("join", prefixes=prefix) & filters.me)
async def join(client, message):
    try:
    	id_chat = message.text.split()[1]
    except:
    	await message.edit_text(f"<emoji id=5237993272109967450>❌</emoji> Произошла ошибка: {e}")
    	return

    if isinstance(id_chat, int):
    	pass
    else:
    	try:
    		i = id_chat.replace("@", '')
    		i = id_chat.replace("https://t.me/", '')
    		id = await get_chat_id(i)
    	except Exception as e:
    		await message.edit_text(f'<emoji id=5237993272109967450>❌</emoji> Не удалось вступить в чат: {e}')
    		return
    
    await app.join_chat(id)
    await message.edit_text(f'<emoji id=5474371208176737086>✉️</emoji> Вы вступили в чат {id_chat}!')

@app.on_message(filters.command("unban", prefixes=prefix) & filters.me)
async def unban(client, message):
    chat_id = message.chat.id
    try:
        if message.reply_to_message:
            id = message.reply_to_message.from_user.id
            name = message.reply_to_message.from_user.first_name
            reason = " ".join(message.text.split()[1:])
        else:
            id = message.text.split()[1]
            user = await app.get_users(id)
            name = user.first_name
            reason = " ".join(message.text.split()[2:])
    except Exception as e:
        await message.edit_text(f"<emoji id=5237993272109967450>❌</emoji> Произошла ошибка: {e}")
        return

    if not reason:
        t = ''
    else:
        t = f'Причина » <i>{reason}</i>'

    if isinstance(id, int):
    	pass
    else:
    	try:
    		i = id.replace("@", '')
    		i = id.replace("https://t.me/", '')
    		id = await get_user_id(i)
    	except Exception as e:
    		await message.edit_text(f'<emoji id=5237993272109967450>❌</emoji> Не удалось разблокировать пользователя: {e}')
    		return
    
    try:
        await client.unban_chat_member(chat_id, id)
    except Exception as e:
        await message.edit_text(f'<emoji id=5237993272109967450>❌</emoji> Не удалось разблокировать пользователя: {e}')
        return
    await message.edit_text(f'<emoji id=5472100935708711380>👍</emoji> <b>{name}</b>, разблокирован! {t}')

@app.on_message(filters.command("ban", prefixes=prefix) & filters.me)
async def ban(client, message):
    chat_id = message.chat.id
    try:
        if message.reply_to_message:
            id = message.reply_to_message.from_user.id
            name = message.reply_to_message.from_user.first_name
            time = int(message.text.split()[1])
            date = message.text.split()[2]
            reason = " ".join(message.text.split()[3:])
        else:
            id = message.text.split()[1]
            user = await app.get_users(id)
            name = user.first_name
            time = int(message.text.split()[2])
            date = message.text.split()[3]
            reason = " ".join(message.text.split()[4:])
    except Exception as e:
        await message.edit_text(f"<emoji id=5237993272109967450>❌</emoji> Произошла ошибка: {e}")
        return

    if not reason:
        t = ''
    else:
        t = f'Причина » <i>{reason}</i>'
    
    if isinstance(id, int):
    	pass
    else:
    	try:
    		i = id.replace("@", '')
    		i = id.replace("https://t.me/", '')
    		id = await get_user_id(i)
    	except Exception as e:
    		await message.edit_text(f'<emoji id=5237993272109967450>❌</emoji> Не удалось заблокировать пользователя: {e}')
    		return
    
    if date in ['м', 'минут', 'минута', 'мин', 'm', 'min', 'minute', 'minutes']:
    	dt = datetime.now() + timedelta(minutes=time)
    	d = 'минут'
    elif date in ['часов', 'час', 'часа', 'h', 'ч' 'hours', 'hour']:
    	dt = datetime.now() + timedelta(hours=time)
    	d = 'часов'
    elif date in ['д', 'дней', 'день', 'дня', 'days', 'day', "d"]:
    	dt = datetime.now() + timedelta(days=time)
    	d = 'дней'
    else:
    	await message.edit_text('<emoji id=5237993272109967450>❌</emoji> <b>Не верно введены аргументы!</b>')
    	return
    	
    full_time_dt = dt.timestamp()
    full_time = datetime.fromtimestamp(full_time_dt)
    try:
        await app.ban_chat_member(chat_id, id, until_date=full_time)
    except Exception as e:
        await message.edit_text(f'<emoji id=5237993272109967450>❌</emoji> Не удалось заблокировать пользователя: {e}')
        return

    await message.edit_text(f'<emoji id=5472267631979405211>🚫</emoji> <b>{name}</b>, заблокирован на <i>{time} {d}</i>. {t}')

@app.on_message(filters.command("unmute", prefixes=prefix) & filters.me)
async def unmute(client, message):
    chat_id = message.chat.id
    try:
        if message.reply_to_message:
            id = message.reply_to_message.from_user.id
            name = message.reply_to_message.from_user.first_name
            reason = " ".join(message.text.split()[1:])
        else:
            id = message.text.split()[1]
            user = await app.get_users(id)
            name = user.first_name
            reason = " ".join(message.text.split()[2:])
    except Exception as e:
        await message.edit_text(f"<emoji id=5237993272109967450>❌</emoji> Произошла ошибка: {e}")
        return

    if not reason:
        t = ''
    else:
        t = f'Причина » <i>{reason}</i>'

    if isinstance(id, int):
    	pass
    else:
    	try:
    		i = id.replace("@", '')
    		i = id.replace("https://t.me/", '')
    		id = await get_user_id(i)
    	except Exception as e:
    		await message.edit_text(f'<emoji id=5237993272109967450>❌</emoji> Не удалось размутить пользователя: {e}')
    		return
    
    try:
        await client.restrict_chat_member(chat_id, id, ChatPermissions(can_send_messages=True))
    except Exception as e:
        await message.edit_text(f'<emoji id=5237993272109967450>❌</emoji> Не удалось размутить пользователя: {e}')
        return

    await message.edit_text(f'<emoji id=5472100935708711380>👍</emoji> <b>{name}</b>, размучен! {t}')

@app.on_message(filters.command("mute", prefixes=prefix) & filters.me)
async def mute(client, message):
    chat_id = message.chat.id
    try:
        if message.reply_to_message:
            id = message.reply_to_message.from_user.id
            name = message.reply_to_message.from_user.first_name
            time = int(message.text.split()[1])
            date = message.text.split()[2]
            reason = " ".join(message.text.split()[3:])
        else:
            id = message.text.split()[1]
            user = await app.get_users(id)
            name = user.first_name
            time = int(message.text.split()[2])
            date = message.text.split()[3]
            reason = " ".join(message.text.split()[4:])
    except Exception as e:
        await message.edit_text(f"<emoji id=5237993272109967450>❌</emoji> Произошла ошибка: {e}")
        return

    if not reason:
        t = ''
    else:
        t = f'Причина » <i>{reason}</i>'
    
    if isinstance(id, int):
    	pass
    else:
    	try:
    		i = id.replace("@", '')
    		i = id.replace("https://t.me/", '')
    		id = await get_user_id(i)
    	except Exception as e:
    		await message.edit_text(f'<emoji id=5237993272109967450>❌</emoji> Не удалось ограничить пользователя: {e}')
    		return
    		
    if date in ['м', 'минут', 'минута', 'мин', 'm', 'min', 'minute', 'minutes']:
    	dt = datetime.now() + timedelta(minutes=time)
    	d = 'минут'
    elif date in ['часов', 'час', 'часа', 'h', 'ч' 'hours', 'hour']:
    	dt = datetime.now() + timedelta(hours=time)
    	d = 'часов'
    elif date in ['д', 'дней', 'день', 'дня', 'days', 'day']:
    	dt = datetime.now() + timedelta(days=time)
    	d = 'дней'
    else:
    	await message.edit_text('<emoji id=5237993272109967450>❌</emoji> <b>Не верно введены аргументы!</b>')
    	return

    full_time_dt = dt.timestamp()
    full_time = datetime.fromtimestamp(full_time_dt)
    try:
        await client.restrict_chat_member(chat_id, id, ChatPermissions(), until_date=full_time)
    except Exception as e:
        await message.edit_text(f'<emoji id=5237993272109967450>❌</emoji> Не удалось ограничить пользователя: {e}')
        return

    await message.edit_text(f'<emoji id=5460662076294831027>🤐</emoji> <b>{name}</b>, замучен на <i>{time} {d}</i>. {t}')

@client.on_message(filters.command("ping", prefixes=prefix))
async def ping(client, message):
	a = time.time()
	m = await message.edit_text(f'🌙')
	if m:
		b = time.time()
		end_time = time.time() - start_time
		hours, rem = divmod(end_time, 3600)
		minutes, seconds = divmod(rem, 60)
		await m.edit_text(f'🌙 Пинг: <b>{round((b - a) * 1000)}</b> ms\n<emoji id=5431449001532594346>⚡️</emoji> Прошло времени с момента запуска: <b>{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}</b>')

@client.on_message(filters.command("spam", prefixes=prefix))
async def ping(client, message):
	try:
		count = int(message.text.split()[1])
		if message.reply_to_message:
			text = message.reply_to_message.text
		else:
			text = " ".join(message.text.split()[2:])
	except:
		await message.edit_text(f"<emoji id=5237993272109967450>❌</emoji> Произошла ошибка: {e}")
		return
	chat_id = message.chat.id
	await message.edit_text(text)
	for i in range(count-1):
		await app.send_message(chat_id, text)
		
@client.on_message(filters.command("help", prefixes=prefix))
async def help(client, message):
    await message.edit_text(help_text)
    
@app.on_message()
async def all(client, message):
	if '-100' in str(message.chat.id):
		return
	else:
		cursor.execute("INSERT INTO messages VALUES(?, ?, ?);", (message.id, message.from_user.id, message.text))
		connect.commit()

if __name__ == "__main__":
	client.run()