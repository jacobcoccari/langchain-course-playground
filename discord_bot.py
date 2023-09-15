# the Discord Python API
import discord


class DiscordClient(discord.Client):
    def __init__(self, discord_api_key):
        # adding intents module to prevent intents error in __init__ method in newer versions of Discord.py
        intents = (
            discord.Intents.default()
        )  # Select all the intents in your bot settings as it's easier
        intents.message_content = True
        super().__init__(intents=intents)
        self.discord_api_key = discord_api_key

    def my_run(self):
        if self.query == None:
            raise Exception("Query function is not set")
        self.run(self.discord_api_key)

    def set_query_function(self, query_fn):
        self.query = query_fn

    # Async function on_ready. Based on DISCORD API DOCUMENTATION
    # This function will be called when the bot is logging in.
    async def on_ready(self):
        # print out information when the bot wakes up
        print("Logged in as")
        print(self.user.name)
        print(self.user.id)
        print("------")
        # send a request to the model without caring about the response
        # just so that the model wakes up and starts loading
        # self.query({'inputs': {'text': 'Hello!'}})

    # Based on DISCORD API DOCUMENTATION
    #
    async def on_message(self, message):
        """
        this function is called whenever the bot sees a message in a channel
        """
        # ignore the message if it comes from the bot itself
        if message.author.id == self.user.id:
            return

        # form query payload with the content of the message
        payload = {"inputs": {"text": message.content}}

        # while the bot is waiting on a response from the model
        # set the its status as typing for user-friendliness
        async with message.channel.typing():
            response = self.query(payload["inputs"]["text"])
        bot_response = response

        # we may get ill-formed response if the model hasn't fully loaded
        # or has timed out
        if not bot_response:
            if "error" in response:
                bot_response = "`Error: {}`".format(response["error"])
            else:
                bot_response = "Hmm... something is not right."

        # send the model's response to the Discord channel
        await message.channel.send(bot_response)
