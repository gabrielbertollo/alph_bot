import twitchio
from twitchio.ext import commands
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

class Bot(commands.Bot):
    def __init__(self):
        # Use environment variables for the token and channel
        token = os.getenv('TWITCH_TOKEN')
        initial_channels = [os.getenv('TWITCH_CHANNEL')]
        super().__init__(token=token, prefix='!', initial_channels=initial_channels)

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    @commands.command(name='save')
    async def save(self, ctx):
        # Assuming the command is "!save <text>"
        text_to_save = ctx.message.content[len("!save "):].strip()
        
        # Write the text to an HTML file
        with open("output.html", "w") as file:
            file.write(f"<html><body><p>{text_to_save}</p></body></html>")
        
        await ctx.send(f'Text saved to HTML file: {text_to_save}')

# Main entry point
if __name__ == "__main__":
    bot = Bot()
    bot.run()
