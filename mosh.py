from threading import Timer
import asyncio
import random
import twitchio
from twitchio.ext import commands
from datetime import datetime

mosh_list = []
mosh_end_timer = None
mosh_message_timer = None
mosh_started = False
mosh_type = "default" 

message_pools = {
    "default": [
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
        "{} found a wallet in the mosh! What a lucky bastard!",
        "{} found a phone in the mosh! WHO LOST THEIR PHONE?!",
        "{} is starting a wall of death! {} is on the other side!",
        "{} found a shoe in the mosh! WHO LOST THEIR SHOE?!",
        "{} is doing the running man dance! Who will join them?",
        "{} accidentally headbutts {} during a jump!",
        "{} dives off the stage and lands on {}!",
        "{} and {} start a push-up contest in the middle of the pit!",
        "{} is riding a wave of people! {} tries to pull them down!",
        "{} is spinning around with arms wide open! {} ducks just in time!",
        "{} and {} are locked in a friendly wrestling match!",
        "{} and {} are having a dance-off in the mosh!",
        "{} and {} are having a thumb war in the mosh!",
        "{} and {} are having a staring contest in the mosh!",
        "{} pours water over {}'s head in the middle of the pit!",
        "{} brought a giant inflatable unicorn into the pit!",
        "{} and {} are playing leapfrog in the mosh!",
        "{} attempts a stage dive but no one catches them! CALL AN AMBULANCE!",
        "{} throws their shirt into the crowd! {} catches it!",
        "{} throws their beer into the air! MAKE IT RAIN!",
        "{} throws a chair at {}! WHAT THE HELL?!",
        "{} throws a burquinha at {}! WHAT EVEN IS THAT?!",
        "{} is trying to sing along... But they don't know the lyrics!",
        "{} is disrespecting their surroundings!",
    ],
    "sad": [
        "Someone stop {}, they're trying to call their ex" 
        "Look at {}, making it rain on the dancefloor, too bad it's tears and not money"
        "{} has been staring at the wall for a while, someone please check on them" 
        "{} needs a shoulder to cry on" 
        "{} voice is cracking but they're still singing, what a champ!" 
        "{} has just slipped on {}'s puddle of tears, careful where you cry folks!" 
        "Alexa, this is too sad, play 'Despacito'." 
        "{} is offering free hugs and cookies for anyone in need during this depressing times." 
        "{} is getting horny, this is the wrong mosh fella, please behave yourself!"
        "Daily reminder to not cry on the Amps, last time {} did it we had to wait for 2 hours for an extra Amp!"
        "{} is telling everyone that this song is as sad as the episode where Chaves gets called a thief, whatever that means."
        "{} and {} are offering complimentary tissues for our saddest homies, what a beautiful moment!" 
        "We've seen the top 10 saddest moments in all of Alph's stream and somehow {} is in all of them. Do you need some help mate?"
        "Such a lonely day... And it's {}'s."
        "{} is crying in the mosh pit.",
        "{} just got their heart broken.",
        "{} is sitting alone in the corner. Someone should check on them.",
        "{} is drowning their sorrows in a drink. {} joins them.",
        "{} is asking for an encore with their ex. I don't think that's wise.",
        "{} cried so much they don't even have a voice to sing anymore, sadge moment. PepeHands",
        "{} is trying to cheer up {} after they dropped their beer.",
        "{} sighs and gently shoves {}. This is a melancholic mosh.",
        "{} is moshing... but with sadness in their eyes.",
        "{} hugs {} in the middle of the mosh. It's okay to cry.",
        "{} brings their broken heart to the pit. {} offers a tissue.",
        "{} breaks down mid-mosh. {} starts slow clapping in support.",
        "{} screams lyrics that no one hears. {} feels every word.",
        "{} falls to their knees. {} helps them up, but the sadness lingers.",
    ],
    "horny": [
        "{} gives {} a wink in the mosh!",
        "{} pulls out a whip. Don't ask questions.",
        "{} rips their shirt dramatically!",
        "{} is moshing with handcuffs on!",
        "{} drops their pants. {} drops their standards.",
        "{} is calling they're ex! SOMEONE STOP THEM!",
        "{} bites their lip while staring at {}!",
        "{} and {} are slow dancing in the middle of the pit. Get a room!",
        "{} sprays whipped cream on {}! What is happening?!",
        "{} is twerking on the amp! Someone stop them!",
        "{} blows a kiss at {} mid-jump!",
        "{} is moshing in nothing but a leather harness!",
        "{} slaps {} on the butt and runs away giggling!",
        "{} is reading 50 Shades of Grey in the middle of the pit!",
        "{} brought massage oil to the mosh. Why?!",
        "{} is doing a striptease on the stage! Security! SECURITY!",
        "{} whispers something in {}'s ear and they BLUSH!",
        "{} pole dances on the mic stand!",
        "{} and {} disappeared behind the speakers... catSUS!",
        "{} is sensually eating a banana while staring at {}!",
        "{} crawls across the floor toward {}! THIS IS A MOSH PIT, NOT A BEDROOM!",
        "{} pulls out a feather and tickles {}!",
        "{} is moshing in lingerie! Bold choice!",
        "{} smacks {} with a paddle! KINKY!",
        "{} is fanning themselves dramatically. Is it the heat or {}?!",
    ],
    "cowboy": [
        "{} is starting a line dance. Who's gonna join them?",
        "{}'s belt buckle deflects a stray bullet!",
        "{}'s horse joined the mosh too.",
        "There's a snake in {}'s boot!",
        "{} is using their lasso to steal {}'s whiskey bottle.",
        "Someone stole {}'s hat. Call the Sheriff!",
        "{} started a bar fight!",
        "{} is auctioning off their favorite cow. Who'll bid higher?",
        "A tumbleweed hits {}'s face.",
        "{} and {} are heading for a standoff! Who will be faster?",
        "{} challenges {} to a spittin' contest! Aim for the spittoon!",
        "{} is riding a mechanical bull in the middle of the pit!",
        "{} pulls out a harmonica and starts playing a sad tune. Yeehaw blues!",
        "{} and {} are arm wrestling for the last piece of jerky!",
        "{} accidentally shot themselves in the foot! Greenhorn move!",
        "{} rolled into town on a tumbleweed!",
        "{} is twirling a six-shooter like a pro!",
        "{} just spit tobacco juice straight onto {}'s boot!",
        "{} is wrangling cattle through the mosh pit! MOOOOOVE!",
        "The Sheriff just rode in! Everyone act natural!",
        "{} just challenged {} to a high-noon duel! Reach for it!",
        "{} is doing the boot scootin' boogie!",
        "{} just hogtied {} with their lasso!",
        "A bandit just robbed the saloon! Everyone after {}!",
        "{} is chewing on a piece of hay and lookin' real cool!",
        "{} just rolled a cigarette one-handed. Smooth, partner!",
        "{} got bucked off the bull and landed on {}!",
        "{} just kicked open the saloon doors! This town ain't big enough!",
        "{} is challenging {} to a quick draw! Watch them dance!",
        "{}'s spurs are jinglin' too loud! Quiet down, partner!",
        "{} just lit a stick of dynamite! EVERYBODY RUN!",
        "{} is teaching {} how to two-step!",
    ]
}

