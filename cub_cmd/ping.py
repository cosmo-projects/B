import time

async def ping_handler(client, message, start_time):
    # Рассчет времени ответа
    end_time = time.time()
    response_time = round((end_time - start_time) * 1000, 2)
    
    # Форматированный ответ
    response = (
        "🏓 Pong!\n"
        "✅ CUB успешно функционирует.\n"
        f"⏱️ Ответил за: ±{response_time} мс"
    )
    
    await message.reply(response)

command = {
    'name': 'ping',
    'aliases': ['пинг', 'test', 'status'],
    'handler': ping_handler
}
