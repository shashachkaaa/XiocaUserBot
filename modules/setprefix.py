from utils.imports import *
from utils.func import *
from utils.misc import *

@Client.on_message(filters.command('setprefix', prefixes=prefix) & filters.me)
async def setprefix(client, message):
	qu = " ".join(message.text.split()[1:])
	if len(qu) >= 2:
		return await message.edit_text(f'<emoji id=5237993272109967450>❌</emoji> <b>Префикс не может быть больше 1 символа!</b>')
	
	await message.edit_text(f'<emoji id=5237907553152672597>✅</emoji> <b>Префикс "{qu}" успешно установлен! Xioca перезагружается для установки префикса</b>')
	db.set(
        "core.updater",
        "restart_info",
        {
            "type": "setpref",
            "chat_id": message.chat.id,
            "message_id": message.id,
            "last_time": time.time()
        },
    )
	db.set("core.main", "prefix", qu)
	restart()

modules_help["setprefix"] = {
	f"setprefix [префикс]": "Установить префикс команд"
}