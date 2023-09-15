from discord_bot import DiscordClient
import os
from dotenv import load_dotenv

load_dotenv()


def main():
    # option 1: DO THIS

    controller = Controller(
        {
            "OPENAPI_KEY": os.environ["OPENAPI_KEY"],
        }
    )

    # controller.query("")

    client = DiscordClient(
        {
            "dicord_token": os.environ["DISCORD_TOKEN"],
        },
        controller,
    )

    client.run()

    # option 2:

    client = DiscordClient(
        {
            "openapi_key": os.environ["OPENAPI_KEY"],
            "dicord_token": os.environ["DISCORD_TOKEN"],
        }
    )

    # option 3:


if __name__ == "__main__":
    main()
