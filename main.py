import twitchio
from twitchio.ext import commands
import os
from dotenv import load_dotenv
from mosh import mosh

# Load environment variables from the .env file
load_dotenv()

class Bot(commands.Bot):
    first_user = None
    
    def __init__(self):
        # Use environment variables for the token and channel
        token = os.getenv('TWITCH_TOKEN')
        initial_channels = [os.getenv('TWITCH_CHANNEL')]
        super().__init__(token=token, prefix='!', initial_channels=initial_channels)

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')
        await self.erase_file_content()
    
    async def event_message(self, message):
        await self.handle_commands(message)
        if ", requested by " in message.content.lower() and message.author.name.lower() == "kokolibot":
            await self.save_requester_name(message.content)
        # React to messages that contain "catSUS"
        if "catSUS" in message.content:
            await message.channel.send('catSUS')
            
    async def save_requester_name(self, text):
        start_index = text.lower().index(", requested by ") + len(", requested by ")
        end_index = text.find(" ", start_index)
        if end_index == -1:
            requester_name = text[start_index:].strip()  
        else:
            requester_name = text[start_index:end_index].strip()
        await self.write_to_file(requester_name)
            
    async def write_to_file(self, text):
        with open("output.html", "w") as file:
            file.write(f"""<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><link rel="stylesheet" type="text/css" href="style.css"><link href="https://fonts.googleapis.com/css?family=Open+Sans" rel="stylesheet"><meta http-equiv="refresh" content="5"></head><body><a class="requesterName">Requester: {text}</a></body></html>""")
            
    async def erase_file_content(self):
        with open("output.html", "w") as file:
            file.write(f"""<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><link rel="stylesheet" type="text/css" href="style.css"><link href="https://fonts.googleapis.com/css?family=Open+Sans" rel="stylesheet"><meta http-equiv="refresh" content="5"></head><body><a class="requesterName"></a></body></html>""")
            
    @commands.command(name='requester', aliases=['r'])
    async def requester(self, ctx):
        if ctx.author.is_mod:
            if len(ctx.message.content.split(" ")) < 2:
                await ctx.send("Please provide the requester name. Example: !requester JohnDoe")
            else:
                requester_name = ctx.message.content.split(" ")[1]
                await self.write_to_file(requester_name)
                await ctx.send(f"Requester has been updated to {requester_name}")
                
    @commands.command(name='rclear', aliases=['rc'])
    async def rclear(self, ctx):
        if ctx.author.is_mod:
            await self.erase_file_content()
            await ctx.send("Requester has been cleared")

    @commands.command(name='mosh')
    async def mosh(self, ctx):
        await mosh(ctx)
        
    @commands.command(name='first')
    async def first(self, ctx):
        if self.first_user is None:
            self.first_user = ctx.author.name
            await ctx.send(f"!givevip @{self.first_user}")
        else:
            await ctx.send(f"First has already been taken by {self.first_user}!")

# Main entry point
if __name__ == "__main__":
    bot = Bot()
    bot.run()
