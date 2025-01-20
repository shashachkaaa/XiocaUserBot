from utils.imports import *
from utils.func import *
from utils.misc import *

BASE_PATH = os.path.abspath(os.getcwd())

@Client.on_message(filters.command(["loadmod", "lm"], prefix) & filters.user(allowed))
async def loadmod(client, message):
    try:
    	r = message.reply_to_message.document
    except:
    	return await answer(message, "<emoji id=5238224607638468926>❓</emoji> <b>Что устанавливать?</b>")
    if r is None:
        return await answer(message, '<emoji id=5237993272109967450>❌</emoji> <b>Команда должна быть ответом на файл!</b>')
    
    if '.py' in r.file_name:
    	pass
    else:
    	return await answer(message, '<emoji id=5237993272109967450>❌</emoji> <b>Файл должен быть в формате .py</b>')

    module_name = r.file_name
    name = module_name.replace('.py', '')
    ms = await answer(message, f'<emoji id=5210696719129392502>🔧</emoji> <b>Устанавливаю модуль <code>{name}</code></b>')

    if os.path.exists(f"./modules/custom_modules/{module_name}"):
        await unload_module(module_name, client)
    
    await client.download_media(r.file_id, file_name=f'./modules/custom_modules/{module_name}')
    
    try:
        try:
        	module, dev, pic, description = await load_module(name, client, message)
        except TypeError:
        	return
    except Exception as e:
        os.remove(f"./modules/custom_modules/{module_name}")
        return await answer(ms, format_exc(e))
        
    installed = f"<b><emoji id=5237907553152672597>✅</emoji> Модуль <code>{name}</code> успешно установлен!</b>\n{module_help(name, False, dev, description)}"
    
    db.set(name, 'dev', dev)
    db.set(name, 'pic', pic)
    db.set(name, 'description', description)
    
    try:
    	if pic == '':
    		await answer(ms, installed)
    	else:
    		await answer(ms, photo=True, chat_id=ms[0].chat.id, response=pic, caption=installed)
    except Exception as e:
    	await answer(ms, format_exc(e))
    	os.remove(f"./modules/custom_modules/{module_name}")

@Client.on_message(filters.command(["unloadmod", "unlm"], prefix) & filters.user(allowed))
async def unload_mods(client: Client, message: Message):
    if len(message.command) <= 1:
        return await answer(message, "<emoji id=5238224607638468926>❓</emoji> <b>Что выгружать?</b>")

    module_name = message.command[1].lower()
    
    matches = process.extract(module_name, modules_help.keys(), limit=3)
    
    best_module_name = []
    
    if matches[0][1] < 100:
    	for best in matches:
    		best_module_name.append(best[0])
    
    try:
    	module_name = best_module_name[0]
    	nm = '<emoji id=5312383351217201533>⚠️</emoji> <b>Точного совпадения не найдено, поэтому применен ближайший результат</b>'
    except:
    	module_name = message.command[1].lower()
    	nm = ''
    
    if os.path.exists(f"{BASE_PATH}/modules/custom_modules/{module_name}.py"):
        try:
            await unload_module(module_name, client)
            db.drop_table(module_name)
        except Exception as e:
            return await answer(message, format_exc(e))

        os.remove(f"{BASE_PATH}/modules/custom_modules/{module_name}.py")
        await answer(message, f'<emoji id=5258130763148172425>🗑</emoji> <b>Модуль <code>{module_name.replace(".py", "")}</code> успешно выгружен!</b>\n\n{nm}')
    elif os.path.exists(f"{BASE_PATH}/modules/{module_name}.py"):
        await answer(message, f'<emoji id=5312383351217201533>⚠️</emoji> <b>Вы пытаетесь выгрузить системный модуль {module_name}, сделать это невозможно!\n\n{nm}</b>')
    else:
        await answer(message, f'<emoji id=5237993272109967450>❌</emoji> <b>Модуль {module_name} не найден</b>')
        
@Client.on_message(filters.command("ml", prefix) & filters.user(allowed))
async def ml(client, message):
	try:
		module_name = message.command[1].lower()
	except:
		return await answer(message, '<emoji id=5237993272109967450>❌</emoji> <b>Введите название модуля</b>')
	
	matches = process.extract(module_name, modules_help.keys(), limit=3)
    
	best_module_name = []
    
	if matches[0][1] < 100:
		for best in matches:
			best_module_name.append(best[0])
    
	try:
		module_name = best_module_name[0]
		nm = '<emoji id=5312383351217201533>⚠️</emoji> <b>Точного совпадения не найдено, поэтому применен ближайший результат</b>'
	except:
		module_name = message.command[1].lower()
		nm = ''
	
	if os.path.exists(f"{BASE_PATH}/modules/custom_modules/{module_name}.py"):
		await answer(message, chat_id=message.chat.id, document=True, response=f'{BASE_PATH}/modules/custom_modules/{module_name}.py', caption = f'<emoji id=5433653135799228968>📁</emoji> <b>Файл</b> <code>{module_name}</code>\n\n<emoji id=5372905603695910757>🌙</emoji> <code>.lm</code> <b>в ответ на это сообщение, чтобы установить модуль</b>\n\n{nm}')
	elif os.path.exists(f"{BASE_PATH}/modules/{module_name}.py"):
		await answer(message, chat_id=message.chat.id, document=True, response=f'{BASE_PATH}/modules/{module_name}.py', caption = f'<emoji id=5433653135799228968>📁</emoji> <b>Файл</b> <code>{module_name}</code>\n\n<emoji id=5372905603695910757>🌙</emoji> <code>.lm</code> <b>в ответ на это сообщение, чтобы установить модуль</b>\n\n{nm}')
	else:
		await answer(message, f'<emoji id=5237993272109967450>❌</emoji> <b>Модуль {module_name} не найден</b>')

modules_help["loader"] = {
	"lm [reply]": "Установить модуль",
	"unlm [модуль]": "Удалить модуль",
	"ml [модуль]": "Поделиться модулем"
}