from utils.bot import JBot
from dotenv import load_dotenv


if __name__ == "__main__":
    load_dotenv(".env")
    bot = JBot()
    bot.run()
