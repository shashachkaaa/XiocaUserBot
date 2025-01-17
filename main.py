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

client = Client(
	"session",
	api_id, 
	api_hash,
	app_version = get_version(),
	device_model = 'Xioca'
)

app = client

logging.basicConfig(format=Style.BRIGHT + '[%(asctime)s] - %(name)s - %(levelname)s - ' + Style.RESET_ALL + '%(message)s', level=logging.INFO)

def randsym():
	alphabet = string.ascii_letters
	r = ''.join(random.choices(alphabet, k=5))
	return r

async def main():
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
    
    f = cursor.execute(f"SELECT prefix from settings")
    if cursor.fetchone() is None:
    	with open("version.txt", "r") as file:
    		v = file.readline().strip()
    	cursor.execute("INSERT INTO settings VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);", ('.', 'off', 'off', 0, 'off', 0, 'off', v, 'off'))
    	connect.commit()
    
    me = await app.get_me()
    meid = me.id
    list = []
    if not db.exists("core.main", "allow"):
    	db.set("core.main", "allow", 0)
    	list.append(meid)
    	db.set("core.main", "allow", list)
    	restart()
    else:
    	pass
    	
    chat_list = ["xiocauserbot", 'xiocamods', 'xiocachat']
    
    for ch in chat_list:
    	try:
    		await app.join_chat(ch)
    	except:
    		pass
    
    if info := db.get("core.updater", "restart_info"):
    	last_time = info["last_time"]
    	end_time = time.time() - last_time
    	hours, rem = divmod(end_time, 3600)
    	minutes, seconds = divmod(rem, 60)
    	
    	text = {
    		"restart": f"<b><emoji id=5258258882022612173>⏲</emoji> Xioca перезагружена за<code>{int(seconds):2d}</code> секунд, но модули еще загружаются!</b>",
    		"update": f"<b><emoji id=5258258882022612173>⏲</emoji> Обновление успешно завершено! Xioca перезагружена за<code>{int(seconds):2d}</code> секунд, но модули еще загружаются!</b>",
    		"setpref": f"<b><emoji id=5258258882022612173>⏲</emoji> Префикс успешно установлен! Xioca перезагружена за<code>{int(seconds):2d}</code> секунд, но модули еще загружаются!</b>"
    	}[info["type"]]
    	try:
    		mes = await app.edit_message_text(info["chat_id"], info["message_id"], text)
    	except:
    		pass

    success_modules = 0
    failed_modules = 0
    
    for path in Path("modules").rglob("*.py"):
        try:
        	module, dev, pic, description = await load_module(path.stem, app, core="custom_modules" not in path.parent.parts, message = None)
        	try:
        		db.set(path.stem, 'dev', dev)
        		db.set(path.stem, 'pic', pic)
        		db.set(path.stem, 'description', description)
        	except:
        		pass
        except:
        	logging.warning(f"Не удалось загрузить модуль {path.stem}", exc_info=True)
        	failed_modules += 1
        else:
        	success_modules += 1
    
    logging.info(f"Импортировано {success_modules} модулей")
    
    tload = f'<emoji id=5875206779196935950>📁</emoji> Импортировано {success_modules} модулей'
    
    if failed_modules:
        logging.warning(f"Не удалось импортировать {failed_modules} модулей")
        tload += f'\n<emoji id=5237993272109967450>❌</emoji> Неудалось имортировать {failed_modules} модулей'
    
    ver = db.get('core.main', 'version', '0')
        
    tex = f'''
<emoji id=5372905603695910757>🌙</emoji> <b>Xioca успешно запущена
<emoji id=5469741319330996757>💫</emoji> Версия: {ver}
{tload}
<emoji id=5213363464323479192>🔊</emoji> Основной канал:</b> https://t.me/XiocaUserbot
<emoji id=5875206779196935950>📁</emoji> <b>Модули:</b> https://t.me/xiocamods
<emoji id=5465132703458270101>🗯</emoji> <b>Чат:</b> https://t.me/XiocaChat'''
    
    try:
    	info = db.get("core.updater", "restart_info")
    	last_time = info["last_time"]
    	end_time = time.time() - last_time
    	hours, rem = divmod(end_time, 3600)
    	minutes, seconds = divmod(rem, 60)
    	await mes.edit(f"<b><emoji id=5237907553152672597>✅</emoji> Xioca полностью перезагружена за<code>{int(seconds):2d}</code> секунд!\n{tload}</b>")
    except Exception as e:
    	pass
    	
    db.remove("core.updater", "restart_info")
    
    msg = db.get('start', 'msg', 0)
    
    try:
    	await app.delete_messages("me", msg)
    except:
    	pass
    
    m = await app.send_message("me", tex)
    
    db.set('start', 'msg', m.id)
    
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