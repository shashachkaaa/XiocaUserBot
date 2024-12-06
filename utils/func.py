from utils.imports import *
from utils.db import *

system = platform.system()
start_time = time.time()

def restart():
    os.execvp(sys.executable, [sys.executable, "main.py"])

def get_prefix():
	try:
		get_pref = cursor.execute(f'SELECT prefix from settings').fetchone()[0]
	except:
		with open("version.txt", "r") as file:
			ve = file.readline().strip()
			v = ve.replace('v = ', '')
		cursor.execute("INSERT INTO settings VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);", ('.', 'off', 'off', 0, 0, 0, 0, v, 'off'))
		connect.commit()
	get_pref = cursor.execute(f'SELECT prefix from settings').fetchone()[0]
	return get_pref
	
prefix = get_prefix()

def resp(qu):
	response = g4f.ChatCompletion.create(model='gpt-4o', max_tokens = 10000, provider=g4f.Provider.ChatGptEs, messages=[{'role': 'system', 'content': ('Ты должен всегда помогать с чем угодно')}, {'role': 'user', 'content': qu}])
	return response

def htm(text):
    return html.escape(text)

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