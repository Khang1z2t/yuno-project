import disnake
from disnake.ext import commands
from disnake import *
from disnake.ext.commands import *
from datetime import datetime, timedelta
import requests
import json
import os
import asyncio
import wavelink
import typing as t 
from typing import Union
import youtube_dl

class AlreadyConnectedToChannel(commands.CommandError):
    pass

class NoVoiceChannel(commands.CommandError):
    pass

class QueueIsEmpty(commands.CommandError):
    pass

class Queue:
    def __init__(self):
        self.queue = []
        self.position = 0
    
    def add(self, *args):
        self._queue.extend(args)
        
    def get_first_track(self):
        if not self._queue:
            raise QueueIsEmpty

        return self._queue[0]
    
    def get_next_track(self):
        if not self._queue:
            raise QueueIsEmpty
        
        self.position += 1
        
        if self.position > len(self._queue) - 1:
            return None
        
        return self._queue[self.position]



class Player(wavelink.Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    async def connect(self, ctx, channel=None):
        if self.is_connected:
            raise AlreadyConnectedToChannel
        
        if (channel := getattr(ctx.author.voice, 'channel', channel)) is None:
            raise NoVoiceChannel
        
        await super().connect(channel.id)
        return channel
    
    
    async def disconnect(self):
        try:
            await self.cleanup()
        except KeyError:
            pass

class Music_test(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.queue = Queue()
        self.client.loop.create_task(self.connect_nodes())
        
    
    async def cog_check(self, ctx):
        if isinstance(ctx.channel, disnake.DMChannel):
            await ctx.send('Nhạc không hỗ trợ ở DMs')
            return False
        return True
    
    async def connect_nodes(self):
        await self.client.wait_until_ready()
        
        await wavelink.NodePool.create_node(bot = self.client,
                                            host = '127.0.0.1',
                                            port = 2333,
                                            password = 'yuno.k',
                                            region = 'asia')
                
            
    # def get_player(self, obj):
    #     if isinstance(obj, commands.Context):
    #         return self.client.wavelink.get_player(obj.guild.id, cls=wavelink.Player, context=obj)
    #     if isinstance(obj, disnake.Guild):
    #         return self.client.wavelink.get_player(obj.id, cls=wavelink.Player)
     
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not member.bot and after.channel is None:
            if not [m for m in before.channel.members if not m.bot]:
                await asyncio.sleep(60)
                if not [m for m in before.channel.members if not m.bot]:
                    await self.embeds_music(member, f'Tự động rời vì không còn ai ở <#{before.channel.id}>')
                    await before.channel.guild.voice_client.disconnect()
                

                
    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print(f'Node: <{node.identifier}> đã sẵn sàng!')
        
    @commands.command(name='connect', aliases=['join'])
    async def connect_cmd(self, ctx, *, channel: t.Optional[disnake.VoiceChannel]):
        if ctx.voice_client:
            raise AlreadyConnectedToChannel
        elif not channel and ctx.author.voice:
            await ctx.author.voice.channel.connect(cls=wavelink.Player)
            await self.embeds_music(ctx, f'{self.client.user.name} này đã kết nối đến <#{ctx.author.voice.channel.id}>')
            await self.client.user.edit(deafen=True)
        else:
            raise NoVoiceChannel
        # player = self.get_player(ctx)
        # channel = await player.connect(ctx,channel)
        # await self.embeds_music(ctx, f'{self.client.user.name} này đã kết nối đến <#{ctx.author.voice.channel.id}>')
        
    @connect_cmd.error
    async def connect_error(self, ctx, error):
        if isinstance(error, AlreadyConnectedToChannel):
            await self.embeds_music(ctx, f'Đang kết nối ở voice channel <#{ctx.voice_client.channel.id}>', disnake.Colour.red())
        elif isinstance(error, NoVoiceChannel):
            await self.embeds_music(ctx, 'Bạn phải tham gia voice channel', disnake.Colour.red())
    
    @commands.command(name='disconnect', aliases=['leave'])
    async def disconnect_cmd(self, ctx):
        user_vc = ctx.author.voice
        bot_vc = ctx.me.voice
        if not user_vc:
            raise NoVoiceChannel 
        if user_vc and bot_vc.channel != user_vc.channel:
            raise AlreadyConnectedToChannel
        else:
            await self.embeds_music(ctx, f'Đang rời khỏi <#{ctx.voice_client.channel.id}>')
            await ctx.voice_client.disconnect()
        # player = self.get_player(ctx)
        # await player.disconnect()
        # await self.embeds_music(ctx, f'Đang rời khỏi <#{ctx.voice_client.channel.id}>')
        
    @commands.command(name='play', aliases=['play'])
    async def play_cmd(self, ctx, *, query:t.Optional[str]):
        
    
    @disconnect_cmd.error
    async def connect_error(self, ctx, error):
        if isinstance(error, AlreadyConnectedToChannel):
            await self.embeds_music(ctx, f'Đang kết nối ở voice channel <#{ctx.voice_client.channel.id}>', disnake.Colour.red())
        elif isinstance(error, NoVoiceChannel):
            await self.embeds_music(ctx, 'Bạn phải tham gia voice channel', disnake.Colour.red())
    
    # embed
    def bot_color(self, ctx):
        bot_role = ctx.guild.me.top_role
        color = bot_role.color
        return color

    async def embeds_music(self, ctx, description=None, colour=None, thumbnail=None, footer=False):
        if colour is None:
            colour = self.bot_color(ctx)
        embed = disnake.Embed(color=colour)
        embed.set_author(name=f'{ctx.author.name}', icon_url=ctx.author.avatar)
        embed.description = f'**{description}**'
        embed.set_thumbnail(url=thumbnail)
        if footer:
            embed.set_footer(text=f'Vào lúc: {datetime.now().strftime("%H:%M:%S")}')
        await ctx.reply(embed=embed)
        
def setup(client):
    client.add_cog(Music_test(client))    