async def start_mosh(ctx, type_name="default"):
    global mosh_end_timer, mosh_list, mosh_started, mosh_message_timer, mosh_type

    user = ctx.author.name

    if user not in mosh_list:
        mosh_list.append(user)
        
        mosh_emotes = {
            "default": "Mosh Mosh Mosh Mosh Mosh Mosh Mosh Mosh Mosh Mosh Mosh",
            "sad": "PepePls PepePls PepePls PepePls PepePls PepePls PepePls PepePls PepePls PepePls",
            "horny": "Kreygasm Kreygasm Kreygasm Kreygasm Kreygasm Kreygasm Kreygasm Kreygasm Kreygasm Kreygasm",
            "cowboy": "aurHowdy aurHowdy aurHowdy aurHowdy aurHowdy aurHowdy aurHowdy aurHowdy aurHowdy aurHowdy"
        }
        
        if not mosh_started:
            mosh_started = True
            mosh_type = type_name
            mosh_message_timer = asyncio.create_task(mosh_countdown(ctx))
            
            start_text = {
                "default": f"{user} is starting a mosh pit! Who's gonna join them? {mosh_emotes[type_name]}",
                "sad": f"{user} is sad and starting a mosh pit. Who's gonna join them? (bring tissues) {mosh_emotes[type_name]}",
                "horny": f"Looks like {user} is horny and is starting a mosh pit! Who's gonna join them? {mosh_emotes[type_name]}",
                "cowboy": f"Yeehaw! {user} is starting a cowboy mosh pit! Saddle up partners! {mosh_emotes[type_name]}"
            }
            await ctx.send(start_text[mosh_type])
            
        else:
            await ctx.send(f"{user} joined the mosh with {len(mosh_list)} moshers! {mosh_emotes[mosh_type]}")

        if mosh_end_timer:
            mosh_end_timer.cancel()

        mosh_end_timer = asyncio.create_task(mosh_end(ctx))

