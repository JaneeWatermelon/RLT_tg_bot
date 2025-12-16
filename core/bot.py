import os
import dotenv
from aiogram import Bot, Dispatcher, types
from core.llm import text_to_sql
import core.database as database

class TGbot:
    def __init__(self, bot_token: str, db: database.Database, dispatcher: Dispatcher):
        self.bot = Bot(token=bot_token)
        self.db = db
        self.dispatcher = dispatcher

        self.dispatcher.message.register(self.handle)

    def run(self):
        print("Bot running successfully!")
        self.dispatcher.run_polling(self.bot)

    async def handle(self, message: types.Message):
        value = 0
        ASSETS_ROOT = os.getenv("ASSETS_ROOT")

        prompt = message.text

        sql = text_to_sql(prompt)
        with open(os.path.join(ASSETS_ROOT, "log_sql_prompts.txt"), "a", encoding="utf-8") as f:
            f.write(f"Запрос: {prompt}\n")
            f.write(f"SQL: \n{sql}\n")

            try:
                row = self.db.fetch_one(sql)

                if row is None:
                    raise ValueError("row is None")
                else:
                    value = list(row.values())[0]
            except Exception as e:
                print(f"Ошибка при выполнении SQL запроса: {e}")
                f.write(f"Ошибка при выполнении SQL запроса: {e}\n")
                value = 0

        await message.answer(str(value))

if __name__ == "__main__":
    dotenv.load_dotenv("dev.env")
    BOT_API_KEY = os.getenv("BOT_API_KEY")

    db = database.Database(
        host=os.getenv("DB_HOST"), 
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

    tg_bot = TGbot(bot_token=BOT_API_KEY, db=db, dispatcher=Dispatcher())

    tg_bot.run()

    
