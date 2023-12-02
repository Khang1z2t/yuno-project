from yuno_import import *

async def create_embed(ctx, description=None, color=None, author=None, thumbnail=None, footer=False):
    if color is None:
        color = bot_color(ctx)
    embed = discord.Embed(color=color)
    if author:
        embed.set_author(name=f'{ctx.author.name}', icon_url=ctx.author.avatar)
    if description:
        embed.description = f'**{description}**'
    if thumbnail:
        embed.set_thumbnail(url=thumbnail)
    if footer:
        embed.set_footer(text=f'Vào lúc: {datetime.now().strftime("%H:%M:%S")}')
    return embed


async def music_embed(ctx, title=None, url=None, thumbnail=None, description=None, color=None, footer=False):
    if color is None:
        color = bot_color(ctx)
    embed = discord.Embed(color=color)
    if title:
        embed.set_author(name=title[:40] + (' . . . ' if len(title) > 40 else ''), url=url)
    if description:
        embed.description = f'**{description}**'
    if thumbnail:
        embed.set_thumbnail(url=thumbnail)
    if footer:
        embed.set_footer(text=f'Vào lúc: {datetime.now().strftime("%H:%M:%S")}')
    return embed


def bot_color(ctx):
    bot_role = ctx.guild.me.top_role
    color = bot_role.color if bot_role else config.BOT_COLOR
    return color

def get_time(duration):
    minutes, seconds = divmod(duration // 1000, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours}:{str(minutes).zfill(2)}:{str(seconds).zfill(2)}" if hours else f"{minutes}:{str(seconds).zfill(2)}"
    

# def get_spotify_token():
#     url = 'https://accounts.spotify.com/api/token'
#     headers = {
#         'Authorization': 'Basic ' + base64.b64encode((config.SPOTIFY_ID + ':' + config.SPOTIFY_SECRET).encode()).decode(),
#     }
#     data = {
#         'grant_type': 'client_credentials'
#     }
#     r = requests.post(url, headers=headers, data=data)
#     return r.json()['access_token']

class Music_checks:
    async def check_join(ctx):
        embed = await create_embed(ctx, f'Bạn phải tham gia voice channel để dùng lệnh này', Color.red())
        return embed
    
    async def check_connected(ctx):
        embed = await create_embed(ctx, f'{ctx.me.user.name} không kết nối đến voice channel nào.', Color.red())
        return embed
    
