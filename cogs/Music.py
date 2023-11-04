from yuno_import import *


class Music(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        self.playlist = {}
    
#     def play_next(self, ctx, id):
#         if id in self.playlist and self.playlist[id]:
#             voice = ctx.guild.voice_client
#             source = self.playlist[id].pop(0)
#             play = voice.play(source, after=lambda x=None: self.play_next(ctx, id))
            
#     def bot_color(self, ctx):
#         bot_role = ctx.guild.me.top_role
#         color = bot_role.color
#         return color

#     async def embeds_music(self, ctx, description=None, thumbnail=None, footer=False):
#         embed = disnake.Embed(color=self.bot_color(ctx))
#         embed.set_author(name=f'{ctx.author.name}', icon_url=ctx.author.avatar)
#         embed.description = f'**{description}**'
#         embed.set_thumbnail(url=thumbnail)
#         if footer:
#             embed.set_footer(text=f'Vào lúc: {datetime.now().strftime("%H:%M:%S")}')
#         await ctx.reply(embed=embed)
            
#     async def play_music(self, ctx, src):
#         voice = ctx.guild.voice_client
#         guild_id = ctx.message.guild.id
        
#         if not voice or not voice.is_connected():
#             if ctx.author.voice:
#                 channel = ctx.author.voice.channel
#                 await channel.connect()
#                 await ctx.guild.change_voice_state(channel=channel, self_deaf=True)
#                 voice = ctx.guild.voice_client
#                 play = voice.play(src, after=lambda x=None: self.play_next(ctx, guild_id))
#                 await self.embeds_music(ctx, 'Bắt đầu phát ...')
#             else:
#                 await self.embeds_music(ctx, 'Ơ bạn đã tham gia voice chat đâu??')
#         else:
#             if voice.is_playing() or voice.is_paused():
#                 if guild_id in self.playlist:
#                     self.playlist[guild_id].append(src)
#                 else:
#                     self.playlist[guild_id] = [src]
                    
#                 await self.embeds_music(ctx, 'Đã thêm vào danh sách phát.')
#             else:
#                 play = voice.play(src, after=lambda x=None: self.play_next(ctx, guild_id))
#                 await self.embeds_music(ctx, 'Bắt đầu phát...')
            
#     # các evt
#     @commands.Cog.listener()
#     async def on_voice_state_update(self, member, before, after):
#         if member.client and after.channel is None:
#             if not [m for m in before.channel.member if not m.client]:
#                 pass # kick bot ra khỏi voice 
    
    
    
    
    
#     # tham gia vào voice channel  
#     @commands.command(pass_context = True)
#     async def join(self, ctx):
#         if(ctx.author.voice):
#             await ctx.reply(f'{self.client.user.name} tới đây')
#             channel = ctx.author.voice.channel
#             voice = await channel.connect()
#             await ctx.guild.change_voice_state(channel=channel, self_deaf=True)
#         else:
#             await ctx.reply('Mầy có ở trong Voice Channel đâu?')

#     # rời khỏi voice channel
#     @commands.command(pass_context = True)
#     async def leave(self, ctx):
#         if(ctx.voice_client):
#             await ctx.guild.voice_client.disconnect()
#             await ctx.reply('Bố mầy cúc đây.')
#         else:
#             await ctx.reply('Mầy có ở trong Voice Channel đâu?')
            
#     # pause  
#     @commands.command(pass_context = True)
#     async def pause(self, ctx):
#         voice = disnake.utils.get(client.voice_clients, guild=ctx.guild)
#         if voice.is_playing():
#             voice.pause()
#             await ctx.reply('Đã tạm dừng.')
#         else:
#             await ctx.reply('Không có bài nào cả sao đừng được.')
            

#     # remuse tiếp tục phát khi pause
#     @commands.command(pass_context = True)
#     async def resume(self, ctx):
#         voice = disnake.utils.get(client.voice_clients, guild=ctx.guild)
#         if voice.is_paused():
#             voice.resume()
#             await ctx.reply('Đã tiếp tục.')
#         else:
#             await ctx.reply('Không có bài nào cả sao típ được.')

#     # stop
#     @commands.command(pass_context = True)
#     async def stop(self, ctx):
#         voice = disnake.utils.get(client.voice_clients, guild=ctx.guild)
#         voice.stop()
#         await ctx.reply('Đã dừng.')

#     # play (dã cải tiến sơ sơ)
#     @commands.command(pass_context = True)
#     async def p(self, ctx, *, url=None):
#         if url is None:
#             await self.embeds_music(ctx, 'Vui lòng nhập tên nhạc hoặc link nhạc.')
#             return
        
#         source = FFmpegPCMAudio("./audio/"+url+'.mp3')
#         await self.play_music(ctx, source)
        
#     @commands.command(pass_context = True)
#     async def play(self, ctx, *, url=None):
#         if url is None:
#             await self.embeds_music(ctx, 'Vui lòng nhập tên nhạc hoặc link nhạc.')
#             return
        
#         source = FFmpegPCMAudio("./audio/"+url+'.mp3')
#         await self.play_music(ctx, source)
                

                
def setup(client):
    client.add_cog(Music(client))