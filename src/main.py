import asyncio
from pytz import timezone
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, InputFile, FSInputFile
from scheduler import scheduler


from config import TOKEN
PHOTOS_DIR = os.path.join(os.path.dirname(__file__), '../photos')
SENT_PHOTOS_DIR = os.path.join(os.path.dirname(__file__), '../sended')

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: Message):
  await message.answer(f'Работаю {message.chat.id}')


async def post_photo():
  try:
    photos = sorted([f for f in os.listdir(PHOTOS_DIR) if f.endswith(('.jpg', '.jpeg', '.png'))])
    if not photos:
            logging.info("Нет доступных фотографий для отправки.")
            return
    photo = photos[0]
    photo_path = os.path.join(PHOTOS_DIR, photo)

    await bot.send_photo(chat_id='-1002452185996',photo=FSInputFile(photo_path))
    logging.info(f"Отправлено фото: {photo}")

    os.makedirs(SENT_PHOTOS_DIR, exist_ok=True)  # Создаём папку, если её нет
    sent_photo_path = os.path.join(SENT_PHOTOS_DIR, photo)
    os.rename(photo_path, sent_photo_path)
    logging.info(f"Фото перемещено в папку отправленных: {sent_photo_path}")


  except Exception as e:
    logging.error(f"Ошибка при отправке фото: {e}")

async def on_startup():
  scheduler.add_job(post_photo, 'cron', hour='19', minute='19', timezone=timezone('Asia/Bishkek'))
  scheduler.add_job(post_photo, 'cron', hour='19', minute='20', timezone=timezone('Asia/Bishkek'))
  scheduler.add_job(post_photo, 'cron', hour='19', minute='21', timezone=timezone('Asia/Bishkek'))
  scheduler.start()
  logging.info('Авторассылка запущена')

async def main(): 
  await on_startup()
  try:
    await dp.start_polling(bot)
  finally:
    await bot.session.close()

if __name__ == '__main__':
  asyncio.run(main())