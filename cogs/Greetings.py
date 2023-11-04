import disnake
from disnake.ext import commands
from disnake import *
from disnake.ext.commands import *
from datetime import datetime, timedelta
import requests
import json
import os

class Greetings(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        self.join_id = None
        self.left_id = None
        self.joinmsg = 'Chào mừng bạn đến sever.'
        self.leftmsg = 'Rất tiếc phải tạm biệt nhưng hẹn gặp lại ở một ngày không xa.'
        self.joinbnr = None
        self.leftbnr = None
    
    # event
    @commands.Cog.listener()
    async def on_member_join(self, mem):
        channel = self.client.get_channel(self.join_id)
        embed= disnake.Embed(description=self.joinmsg,
                            color=0x30FF07)
        if mem.avatar is not None:
            ava_url = mem.avatar.url
        else:
            default_ava = int(mem.discriminator) % 5
            ava_url = disnake.Asset(url=f'https://cdn.discordapp.com/embed/avatars/{default_ava}.png', key='avatar', state='user1')
        embed.set_author(name=f'{mem.name}', icon_url=ava_url)
        embed.set_thumbnail(url=ava_url)    
        embed.set_image(self.joinbnr)
        timejoin = datetime.now().strftime('%H:%M:%S')
        embed.set_footer(text=f'Vào lúc: {timejoin}')
        await channel.send(f'Xin chào {mem.mention}')
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, mem):
        channel = self.client.get_channel(self.left_id)
        embed= disnake.Embed(description=self.leftmsg,
                            color=0xFF0707)
        if mem.avatar is not None:
            ava_url = mem.avatar.url
        else:
            default_ava = int(mem.discriminator) % 5
            ava_url = disnake.Asset(url=f'https://cdn.discordapp.com/embed/avatars/{default_ava}.png', key='avatar', state='user1')
        embed.set_author(name=f'{mem.name}', icon_url=ava_url)
        embed.set_thumbnail(url=ava_url)
        embed.set_image(self.leftbnr)
        timeleft = datetime.now().strftime('%H:%M:%S')
        embed.set_footer(text=f'Vào lúc: {timeleft}')
        await channel.send(f'Hẹn gặp lại {mem.mention}')
        await channel.send(embed=embed)
    
    
    # command 
    @commands.command()
    async def hi(self, ctx):
        user = ctx.author
        await ctx.reply(f'Xin Chào {user.mention}.')
        
    @commands.command()
    async def greetingcn(self, ctx, channel: disnake.TextChannel):
        if channel:
            id = channel.id
            self.join_id = self.left_id = id
            await ctx.reply(f'Kênh chào và rời đã được đặt ở <#{channel.id}>')
        else:
            await ctx.reply(f'Không tìm thấy channel <#{channel.id}>')  
        
    @commands.command()
    async def joincn(self, ctx, channel: disnake.TextChannel):
        if channel:
            id = channel.id
            self.join_id = id
            await ctx.reply(f'Kênh chào đã được đặt ở <#{channel.id}>')
        else:
            await ctx.reply(f'Không tìm thấy channel <#{channel.id}>')
            
    @commands.command()
    async def leftcn(self, ctx, channel: disnake.TextChannel):
        if channel:
            id = channel.id
            self.left_id = id
            await ctx.reply(f'Kênh rời đã được đặt ở <#{channel.id}>')
        else:
            await ctx.reply(f'Không tìm thấy channel <#{channel.id}>')
            
    @commands.command()
    async def joinmsg(self, ctx, *message):
        if message is None:
            await ctx.reply('Vui lòng nhập tin nhắn chào mừng.')
        else:
            msg = ' '.join(message)
            self.joinmsg = msg
            await ctx.reply('Đã thiết lập tin nhắn chào mừng')
        
    @commands.command()
    async def leftmsg(self, ctx, *message):
        if message is None:
            await ctx.reply('Vui lòng nhập tin nhắn tạm biệt.')
        else:
            msg = ' '.join(message)
            self.leftmsg = msg
            await ctx.reply('Đã thiết lập tin nhắn tạm biệt')
            
    @commands.command()
    async def joinbnr(self, ctx, url):
        if url is None:
            await ctx.reply('Vui lòng nhập URL hình ảnh cho banner chào mừng')
        else: 
            self.joinbnr = url
            await ctx.reply('Đã đặt banner chào mừng thành công')
    
    @commands.command()
    async def leftbnr(self, ctx, url):
        if url is None:
            await ctx.reply('Vui lòng nhập URL hình ảnh cho banner tạm biệt')
        else: 
            self.leftbnr = url
            await ctx.reply('Đã đặt banner tạm biệt thành công')


def setup(client):
    client.add_cog(Greetings(client))