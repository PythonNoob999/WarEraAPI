'''
a simple discord bot to get user data
'''

from WarEraAPI import WarEraClient
from os import environ

import discord
import discord.ext.commands


intents = discord.Intents.default()
intents.message_content = True

bot = discord.ext.commands.Bot(command_prefix="!", intents=intents)
client = WarEraClient()

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


async def get_user(
    ctx: discord.ext.commands.Context
) -> None:
    
    msg = ctx.message

    if not msg.mentions:
        username = msg.content.split()[1] if len(msg.content.split()) > 1 else None
        if not username:
            await ctx.reply(
                content="Please mention a user or provide a username to fetch their profile info"
            )
            return
    else:
        username = msg.mentions[0].global_name
    

    try:
        search = await client.search(username)

        if not search.userIds:
            return await ctx.reply(
                content=f"{username} Not Found"
            )

        user_id = search.userIds[0]
        user = await client.get_user(user_id)
        country = await client.get_country(user.country)
        embed = discord.Embed(
            title="User Profile",
            color=0x3498db
        )

        embed.add_field(
            name="Username",
            value=user.username,
            inline=True
        )
        embed.add_field(
            name="Country",
            value=country.name,
            inline=True
        )
        embed.add_field(
            name="Level",
            value=str(user.leveling["level"]),
            inline=True
        )
        embed.add_field(
            name="Joined",
            value=user.createdAt.strftime("%B %d, %Y"),
            inline=True
        )

        if user.rankings:
            embed.add_field(
                name="TotalDamages",
                value=user.rankings["userDamages"]["value"],
                inline=True
            )
            embed.add_field(
                name="TotalWealth",
                value=f'{user.rankings["userWealth"]["value"]:.0f}Coints',
                inline=True
            )

        embed.set_footer(text="WarEra User Profile")
        if user.animatedAvatarUrl or user.avatarUrl:
            embed.set_image(url=user.animatedAvatarUrl or user.avatarUrl)
        
        await ctx.reply(
            embed=embed
        )

    except Exception as e:
        print(e)
        await ctx.reply(
            content="an unexpected error occurred while fetching the user profile ⚠️"
        )


bot.add_command(
    discord.ext.commands.Command(
        get_user,
        name="get_user",
        help="get info about a user"
    )
)


bot.run(
    token=environ["BOT_TOKEN"]
)