async def mosh_end(ctx):
    global mosh_list, mosh_end_timer, mosh_started, mosh_message_timer, mosh_type

    await asyncio.sleep(90)

    has_winner = True

    if len(mosh_list) > 1:
        if has_winner:
            winner = random.choice(mosh_list)
            end_text = {
                "default": "The mosh pit ended with {} participants! That was a wild one! {} survived the mosh and won a VIP token! What a beast!",
                "sad": "The sad times are over! The mosh pit has ended with {} participants! {} cried the hardest and won a VIP token! Here's a tissue and a prize!",
                "horny": "The horny mosh pit has ended with {} participants! {} was the horniest mosher and won a VIP token! Behave yourself!",
                "cowboy": "The rodeo is over! The cowboy mosh pit ended with {} participants! {} is the last cowboy standing and won a VIP token! Yeehaw!"
            }
            await ctx.send(end_text[mosh_type].format(len(mosh_list), winner))
            await ctx.send(f"!givevip @{winner} 0.1")
        else:
            end_text = {
                "default": "The mosh pit ended with {} participants! That was a wild one!",
                "sad": "The sad times are over! The mosh pit has ended with {} participants! Let's hope it was a healing experience!",
                "horny": "The horny mosh pit has ended with {} participants! That was steamy!",
                "cowboy": "The rodeo is over! The cowboy mosh pit ended with {} participants! What a wild ride!"
            }
            await ctx.send(end_text[mosh_type].format(len(mosh_list)))
    else:
        user = mosh_list[0]
        end_text = {
            "default": "{} was the only one in the mosh! What a loner!",
            "sad": "{} was the only one sad enough to start a mosh pit. Let's hope they find some comfort soon!",
            "horny": "{} was the only one horny here. Go to horny jail!",
            "cowboy": "{} was the only cowboy in town. Lonely rider!"
        }
        await ctx.send(end_text[mosh_type].format(user))

    mosh_list = []
    mosh_started = False
    mosh_type = "default"
    
    if mosh_end_timer:
        mosh_end_timer.cancel()
    if mosh_message_timer:
        mosh_message_timer.cancel()


async def mosh_countdown(ctx):
    global mosh_list, mosh_started, mosh_type, message_pools

    while True:
        await asyncio.sleep(15)

        if mosh_started and len(mosh_list) > 1:
            user1, user2 = random.sample(mosh_list, 2)
            message = random.choice(message_pools[mosh_type]).format(user1, user2)
            await ctx.send(message)
