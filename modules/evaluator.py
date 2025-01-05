from utils.imports import *
from utils.func import *
from utils.misc import *

import traceback

meval = import_lib('meval')
from meval import meval

def getattrs(app: Client, message: types.Message):
        return {
            "message": message,
            "chat": message.chat,
            "user": message.from_user,
            "r": message.reply_to_message,
            "reply": message.reply_to_message,
            "ruser": getattr(message.reply_to_message, "from_user", None)
        }

@Client.on_message(filters.command(["eval", 'e'], prefixes=prefix) & filters.user(allowed))
async def ev(client, message: Message):
    	c = message.text
    	cod = c.replace(f"{prefix}eval ", "")
    	code = cod.replace(f"{prefix}e ", "")
    	try:
    	   result = await meval(code, globals(), **getattrs(client, message))
    	except Exception as ex:
    		return await answer(message, format_exc(ex))
    	
    	return await answer(message, f'''<emoji id=5339181821135431228>💻</emoji> <b>Код:</b>
<code>{code}</code>

<emoji id=5175061663237276437>🐍</emoji> <b>Вывод:</b>
<code>{html.escape(str(result))}</code>''')
    	

modules_help['evaluator'] = {
	"eval/e [код]": "Интерпретатор python"
}