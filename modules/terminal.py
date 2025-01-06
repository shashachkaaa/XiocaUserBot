from utils.imports import *
from utils.func import *
from utils.misc import *

@Client.on_message(filters.command(['t', 'terminal'], prefixes=prefix) & filters.user(allowed))
async def terminal(client, message):
    code = " ".join(message.text.split()[1:])
    try:
    	process = subprocess.Popen(code.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    	output, error = process.communicate()
    except Exception as e:
    	return await answer(message, f'''<emoji id=5339181821135431228>💻</emoji> <b>Команда:</b>
```bash
{code}```

<emoji id=5237993272109967450>❌</emoji> <b>Ошибка:</b>
```bash
{error.decode()}```''')
    
    await answer(message, f'''<emoji id=5339181821135431228>💻</emoji> <b>Команда:</b>
```bash
{code}```

<emoji id=5375360100196163660>🐲</emoji> <b>Вывод:</b>
```bash
{output.decode()}```
''')

modules_help['terminal'] = {
	"terminal [команда]": "Выполнить команду в терминале",
	"t [команда]": "Выполнить команду в терминале"
}