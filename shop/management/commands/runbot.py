import os
import asyncio
from django.core.management.base import BaseCommand
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from shop.bot.handlers import router as main_router
from aiogram.client.default import DefaultBotProperties 

class Command(BaseCommand):
    help = 'Runs the Telegram bot using aiogram'

    def handle(self, *args, **options):
        bot_token = os.getenv('BOT_TOKEN')
        if not bot_token:
            self.stdout.write(self.style.ERROR('Bot token not found in .env file.'))
            return

        asyncio.run(self.start_bot(bot_token))

    async def start_bot(self, token: str):
        default_properties = DefaultBotProperties(parse_mode='HTML')
        bot = Bot(token=token, default=default_properties)

        storage = MemoryStorage()
        dp = Dispatcher(storage=storage)

        dp.include_router(main_router)

        self.stdout.write(self.style.SUCCESS('Bot is running with aiogram...'))
        
        await bot.delete_webhook(drop_pending_updates=True)
        
        await dp.start_polling(bot)
