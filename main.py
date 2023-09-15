from discord_bot import DiscordClient
import os
from dotenv import load_dotenv
from controller import Controller

load_dotenv()


def main():
    controller = Controller(
        os.environ["OPENAI_API_KEY"],
        os.environ["DISCORD_TOKEN"],
    )

    controller.run()


if __name__ == "__main__":
    main()
