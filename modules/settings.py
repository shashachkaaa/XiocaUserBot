from utils.imports import *
from utils.func import *
from utils.misc import *

@Client.on_message(filters.command('ownerlist', prefixes=prefix) & filters.user(allowed))
async def ownerlist(client, message):
	text = f'<emoji id=5778423822940114949>🛡</emoji> <b>Список пользователей, имеющих доступ к юзерботу:\n\n</b>'
	
	allo = db.get("core.main", "allow")
	num = 0
	for i in allo:
		num += 1
		text += f'<emoji id=4971987363145188045>▫️</emoji> <b><a href="tg://openmessage?user_id={i}">{num} Юзер</a></b> (<code>{i}</code>)\n'
	await answer(message, text)
		
@Client.on_message(filters.command('owneradd', prefixes=prefix) & filters.me)
async def owneradd(client, message):
	try:
		rid = message.reply_to_message.from_user.id
		name = message.reply_to_message.from_user.first_name
	except:
		return await answer(message, '<emoji id=5237993272109967450>❌</emoji> <b>Команда должна быть ответом на сообщение</b>')
		
	list = []
	allo = db.get("core.main", "allow")
	for i in allo:
		list.append(i)
		
	if rid in allo:
		return await answer(message, f'<emoji id=5237993272109967450>❌</emoji> <b>У {name} уже есть доступ к юзерботу!</b>')
	else:
		await answer(message, f'<emoji id=5778423822940114949>🛡</emoji> <b>{name} был выдан доступ к юзерботу! Xioca перезагружается для корректной настройки прав..</b>')
		db.set("core.main", "allow", 0)
		list.append(rid)
		db.set("core.main", "allow", list)
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
		restart()

@Client.on_message(filters.command('ownerrm', prefixes=prefix) & filters.me)
async def ownerrm(client, message):
	try:
		rid = message.reply_to_message.from_user.id
		name = message.reply_to_message.from_user.first_name
	except:
		return await answer(message, '<emoji id=5237993272109967450>❌</emoji> <b>Команда должна быть ответом на сообщение</b>')
		
	list = []
	allo = db.get("core.main", "allow")
	for i in allo:
		list.append(i)
	
	me = await client.get_me()
	meid = me.id
		
	if rid not in allo:
		return await answer(message, f'<emoji id=5237993272109967450>❌</emoji> <b>У {name} отсутствует доступ к юзерботу!</b>')
	else:
		if rid == meid:
			return await answer(message, f'<emoji id=5237993272109967450>❌</emoji> <b>Нельзя отнять доступ у самого себя!</b>')
		await answer(message, f'<emoji id=5778423822940114949>🛡</emoji> <b>У {name} отнят доступ к юзерботу! Xioca перезагружается для корректной настройки прав..</b>')
		db.set("core.main", "allow", 0)
		list.remove(rid)
		db.set("core.main", "allow", list)
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
		restart()

@Client.on_message(filters.command('setinfo', prefixes=prefix) & filters.user(allowed))
async def setinfo(client, message):
	try:
		qu = message.text
		qu = qu.replace(f'{prefix}setinfo ', "")
		if qu == 'off':
			db.set("core.main", 'type_info', "xioca")
			return await answer(message, f"<emoji id=5237907553152672597>✅</emoji> <b>Инфо успешно обновлено!</b>")
	except Exception as e:
		print(e)
		pass
		
	try:
		m = str(message.reply_to_message.media)
	except Exception as e:
		return await answer(message, '<emoji id=5237993272109967450>❌</emoji> <b>Команда должна быть ответом на фото, GIF или видео!</b>')

	msg = message.reply_to_message
	
	if m == 'MessageMediaType.PHOTO':
		type = "photo"
		id = msg.photo.file_id
	elif m == "MessageMediaType.ANIMATION":
		type = "animation"
		id = msg.animation.file_id
	elif m == "MessageMediaType.VIDEO":
		type = "video"
		id = msg.video.file_id
	else:
		return await answer(message, f'<emoji id=5237993272109967450>❌</emoji> <b>Команда должна быть ответом на фото, GIF или видео!</b> {m}')
	
	await answer(message, f"<emoji id=5237907553152672597>✅</emoji> <b>Инфо успешно обновлено!</b>")
	db.set("core.main", 'type_info', type)
	db.set('core.main', "info", id)	
		
@Client.on_message(filters.command('setprefix', prefixes=prefix) & filters.user(allowed))
async def setprefix(client, message):
	qu = " ".join(message.text.split()[1:])
	if len(qu) >= 2:
		return await answer(message, f'<emoji id=5237993272109967450>❌</emoji> <b>Префикс не может быть больше 1 символа!</b>')
	
	await answer(message, f'<emoji id=5237907553152672597>✅</emoji> <b>Префикс "{qu}" успешно установлен! Xioca перезагружается для установки префикса</b>')
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

modules_help["settings"] = {
	"owneradd [ответ]": "Выдать доступ к юзерботу",
	"ownerrm [ответ]": "Отнять доступ к юзерботу",
	"ownerlist": "Получить список пользователей, имеющих доступ к юзерботу",
	"setprefix [префикс]": "Установить префикс команд",
	"setinfo [ответ/off]": "Установить фото, GIF или видео на инфо"
}