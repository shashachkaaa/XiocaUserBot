from utils.imports import *
from utils.func import *
from utils.misc import *

BASE_PATH = os.path.abspath(os.getcwd())

@Client.on_message(filters.command(["loadmod", "lm"], prefix) & filters.me)
async def loadmod(client, message):
    try:
    	r = message.reply_to_message.document
    except:
    	return await message.edit("<emoji id=5238224607638468926>❓</emoji> <b>Что устанавливать?</b>")
    if r is None:
        return await message.edit_text('<emoji id=5237993272109967450>❌</emoji> <b>Команда должна быть ответом на файл!</b>')
    
    if '.py' in r.file_name:
    	pass
    else:
    	return await message.edit_text('<emoji id=5237993272109967450>❌</emoji> <b>Файл должен быть в формате .py</b>')

    module_name = r.file_name
    name = module_name.replace('.py', '')
    await message.edit_text(f'<emoji id=5210696719129392502>🔧</emoji> <b>Устанавливаю модуль <code>{name}</code></b>')

    if os.path.exists(f"./modules/custom_modules/{module_name}"):
        await unload_module(module_name, client)
    
    await client.download_media(r.file_id, file_name=f'./modules/custom_modules/{module_name}')
    
    try:
        await load_module(name, client, message)
    except Exception as e:
        os.remove(f"./modules/custom_modules/{module_name}")
        return await message.edit(format_exc(e))
    
    try:
    	await message.edit_text(f"<b><emoji id=5237907553152672597>✅</emoji> Модуль <code>{name}</code> успешно установлен!</b>\n\n{module_help(name, False)}")
    except Exception as e:
    	await message.edit(format_exc(e))
    	os.remove(f"./modules/custom_modules/{module_name}")

@Client.on_message(filters.command(["unloadmod", "unlm"], prefix) & filters.me)
async def unload_mods(client: Client, message: Message):
    if len(message.command) <= 1:
        return await message.edit("<emoji id=5238224607638468926>❓</emoji> Что выгружать?")

    module_name = message.command[1].lower()

    if os.path.exists(f"{BASE_PATH}/modules/custom_modules/{module_name}.py"):
        try:
            await unload_module(module_name, client)
        except Exception as e:
            return await message.edit(format_exc(e))

        os.remove(f"{BASE_PATH}/modules/custom_modules/{module_name}.py")
        await message.edit(f'<emoji id=5258130763148172425>🗑</emoji> <b>Модуль <code>{module_name.replace(".py", "")}</code> успешно выгружен!</b>')
    elif os.path.exists(f"{BASE_PATH}/modules/{module_name}.py"):
        await message.edit('<emoji id=5364241851500997604>⚠️</emoji> <b>Вы пытаетесь выгрузить системный модуль, сделать это невозможно!!!</b>')
    else:
        await message.edit(f'<emoji id=5237993272109967450>❌</emoji> <b>Модуль {module_name} не найден</b>')

@Client.on_message(filters.command("ml", prefix) & filters.me)
async def ml(client, message):
	try:
		module_name = message.command[1].lower()
	except:
		return await message.edit('<emoji id=5237993272109967450>❌</emoji> <b>Введите название модуля</b>')
	
	if os.path.exists(f"{BASE_PATH}/modules/custom_modules/{module_name}.py"):
		await client.delete_messages(message.chat.id, message.id)
		await client.send_document(message.chat.id, document=f'{BASE_PATH}/modules/custom_modules/{module_name}.py', caption = f'<emoji id=5433653135799228968>📁</emoji> <b>Файл</b> <code>{module_name}</code>\n\n<emoji id=5372905603695910757>🌙</emoji> <code>.lm</code> <b>в ответ на это сообщение, чтобы установить модуль</b>')
	elif os.path.exists(f"{BASE_PATH}/modules/{module_name}.py"):
		await message.edit('<emoji id=5364241851500997604>⚠️</emoji> <b>Вы пытаетесь поделится системным модулем, сделать это невозможно!!!</b>')
	else:
		await message.edit(f'<emoji id=5237993272109967450>❌</emoji> <b>Модуль {module_name} не найден</b>')

modules_help["loader"] = {
	"lm [reply]": "Установить модуль",
	"unlm [модуль]": "Удалить модуль",
	"ml [модуль]": "Поделиться модулем"
}