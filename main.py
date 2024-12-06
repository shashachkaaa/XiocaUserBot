from utils.imports import *
from utils.func import *
from utils.texts import *
from commands import *

try:
    with open("user_data.txt", "r") as file:
        api_id = file.readline().strip()
        api_hash = file.readline().strip()
        
        api_id = api_id.replace(f'api_id=', '')
        api_hash = api_hash.replace(f'api_hash=', '')
        api_id  = int(api_id[0])
        api_hash = str(api_hash[0])
        
except FileNotFoundError:
    api_id = int(input("Введите ваш API ID: "))
    api_hash = input("Введите ваш API HASH: ")

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
            logging.warning("Файл с сессией заблокирован!")
            subprocess.run(['rm', '-rf', 'session.session', 'user_data.txt'])
            restart()
        raise
    except (errors.NotAcceptable, errors.Unauthorized) as e:
        logging.error(f"{e.__class__.__name__}: {e}")
        os.rename("session.session", "session.session-old")
        restart()
        
    await idle()
    await app.stop()

authed = client.authorize()

if authed:
    print("Пользователь авторизован!")
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
print(Fore.YELLOW + Style.BRIGHT + start_art)
print(Fore.YELLOW + Style.BRIGHT + pyfiglet.figlet_format('xioca', font = 'starwars') + Fore.WHITE)
print(Fore.YELLOW + Style.BRIGHT + '            XIOCA HAS STARTED' + Fore.WHITE)

path = "commands"
module = importlib.import_module(path)

for name, obj in vars(module).items():
    if type(getattr(obj, "handlers", [])) == list:
        for handler, group in getattr(obj, "handlers", []):
            client.add_handler(handler, group)

if __name__ == "__main__":
	app.run(main())