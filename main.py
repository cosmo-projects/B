import os
import sys
import configparser
import time
from pyrogram import Client, filters
from pyrogram.types import Message

# Конфигурация
CONFIG_FILE = "config.ini"
COMMANDS_DIR = "cub_cmd"

# Поддержка Termux
if 'com.termux' in os.environ.get('PREFIX', ''):
    os.system('clear')
    print("🚀 Настройка Cosmo User Bot в Termux 🌌\n")

# Загрузка конфига
config = configparser.ConfigParser()
if not os.path.exists(CONFIG_FILE):
    print("🪐 Введите данные от Telegram API:\n")
    config['pyrogram'] = {
        'api_id': input("API ID: "),
        'api_hash': input("API Hash: ")
    }
    with open(CONFIG_FILE, 'w') as f:
        config.write(f)
    print("\n✅ Конфигурация сохранена! Запустите бота снова.")
    sys.exit()

config.read(CONFIG_FILE)
api_id = config.getint('pyrogram', 'api_id')
api_hash = config.get('pyrogram', 'api_hash')

# Загрузка команд
commands = {}
for filename in os.listdir(COMMANDS_DIR):
    if filename.endswith('.py') and not filename.startswith('__'):
        module_name = filename[:-3]
        try:
            module = __import__(f"{COMMANDS_DIR}.{module_name}", fromlist=['command'])
            if hasattr(module, 'command'):
                cmd = module.command
                commands[cmd['name']] = cmd
                for alias in cmd.get('aliases', []):
                    commands[alias] = cmd
        except:
            pass

# Клиент Pyrogram
app = Client(
    "cub_session",
    api_id=api_id,
    api_hash=api_hash,
    device_model="Cosmo User Bot",
    app_version="CUB 1.0",
    system_version="SpaceOS"
)

# Обработчик сообщений
@app.on_message(filters.text & (filters.private | filters.group))
async def handle_commands(client: Client, message: Message):
    start_time = time.time()
    prefixes = ['.', '! ', '/', '*']
    text = message.text
    
    # Поиск префикса
    prefix = None
    for p in prefixes:
        if text.startswith(p):
            prefix = p
            break
    
    if not prefix:
        return
    
    # Извлечение команды
    cmd_text = text[len(prefix):].strip()
    cmd_name = cmd_text.split()[0].lower() if cmd_text else ''
    
    # Поиск команды
    if cmd_name in commands:
        command = commands[cmd_name]
        try:
            await command['handler'](client, message, start_time)
        except:
            pass

# Запуск клиента
if __name__ == "__main__":
    print("""
    ____                  __  __       ____        _   
   / ___|___  _ __ ___   |  \/  | ___ | __ ) _   _| |_ 
  | |   / _ \| '_ ` _ \  | |\/| |/ _ \|  _ \| | | | __|
  | |__| (_) | | | | | | | |  | | (_) | |_) | |_| | |_ 
   \____\___/|_| |_| |_| |_|  |_|\___/|____/ \__,_|\__|
  :: Cosmo User Bot :: (CUB) ::          
""")
    print("🌌 Запуск космического бота...")
    app.start()
    print("\n🛑 Для остановки нажмите Ctrl+C\n")
    
    try:
        from threading import Event
        Event().wait()
    except KeyboardInterrupt:
        print("\n🌠 Остановка космического бота...")
        app.stop()
        print("✅ Бот успешно остановлен!")
