from threading import Timer
import asyncio
import random
import twitchio
from twitchio.ext import commands
from datetime import datetime

mosh_list = []
mosh_end_timer = None
mosh_message_timer = None
message_pool = [
    "{} hits {} in the eye! This mosh is crazy!",
    "{} is crowd surfing the mosh!",
    "{} is on the ground! Hold the pit!",
    "{} is throwing elbows in the mosh!",
    "{} is starting a wall of death!",
    "{} is starting a circle pit!",
    "{} is starting a stage dive!",
    "{} is starting a human pyramid!",
    "{} is starting a headbanging circle!",
    "{} hits {} in the face with a beer!",
    "{} throws a shoe at {}!",
    "{} throws a bra at {}!",
    "{} knocks {} out with a punch!",
    "Hold the pit! {} is playing with their Bayblade!",
    "Hold the pit! {} and {} are playing Magic the Gathering!",
    "{} is starting a rowing pit! ROW ROW ROW!",
]
mosh_started = False

async def mosh(ctx):
    global mosh_end_timer, mosh_list, mosh_started, mosh_message_timer

    user = ctx.author.name

    if user not in mosh_list:
        mosh_list.append(user)
        if not mosh_started:
            mosh_started = True
            mosh_message_timer = asyncio.create_task(mosh_countdown(ctx))
            await ctx.send(f"{user} is starting the mosh! Who's gonna join them? Mosh Mosh Mosh Mosh Mosh Mosh Mosh Mosh Mosh Mosh Mosh Mosh Mosh Mosh Mosh Mosh Mosh Mosh Mosh Mosh Mosh Mosh")
        else:
            await ctx.send(f"{user} joined the mosh with {len(mosh_list)} moshers! Mosh Mosh Mosh Mosh Mosh Mosh Mosh Mosh Mosh Mosh Mosh Mosh Mosh Mosh Mosh Mosh Mosh Mosh Mosh Mosh Mosh Mosh")

        if mosh_end_timer:
            mosh_end_timer.cancel()

        mosh_end_timer = asyncio.create_task(mosh_end(ctx))

async def mosh_end(ctx):
    global mosh_list, mosh_end_timer, mosh_started, mosh_message_timer

    await asyncio.sleep(60)

    if len(mosh_list) > 1:
        await ctx.send(f"The mosh ended with {len(mosh_list)} participants!")
    else:
        user = mosh_list[0]
        await ctx.send(f"{user} was the only one in the mosh! What a loner!")

    mosh_list = []
    mosh_started = False
    if mosh_end_timer:
        mosh_end_timer.cancel()
    if mosh_message_timer:
        mosh_message_timer.cancel()


async def mosh_countdown(ctx):
    global mosh_list, mosh_end_timer, mos_started

    while True:
        await asyncio.sleep(15)

        if mosh_started and len(mosh_list) > 1:
            user1, user2 = random.sample(mosh_list, 2)
            message = random.choice(message_pool).format(user1, user2)
            await ctx.send(message)
