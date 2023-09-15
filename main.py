from discord_bot import DiscordClient
import os
from dotenv import load_dotenv
from controller import Controller

load_dotenv()


def main():
    discord_client = DiscordClient(
        os.environ["DISCORD_TOKEN"],
    )

    controller = Controller(
        os.environ["OPENAI_API_KEY"],
        discord_client,
    )

    controller.run()


if __name__ == "__main__":
    main()
