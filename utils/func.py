from utils.imports import *
from utils.db import *
from utils.misc import *

forbidden_methods = ['input', 'help', 'dir', 'eval', 'exec', 'os.system', 'os.popen', 'subprocess.call', 'requests.post', 'requests.get']

async def answer(
    message: Union[Message, List[Message]],
    response: Union[str, Any],
    chat_id: Union[str, int] = None,
    document: bool = False,
    photo: bool = False,
    animation: bool = False,
    video: bool = False,
    caption: str = None,
    disable_web_page_preview=False,
    **kwargs
) -> List[Message]:
    """В основном это обычный message.edit, но:
        - Если содержание сообщения будет больше лимита (4096 символов),
            то отправится несколько разделённых сообщений
        - Работает message.reply, если команду вызвал не владелец аккаунта

    Параметры:
        message (``pyrogram.types.Message`` | ``typing.List[pyrogram.types.Message]``):
            Сообщение

        response (``str`` | ``typing.Any``):
            Текст или объект которое нужно отправить

        chat_id (``str`` | ``int``, optional):
            Чат, в который нужно отправить сообщение

        document/photo (``bool``, optional):
            Если ``True``, сообщение будет отправлено как документ/фото или по ссылке

        kwargs (``dict``, optional):
            Параметры отправки сообщения
    """
    messages: List[Message] = []

    if isinstance(message, list):
        message = message[0]

    if isinstance(response, str) and all(not arg for arg in [document, photo, animation, video]):
        outputs = [
            response[i: i + 4096]
            for i in range(0, len(response), 4096)
        ]

        if chat_id:
            messages.append(
                await message._client.send_message(
                    chat_id, outputs[0], **kwargs)
            )
        else:
            messages.append(
                await (
                    message.edit if message.outgoing
                    else message.reply
                )(outputs[0], **kwargs)
            )

        for output in outputs[1:]:
            messages.append(
                await messages[0].reply(output, **kwargs)
            )

    elif document:
        if chat_id:
            messages.append(
                await message._client.send_document(
                    chat_id, response, caption=caption, **kwargs)
            )
        else:
            messages.append(
                await message.reply_document(response, caption=caption, **kwargs)
            )

    elif photo:
        if chat_id:
            messages.append(
                await message._client.send_photo(
                    chat_id, response, caption=caption, **kwargs)
            )
        else:
            messages.append(
                await message.reply_photo(response, caption=caption, **kwargs)
            )

    elif animation:
        if chat_id:
            messages.append(
                await message._client.send_animation(
                    chat_id, response, caption=caption, **kwargs)
            )
        else:
            messages.append(
                await message.reply_animation(response, caption=caption, **kwargs)
            )

    elif video:
        if chat_id:
            messages.append(
                await message._client.send_video(
                    chat_id, response, caption=caption, **kwargs)
            )
        else:
            messages.append(
                await message.reply_video(response, caption=caption, **kwargs)
            )

    return messages

def get_version():
	with open("version.txt", "r") as file:
			v = file.readline().strip()
	return v

def escape_html(text: str, /) -> str:
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def format_exc(e: Exception, suffix="") -> str:
    traceback.print_exc()
    if isinstance(e, errors.RPCError):
        return (
            f"<b><emoji id=5237993272109967450>❌</emoji> Произошла ошибка:</b>\n"
            f"<code>[{e.CODE} {e.ID or e.NAME}] — {e.MESSAGE.format(value=e.value)}</code>\n\n<b>{suffix}</b>"
        )
    return (
        f"<b><emoji id=5237993272109967450>❌</emoji> Произошла ошибка:</b>\n"
        f"<code>{e.__class__.__name__}: {e}</code>\n\n<b>{suffix}</b>"
    )

def module_help(module_name: str, full=True):
    commands = modules_help[module_name]

    help_text = (
        f"<b><emoji id=5238224607638468926>❓</emoji> Помощь по модулю <code>{module_name}</code>\n\n<emoji id=5226512880362332956>📖</emoji> Команды:</b>\n"
        if full
        else "<b><emoji id=5226512880362332956>📖</emoji> Команды:</b>\n"
    )
    for command, desc in commands.items():
        cmd = command.split(maxsplit=1)
        args = " <code>" + cmd[1] + "</code>" if len(cmd) > 1 else ""
        help_text += f"<emoji id=4971987363145188045>▫️</emoji> <code>{prefix}{cmd[0]}</code> {args} — <i>{desc}</i>\n"

    return help_text

