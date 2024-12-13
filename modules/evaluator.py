from utils.imports import *
from utils.func import *
from utils.misc import *

@Client.on_message(filters.command(["eval", 'e'], prefixes=prefix) & filters.me)
async def ev(client, message):
    	code = " ".join(message.text.split()[1:])
    	try:
    	   result = eval(code)
    	   try:
    	   	return await message.edit_text(f'''<emoji id=5339181821135431228>💻</emoji> <b>Код:</b>
```python
{code}```

<emoji id=5175061663237276437>🐍</emoji> <b>Вывод:</b>
```python
{result}```''')
    	   except:
    	   	with open('eval_output.txt', 'w') as f:
    	   		f.write(f'''💻 Код:
{code}

🐍 Вывод:
{result}''')
    	   	await message.delete()
    	   	await client.send_document(message.chat.id, document='eval_output.txt', caption='<emoji id=5175061663237276437>🐍</emoji> <b>Вывод команды слижком большой и был преобразован в файл...</b>')
    	   	os.remove('eval_output.txt')
    	   	return
    	except Exception as ex:
    		return await message.edit_text(format_exc(ex))

modules_help['evaluator'] = {
	"eval [код]": "Интерпретатор python",
	"e [код]": "Интерпретатор python"
}