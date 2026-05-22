import asyncio
import twitchio
from twitchio.ext import commands
import os
from dotenv import load_dotenv
from mosh import start_mosh
from PIL import Image, ImageDraw, ImageFont

# Load environment variables from the .env file
load_dotenv()

class Bot(commands.Bot):
    first_user = None
    second_user = None
    
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
        await start_mosh(ctx, "default")
        
    @commands.command(name='sadmosh')
    async def sadmosh(self, ctx):
        await start_mosh(ctx, "sad")
        
    @commands.command(name='hornymosh')
    async def hornymosh(self, ctx):
        await start_mosh(ctx, "horny")

    @commands.command(name='cowboymosh')
    async def cowboymosh(self, ctx):
        await start_mosh(ctx, "cowboy")
        
    @commands.command(name='first', aliases=['First'])
    async def first(self, ctx):
        if self.first_user is None:
            self.first_user = ctx.author.name
            await ctx.send(f"{self.first_user} you are FIRST! You will receive a VIP token soon!")
            await asyncio.sleep(120) 
            await ctx.send(f"!givevip @{self.first_user}")
        else:
            await ctx.send(f"First has already been taken by {self.first_user}!")

    @commands.command(name='second', aliases=['Second'])
    async def second(self, ctx):
        if self.first_user is not None and self.second_user is None:
            if ctx.author.name == self.first_user:
                await ctx.send("You cannot take Second after taking First!")
                return
            self.second_user = ctx.author.name
            await ctx.send(f"{self.second_user} you are SECOND! You will receive a VIP token soon!")
            await asyncio.sleep(120)
            await ctx.send(f"!givevip @{self.second_user} 0.1")
        else:
            if self.first_user is None:
                await ctx.send(f"Calm down {ctx.author.name}! First must be taken before Second!")
            else:
                await ctx.send(f"Second has already been taken by {self.second_user}!")
    
    def generate_requests_image(self, is_on):
        width, height = 300, 180
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Title "REQUESTS" in Arial Black
        title_font = ImageFont.truetype('ariblk.ttf', 36)
        title_bbox = draw.textbbox((0, 0), "REQUESTS", font=title_font)
        title_x = (width - (title_bbox[2] - title_bbox[0])) // 2
        draw.text((title_x, 10), "REQUESTS", fill="white", font=title_font)

        # Switch pill shape
        pill_w, pill_h = 160, 60
        pill_x = (width - pill_w) // 2
        pill_y = 80
        radius = pill_h // 2

        if is_on:
            pill_color = (34, 197, 94)  # green
            label = "ON"
            # Circle on the right side
            circle_x = pill_x + pill_w - pill_h
        else:
            pill_color = (220, 38, 38)  # red
            label = "OFF"
            # Circle on the left side
            circle_x = pill_x

        # Draw pill background
        draw.rounded_rectangle(
            [pill_x, pill_y, pill_x + pill_w, pill_y + pill_h],
            radius=radius, fill=pill_color
        )

        # Draw white circle (knob)
        margin = 4
        draw.ellipse(
            [circle_x + margin, pill_y + margin,
             circle_x + pill_h - margin, pill_y + pill_h - margin],
            fill="white"
        )

        # Draw ON/OFF label on the pill
        label_font = ImageFont.truetype('ariblk.ttf', 24)
        label_bbox = draw.textbbox((0, 0), label, font=label_font)
        label_w = label_bbox[2] - label_bbox[0]
        label_h = label_bbox[3] - label_bbox[1]
        if is_on:
            label_x = pill_x + (pill_w - pill_h) // 2 - label_w // 2 + 10
        else:
            label_x = pill_x + pill_h + (pill_w - pill_h) // 2 - label_w // 2 - 10
        label_y = pill_y + (pill_h - label_h) // 2 - label_bbox[1]
        draw.text((label_x, label_y), label, fill="white", font=label_font)

        img.save("requests.png")

    @commands.command(name='requests')
    async def requests(self, ctx):
        if 'on' in ctx.message.content.lower() and ctx.author.is_mod:
            self.generate_requests_image(True)
        elif 'off' in ctx.message.content.lower():
            self.generate_requests_image(False)

    @commands.command(name='birthday')
    async def birthday(self, ctx):
        if ctx.author.is_mod:
            parts = ctx.message.content.split(" ")
            if len(parts) < 2:
                await ctx.send("Please provide a user. Example: !birthday @user")
                return
            target = parts[1].lstrip("@")
            await ctx.send(f"Happy Birthday @{target}, as a gift you get a VIP token!")
            await ctx.send(f"!givevip @{target}")

    @commands.command(name='aniversario')
    async def aniversario(self, ctx):
        if ctx.author.is_mod:
            parts = ctx.message.content.split(" ")
            if len(parts) < 2:
                await ctx.send("Por favor forneça um usuário. Exemplo: !aniversario @user")
                return
            target = parts[1].lstrip("@")
            await ctx.send(f"Feliz Aniversário @{target}, como presente você ganha um token VIP!")
            await ctx.send(f"!givevip @{target}")

    @commands.command(name='on')
    async def on(self, ctx):
        if ctx.author.is_mod:
            self.generate_requests_image(True)
            await ctx.send("!requests on")
            await ctx.send("!vips on")

    @commands.command(name='off')
    async def off(self, ctx):
        if ctx.author.is_mod:
            self.generate_requests_image(False)
            await ctx.send("!requests off")
            await ctx.send("!vips off")

# Main entry point
if __name__ == "__main__":
    bot = Bot()
    bot.run()