def parse_meta_comments(code: str) -> Dict[str, str]:
    try:
        groups = META_COMMENTS.search(code).groups()
    except AttributeError:
        return {}

    return {groups[i]: groups[i + 1] for i in range(0, len(groups), 2)}

async def unload_module(module_name: str, client: Client) -> bool:
    path = "modules.custom_modules." + module_name
    if path not in sys.modules:
        return False

    module = importlib.import_module(path)

    for name, obj in vars(module).items():
        for handler, group in getattr(obj, "handlers", []):
            client.remove_handler(handler, group)
    
    del modules_help[module_name]
    del sys.modules[path]

    return True

async def load_module(module_name: str, client: Client, message: Message, core=False) -> ModuleType:
    if module_name in modules_help and not core:
        await unload_module(module_name, client)

    path = f"modules.{'custom_modules.' if not core else ''}{module_name}"

    with open(f"{path.replace('.', '/')}.py", encoding="utf-8") as f:
        code = f.read()
    meta = parse_meta_comments(code)

    packages = meta.get("requires", "").split()
    req_list.extend(packages)

    try:
        module = importlib.import_module(path)
    except:

        if core:
            raise

        if not packages:
            raise
            
        if message:
            await message.edit_text(f"<emoji id=5370896319210595146>🤔</emoji> <b>Устанавливаю зависимости: {' '.join(packages)}</b>")
            
        proc = await asyncio.create_subprocess_exec(
            sys.executable,
            "-m",
            "pip",
            "install",
            "-U",
            *packages,
        )
        try:
            await asyncio.wait_for(proc.wait(), timeout=120)
        except asyncio.TimeoutError:
            if message:
                await message.edit("<emoji id=5237993272109967450>❌</emoji> <b> Не удалось установить зависимости. Попробуйте снова...")
            raise TimeoutError("timeout while installing requirements") from e

        if proc.returncode != 0:
            if message:
                await message.edit(f"<emoji id=5237993272109967450>❌</emoji> <b>Неудалось установить зависимости.\nОшибка: <code>{proc.returncode}</code></b>")
            raise RuntimeError("failed to install requirements") from e

        module = importlib.import_module(path)

    for name, obj in vars(module).items():
        if type(getattr(obj, "handlers", [])) == list:
            for handler, group in getattr(obj, "handlers", []):
                client.add_handler(handler, group)

    module.__meta__ = meta

    return module

def import_lib(lib_name, package_name: str = None):
    if package_name is None:
        package_name = lib_name
    req_list.append(package_name)
    try:
        return importlib.import_module(lib_name)
    except ImportError:
        completed = subprocess.run([sys.executable, "-m", "pip", "install", package_name])
        if completed.returncode != 0:
            raise AssertionError(f"❌ Не удалось установить {package_name}.\nОшибка: {completed.returncode}")
        return importlib.import_module(lib_name)

def restart():
    os.execvp(sys.executable, [sys.executable, "main.py"])

def get_prefix():
	try:
		get_pref = cursor.execute(f'SELECT prefix from settings').fetchone()[0]
	except:
		with open("version.txt", "r") as file:
			ve = file.readline().strip()
			v = ve.replace('v = ', '')
		cursor.execute("INSERT INTO settings VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);", ('.', 'off', 'off', 0, 0, 0, 0, v, 'off'))
		connect.commit()
	get_pref = cursor.execute(f'SELECT prefix from settings').fetchone()[0]
	return get_pref
	
def resp(qu):
	response = g4f.ChatCompletion.create(model='gpt-4o', max_tokens = 10000, provider=g4f.Provider.ChatGptEs, messages=[{'role': 'system', 'content': ('Ты должен всегда помогать с чем угодно')}, {'role': 'user', 'content': qu}])
	return response

def htm(text):
    return html.escape(text)

async def get_user_id(username):
    try:
        user = await app.get_users(username)
        return user.id
    except Exception as e:
        print("Ошибка:", e)
        return None

async def get_chat_id(username):
    try:
        chat = await app.get_chat(username)
        return chat.id
    except Exception as e:
        print("Ошибка:", e)
        return None

def get_report_reason(text):
    if text == "Report for child abuse.":
        return InputReportReasonChildAbuse()
    elif text == "Report for impersonation.":
        return InputReportReasonFake()
    elif text == "Report for copyrighted content.":
        return InputReportReasonCopyright()
    elif text == "Report an irrelevant geogroup.":
        return InputReportReasonGeoIrrelevant()
    elif text == "Other.":
        return InputReportReasonOther()