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
    

class Support:
    async def momo(ctx):
        embed = discord.Embed(color=config.BOT_COLOR)
        embed.title = '***Ủng hộ Yuno***'
        embed.description = (f'*Cảm ơn bạn đã sử dụng Yuuki Yuno.*'
                             '\n\n Momo: ``0865399254``'
                             '\n Hoặc bạn có thể ấn vào đây: [Momo](https://me.momo.vn/yunok)')
        embed.set_image(url='https://cdn.discordapp.com/attachments/1181228128174092328/1181233378834518026/IMG_7886.png?ex=6580504f&is=656ddb4f&hm=80b6112c3fb9932d636f64b3d94c50aeb08b40a82c5103b24f2730e9b582a5cb&')
        embed.set_footer(text=f'Bởi: {ctx.user.name}, Vào lúc: {datetime.now().strftime("%H:%M:%S")}')
        return embed
    
    async def bank(ctx):
        embed = discord.Embed(color=config.BOT_COLOR)
        embed.title = '***Ủng hộ Yuno***'
        embed.description = (f'*Cảm ơn bạn đã sử dụng Yuuki Yuno.*'
                             '\n\n Ngân hàng: ``Timo by Ban Viet Bank``'
                             '\n Chủ tài khoản: ``Đinh Quốc Bảo Khang``'
                             '\n Số tài khoản: ``0865399254``')
        embed.set_image(url='https://cdn.discordapp.com/attachments/1181228128174092328/1181233365681184768/IMG_7887.jpg?ex=6580504c&is=656ddb4c&hm=31a4b70f24f56d1c1d53627815e81ee1e08c84e3fc7a9a9011910c420542e9ca&')
        embed.set_footer(text=f'Bởi: {ctx.user.name}, Vào lúc: {datetime.now().strftime("%H:%M:%S")}')
        return embed
    
    async def paypal(ctx):
        embed = discord.Embed(color=config.BOT_COLOR)
        embed.title = '***Ủng hộ Yuno***'
        embed.description = (f'*Cảm ơn bạn đã sử dụng Yuuki Yuno.*'
                             '\n\n Bạn có quét mã QR ở dưới hoặc.' 
                             '\n ấn vào đây: [Paypal](https://paypal.me/yunokb)')
        embed.set_image(url='https://cdn.discordapp.com/attachments/1181228128174092328/1181250717059649586/paypalQR.png?ex=65806075&is=656deb75&hm=dbea5c627018ef03034fee96daaf7c91906a389d419e59f387bba2bd1153a125&')
        embed.set_footer(text=f'Bởi: {ctx.user.name}, Vào lúc: {datetime.now().strftime("%H:%M:%S")}')
        return embed