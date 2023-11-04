import disnake
from disnake.ext import commands
from disnake import *
from disnake.ext.commands import *
from datetime import datetime, timedelta
from typing import Union
import requests
import json
import os
from apiKey import *

class Command(commands.Cog):
    
    def __init__(self, client):
        self.client = client
    
    # embed
    def bot_color(self, ctx):
        bot_role = ctx.guild.me.top_role
        color = bot_role.color
        return color
      
    # lấy avt người dùng  
    @commands.command()
    async def avt(self, ctx, user: disnake.User = None):
        if user is None:
            if ctx.message.reference:
                ori_msg = await ctx.fetch_message(ctx.message.reference.message_id)
                user = ori_msg.author
            else:
                user = ctx.author
            
        embed = disnake.Embed(title=f'{user.name}',color=self.bot_color(ctx))
        if user.avatar is not None:
            ava_url = user.avatar.with_size(1024)
            embed.description = f'[Link tải về]({user.avatar.url})'
        else:
            default_ava = int(user.discriminator) % 5 
            ava_url = disnake.Asset(url=f'https://cdn.discordapp.com/embed/avatars/{default_ava}.png', key='avatar', state='user1').with_size(1024)
            embed.description = f'Người dùng này không có ảnh đại diện. \nẢnh mặc định: [Link tải về]({ava_url})'
        embed.set_image(ava_url)
        current_time = datetime.now() 
        time = current_time.strftime('%H:%M:%S')
        embed.set_footer(text=f'Bởi: {ctx.author.name} Vào lúc: {time}')
        await ctx.reply(embed=embed)
    
    # add emoji bằng lệnh 
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def add(self, ctx, emoji: disnake.PartialEmoji):
        if emoji.is_custom_emoji():
            emoji_name = emoji.name
            emoji_data = await emoji.read()
            emoji_id = emoji.id
            existing_emojis = [e.name for e in ctx.guild.emojis]
            if emoji_name in existing_emojis:
                await ctx.send(f'Máy chủ đã tồn tại emoji <:{emoji_name}:{emoji_id}>    <a:aHTVN_ChikaBonk:1167128195938652160>')
            else:
                # tạo emoji tên sever đó
                await ctx.guild.create_custom_emoji(name=emoji_name, image=emoji_data)
                await ctx.send(f'Đã thêm vào máy chủ emoji <:{emoji_name}:{emoji_id}>    <a:aChisatoAHHHHHH:1167095573430665289> ')
        else:
            await ctx.send('Chỉ hỗ trợ emojis tùy chỉnh.')
                
    # add sticker bằng lệnh
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def adds(self, ctx, sticker_id: int):
        token = token
        url = f'https://discord.com/api/v10/guilds/{ctx.guild.id}/stickers/{sticker_id}'
        headers = {'Authorization':f'{token}'}
        
        # kiểm tra sticker có tồn tại không 
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            await ctx.send(f'Máy chủ đã tồn tại sticker {sticker_id} rồi   <a:aHTVN_ChikaBonk:1167128195938652160>')
        elif response.status_code == 400:
            await ctx.send(f'Ticker không tồn tại trong máy chủ. Hãy thêm nó bằng cách sử dụng giao diện Discord.')
        else:
            await ctx.send("Không thành công")
            
    # lấy màu của color vể chỉ lấy role
    @commands.command()
    async def color(self, ctx, *, role: Union[Role, Member]):
        color = None
        if isinstance(role, Role):
            color = role.color
        elif isinstance(role, Member):
            color = role.top_role.color
        
        if color:
            await ctx.reply(f'Role của {role} có màu: {role.color}')
        else: 
            await ctx.reply('Không tìm thấy role')
    


                
    
        
def setup(client):
    client.add_cog(Command(client))