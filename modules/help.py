from utils.imports import *
from utils.func import *
from utils.misc import *

@Client.on_message(filters.command(["help", "h"], prefix) & filters.user(allowed))
async def help_cmd(_, message: Message):
    if len(message.command) == 1:
        msg_edited = False
        text = (f'''<b><emoji id=5372905603695910757>🌙</emoji> Помощь по юзерботу Xioca
Всего модулей: {round(int(len(modules_help) / 1))}\n\n</b>''')

        for module_name, module_commands in sorted(
            modules_help.items(), key=lambda x: x[0], reverse=True
        ):
            text += "<emoji id=4971987363145188045>▫️</emoji> <b>{}:</b> {}\n".format(
                module_name.title(),
                " | ".join(
                    [
                        f"<code>{prefix + cmd_name.split()[0]}</code>"
                        for cmd_name in module_commands.keys()
                    ]
                ),
            )

            if len(text) >= 4096:
                text += "</b>"
                if msg_edited:
                    await answer(message, text)
                else:
                    await answer(message, text)
                    msg_edited = True
                text = "<b>"

        if msg_edited:
            await answer(message, text)
        else:
            await answer(message, text)
    elif message.command[1].lower() in modules_help:
        dev = db.get(message.command[1].lower(), 'dev', '')
        pic = db.get(message.command[1].lower(), 'pic', '')
        description = db.get(message.command[1].lower(), 'description', '')
        	
        helptext = module_help(message.command[1].lower(), True, dev, description)
        
        if pic == '':
        	await answer(message, helptext)
        else:
        	await answer(message, photo=True, chat_id=message.chat.id, response=pic, caption=helptext)
    else:
        command_name = message.command[1].lower()
        for name, commands in modules_help.items():
            for command in commands.keys():
                if command.split()[0].lower() == command_name:
                    cmd = command.split(maxsplit=1)
                    cmd_desc = commands[command]
                    return await answer(message, f'''<emoji id=5372905603695910757>🌙</emoji> Помощь по модулю <code>{name}</code></b>

<emoji id=4971987363145188045>▫️</emoji> <code>{prefix}{cmd[0]}</code> {' <code>' + cmd[1] + '</code>' if len(cmd) > 1 else ''} — <i>{cmd_desc}</i>''')
        matches = process.extract(command_name, modules_help.keys(), limit=3)
        
        best_module_name = []
        
        if matches[0][1] < 100:
        	for best in matches:
        		best_module_name.append(best[0])
        else:
        	return await answer(message, f"<emoji id=5237993272109967450>❌</emoji> <b>Модуль {command_name} отсутствует</b>")
        
        dev = db.get(best_module_name[0], 'dev', '')
        pic = db.get(best_module_name[0], 'pic', '')
        description = db.get(best_module_name[0], 'description', '')
        
        helptext = module_help(best_module_name[0], True, dev, description, True)
        
        if pic == '':
        	await answer(message, helptext)
        else:
        	await answer(message, photo=True, chat_id=message.chat.id, response=pic, caption=helptext)

modules_help["help"] = {
    "help [модуль/команда]": "Получить информацию по модулю"
}