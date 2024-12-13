from utils.imports import *
from utils.func import *
from utils.texts import *
from utils.misc import *

try:
    with open("user_data.txt", "r") as file:
        api_id = file.readline().strip()
        api_hash = file.readline().strip()
        
        api_id = api_id.replace(f'api_id=', '')
        api_hash = api_hash.replace(f'api_hash=', '')
        api_id  = int(api_id[0])
        api_hash = str(api_hash[0])
        
except FileNotFoundError:
    api_id = int(input(fade.fire("Введите ваш API ID: ")))
    api_hash = input(fade.fire("Введите ваш API HASH: "))

    with open("user_data.txt", "w") as file:
        file.write(f"api_id={api_id}\napi_hash='{api_hash}'")

client = Client("session", api_id, api_hash)
app = client
logging.basicConfig(level=logging.INFO)

async def main():
    logging.basicConfig(level=logging.INFO)
    DeleteAccount.__new__ = None

    try:
        await app.start()
    except sqlite3.OperationalError as e:
        if str(e) == "database is locked" and os.name == "posix":
            logging.warning(fade.fire("Файл с сессией заблокирован!"))
            subprocess.run(['rm', '-rf', 'session.session', 'user_data.txt'])
            restart()
        raise
    except (errors.NotAcceptable, errors.Unauthorized) as e:
        logging.error(f"{e.__class__.__name__}: {e}")
        os.rename("session.session", "session.session-old")
        os.rename("user_data.txt", "user_data.txt-old")
        restart()
    
    success_modules = 0
    failed_modules = 0
    
    for path in Path("modules").rglob("*.py"):
        try:
        	await load_module(path.stem, app, core="custom_modules" not in path.parent.parts, message = None)
        except:
        	logging.warning(f"Не удалось загрузить модуль {path.stem}", exc_info=True)
        	failed_modules += 1
        else:
        	success_modules += 1
    
    logging.info(f"Импортировано {success_modules} модулей")
    
    if failed_modules:
        logging.warning(f"Не удалось загрузить {failed_modules} модулей")
    
    f = cursor.execute(f"SELECT prefix from settings")
    print(f)
    if cursor.fetchone() is None:
    	with open("version.txt", "r") as file:
    		v = file.readline().strip()
    		v = v.replace('v = ', '')
    	cursor.execute("INSERT INTO settings VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);", ('.', 'off', 'off', 0, 'off', 0, 'off', v, 'off'))
    	connect.commit()
    
    if info := db.get("core.updater", "restart_info"):
    	last_time = info["last_time"]
    	end_time = time.time() - last_time
    	hours, rem = divmod(end_time, 3600)
    	minutes, seconds = divmod(rem, 60)
    	
    	text = {
    		"restart": f"<b><emoji id=5237907553152672597>✅</emoji> Xioca успешно перезагружена за <code>{int(seconds):02d}</code> секунд!</b>",
    		"update": f"<b><emoji id=5237907553152672597>✅</emoji> Обновление успешно завершено! Xioca перезагружена за <code>{int(seconds):02d}</code> секунд!</b>",
    		"setpref": f"<b><emoji id=5237907553152672597>✅</emoji> Префикс успешно установлен! Xioca перезагружена за <code>{int(seconds):02d}</code> секунд!</b>"
    	}[info["type"]]
    	try:
    		await app.edit_message_text(info["chat_id"], info["message_id"], text)
    	except:
    		pass
    	db.remove("core.updater", "restart_info")
    
    await idle()
    await app.stop()
    
try:
	authed = client.authorize()
except:
	pass

if authed:
    print(fade.fire("Пользователь авторизован!"))
else:
    phone_number = input(Fore.YELLOW + Style.BRIGHT + "Введите ваш номер телефона: ")
    code = client.send_code(phone_number)
    
    input_code = input(Fore.YELLOW + Style.BRIGHT + "Введите код подтверждения: ")

    client.sign_in(phone_number, input_code)

try:
	subprocess.call(['apt', 'install', 'ffmpeg', '-y'])
except:
	pass

if os.name == "nt":
        	os.system("cls")
else:
        	os.system("clear")
start_t = start_art + pyfiglet.figlet_format('xioca', font = 'starwars') +'\n            XIOCA HAS STARTED' + Fore.WHITE
print(fade.fire(start_t))

if __name__ == "__main__":
	app.run(main())