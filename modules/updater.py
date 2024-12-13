from utils.imports import *
from utils.func import *
from utils.misc import *

@Client.on_message(filters. command('update', prefixes=prefix) & filters.me)
async def update(client, message):
  await message.edit_text('<emoji id=5373310679241466020>🌀</emoji> <b>Проверка обновлений...</b>')
  try:
    subprocess.run("rm -rf version.txt", shell=True, capture_output=True)
    subprocess.run("wget https://raw.githubusercontent.com/shashachkaaa/XiocaUserBot/refs/heads/main/version.txt", shell=True, capture_output=True)
    with open("version.txt", "r") as file:
      v = file.readline().strip()
      v = v.replace('v = ', '')
  except:
    await message.edit_text('<emoji id=5373310679241466020>🌀</emoji> <b>Установка пакетов...</b>')
    subprocess.run("pkg install wget", shell=True, capture_output=True)
    await message.edit_text('<emoji id=5373310679241466020>🌀</emoji> <b>Проверка обновлений...</b>')
    subprocess.run("rm -rf version.txt", shell=True, capture_output=True)
    subprocess.run("wget https://raw.githubusercontent.com/shashachkaaa/XiocaUserBot/refs/heads/main/version.txt", shell=True, capture_output=True)

  ver = cursor.execute(f'SELECT version from settings').fetchone()[0]
  with open("version.txt", "r") as file:
    ve = file.readline().strip()
    v = ve.replace('v = ', '')
  
  if ver == v:
    return await message.edit_text('<emoji id=5260463209562776385>✅</emoji> <b>Обновления не найдены.</b>')
  else:
    await message.edit_text('<emoji id=5373310679241466020>🌀</emoji> <b>Устанавливаю обновление...</b>')
    cursor.execute(f'UPDATE settings SET version = "{v}"')
    connect.commit()
    # Исключить файлы/папки из обновления
    subprocess.run("wget --exclude=session.session --exclude=user_data.txt --exclude=db.db https://raw.githubusercontent.com/shashachkaaa/XiocaUserBot/refs/heads/main/*", shell=True, capture_output=True)
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

@Client.on_message(filters.command('restart', prefixes=prefix) & filters.me)
async def res(client, message):
    db.set(
        "core.updater",
        "restart_info",
        {
            "type": "restart",
            "chat_id": message.chat.id,
            "message_id": message.id,
            "last_time": time.time()
        },
    )
    await message.edit_text(f'<emoji id=5258420634785947640>🔄</emoji> <b>Перезапускаюсь...</b>')
    restart()

modules_help["updater"] = {
	"update": "Обновить юзербота",
	"restart": "Перезапустить юзербота"
}