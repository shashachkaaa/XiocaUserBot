from utils.imports import *
from utils.func import *
from utils.misc import *

@Client.on_message(filters. command('update', prefixes=prefix) & filters.me)
async def update(client, message):
  await message.edit_text('<emoji id=5373310679241466020>🌀</emoji> <b>Проверка обновлений...</b>')
  try:
    subprocess.run("rm -rf version".txt, shell=True, capture_output=True)
    subprocess.run("wget https://raw.githubusercontent.com/shashachkaaa/XiocaUserBot/refs/heads/main/version.txt", shell=True, capture_output=True)
    with open("version.txt", "r") as file:
      v = file.readline().strip()
  except:
    await message.edit_text('<emoji id=5373310679241466020>🌀</emoji> <b>Установка пакетов...</b>')
    subprocess.run("pkg install wget -y", shell=True, capture_output=True)
    await message.edit_text('<emoji id=5373310679241466020>🌀</emoji> <b>Проверка обновлений...</b>')
    subprocess.run("wget https://raw.githubusercontent.com/shashachkaaa/XiocaUserBot/refs/heads/main/version.txt", shell=True, capture_output=True)

  ver = cursor.execute(f'SELECT version from settings').fetchone()[0]
  with open("version.txt", "r") as file:
    ve = file.readline().strip()
  
  if ver == ve:
    return await message.edit_text('<emoji id=5260463209562776385>✅</emoji> <b>Обновления не найдены.</b>')
  else:
    await message.edit_text('<emoji id=5373310679241466020>🌀</emoji> <b>Устанавливаю обновление...</b>')
    cursor.execute(f'UPDATE settings SET version = "{ve}"')
    connect.commit()
    subprocess.run(['git', 'pull'])
    pip.main(['install', '-r', 'requirements.txt'])
    await message.edit_text('<emoji id=5260463209562776385>✅</emoji> <b>Обновления установлены. Xioca перезагружается для завершения обновления...</b>')
    db.set(
      "core.updater",
      "restart_info",
      {
          "type": "update",
          "chat_id": message.chat.id,
          "message_id": message.id,
          "last_time": time.time()
      },
    )
    restart()

@Client.on_message(filters.command('restart', prefixes=prefix) & filters.user(allowed))
async def res(client, message):
    mes = await answer(message, f'<emoji id=5258420634785947640>🔄</emoji> <b>Перезапускаюсь...</b>')
    db.set(
        "core.updater",
        "restart_info",
        {
            "type": "restart",
            "chat_id": message.chat.id,
            "message_id": mes[0].id,
            "last_time": time.time()
        },
    )
    restart()

modules_help["updater"] = {
	"update": "Обновить юзербота",
	"restart": "Перезапустить юзербота"
}