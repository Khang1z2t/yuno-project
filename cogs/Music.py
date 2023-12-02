from yuno_import import *

from utils import Embeds



class Music(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        self.text_channel = None
        self.requester = None
        client.loop.create_task(self.node_connect())
        
        
    async def node_connect(self):
        await self.client.wait_until_ready()
        
        node: wavelink.Node = wavelink.Node(
            uri = config.LAVALINK_URI,
            password = config.LAVALINK_PASS,
            secure = config.LAVALINK_SECURE,
            use_http = config.LAVALINK_USE_HTTP
        )
        
        await wavelink.NodePool.connect(
            client = self.client,
            nodes = [node]
        )
    
    
    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print(f'Node <{node.id}> đã sắn sàng!')
        
        
    @commands.Cog.listener()
    async def on_voice_state_update(self, 
                                    member: discord.Member, 
                                    before: discord.VoiceState,
                                    after: discord.VoiceState):
        try:
            guild = after.channel.guild
        except Exception:
            guild = before.channel.guild
            
        vc: wavelink.Player = guild.voice_client
        if before.channel is not None and after.channel is None and guild.voice_client and len(before.channel.members) < 2:
            await asyncio.sleep(60)
            if len(before.channel.members) < 2:
                await vc.disconnect()
                
                try:
                    channel = self.text_channel
                    await channel.send(
                        embed = await Embeds.create_embed(
                            channel,
                            f'Ngắt kết nối vì không có user tại channel <#{before.channel.id}>.'
                        )
                    )
                except Exception as e:
                    print(e)
                    return
    
    @commands.Cog.listener()
    async def on_wavelink_track_end(self, payload: wavelink.TrackEventPayload):
        try:
            ctx = payload.player.ctx
            vc: wavelink.Player = ctx.guild.voice_client
            channel = self.text_channel
            
            if vc is None:
                return
            
            if vc.is_playing() is True:
                return
            
            if vc.loop:
                return await vc.play(payload.track)
                
            if vc.queue.is_empty:
                await channel.send(
                    embed = await Embeds.create_embed(channel, f'Không còn bài nào trong danh sách phát')
                )
                await asyncio.sleep(300)
                if not vc.queue.is_empty or vc.is_playing() is True:
                    return
                await vc.disconnect()
            
            if (isinstance(payload.track, wavelink.YouTubeTrack) or isinstance(payload.track, wavelink.SoundCloudTrack)):
                vc.previous = payload.track
            else:
                songs = await wavelink.YouTubeTrack.search(payload.track.title)
                vc.previous = songs[0]
                
                next_song = vc.queue.get()
                
                await vc.play(next_song)
                embed = await Embeds.music_embed(ctx, f'{next_song}', f'{next_song.uri}', f'{next_song.thumbnail}', 
                                                 f'`{next_song.author}` | `{Embeds.get_time(next_song.duration)}` | <@{self.requester.id}>')
                await channel.send(embed=embed, mention_author=False)
                
        except Exception as e:
            print(e)
            return
    
    @commands.command(name='join', aliases=['connect', 'connec'], help=config.HELP_JOIN)
    async def join_cmd(self, ctx, channel:t.Optional[discord.VoiceChannel]):
        try:
            self.text_channel = ctx.channel
            if channel is None:
                channel = ctx.author.voice.channel
            
            node = wavelink.NodePool.get_node()
            player = node.get_player(ctx.guild)
            
            if player is not None:
                if player.is_connected():
                    embed = await Embeds.create_embed(ctx, f'{self.client.user.name} đang kết nói ở channel <#{channel.id}>', Color.red())
                    await ctx.reply(embed=embed)
                    return
            await channel.connect(cls=wavelink.Player)
            embed = await Embeds.create_embed(ctx, f'Đã kết nối đến <#{channel.id}>')
            await ctx.reply(embed=embed)
        except Exception as e:
            print(e)
            return
        
    
    @commands.command(name='leave', aliases=['disconnect', 'disc'], help=config.HELP_LEAVE)
    async def leave_cmd(self, ctx):
        try:
            if not ctx.author.voice:
                await ctx.reply(
                    embed = await Embeds.Music_checks.check_join(ctx)
                    )
                return
            
            if not ctx.voice_client:
                await ctx.reply(
                    embed = await Embeds.Music_checks.check_disconnect(ctx)
                )
                return
            
            if ctx.author.voice and ctx.voice_client.channel != ctx.author.voice.channel:
                embed = await Embeds.create_embed(ctx, f'{self.client.user.name} đang kết nối ở channel <#{ctx.voice_client.channel.id}>', Color.red())
                await ctx.reply(embed=embed)
            else:
                embed = await Embeds.create_embed(ctx, f'Đã rời khỏi channel <#{ctx.voice_client.channel.id}>')
                await ctx.reply(embed=embed)
                await ctx.voice_client.disconnect()
        except Exception as e:
            print(e)
            return
    
    @commands.command(name='play', aliases=['p'], help=config.HELP_PLAY)
    async def play_cmd(self, ctx, *, song: str = None):
        try:
            self.text_channel = ctx.channel
            self.requester = ctx.author
            if song is None:
                embed = await Embeds.create_embed(ctx, f'Vui lòng nhập tên bài hát hoặc link', Color.red())
                await ctx.reply(embed=embed)
                return
            
            if not getattr(ctx.author.voice, 'channel', None):
                return await ctx.reply(
                    embed = await Embeds.Music_checks.check_join(ctx)
                )
            
            if not ctx.voice_client:
                vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
            else:
                vc: wavelink.Player = ctx.voice_client
            
            if vc.is_paused() is True:
                await vc.resume()
            
            if vc.queue.is_empty and not vc.is_playing():
                try:
                    songs = await wavelink.YouTubeTrack.search(song)
                    song = songs[0]
                except Exception:
                    return await ctx.reply(
                        embed = await Embeds.create_embed(ctx, f'Không tìm thấy bài hát nào có tên {song}', Color.red())
                    )
                
                if int(song.duration) > 18000000:
                    return await ctx.reply(
                        embed = await Embeds.create_embed(ctx, f'Bài hát dài quá dài, vui lòng chọn bài khác.')
                    )
                
                await vc.play(song)
                embed = await Embeds.music_embed(ctx, f'{song}', f'{song.uri}', f'{song.thumbnail}', 
                                                f'`{song.author}` | `{Embeds.get_time(song.duration)}` | <@{ctx.author.id}>')
                await ctx.reply(embed=embed, mention_author=False)
            
            else:
                try:
                    songs = await wavelink.YouTubeTrack.search(song)
                    song = songs[0]
                except Exception:
                    return await ctx.reply(
                        embed = await Embeds.create_embed(ctx, f'Không tìm thấy bài hát nào có tên {song}', Color.red())
                    )
                
                if int(song.duration) > 18000000:
                    return await ctx.reply(
                        embed = await Embeds.create_embed(ctx, f'Bài hát dài quá dài, vui lòng chọn bài khác.')
                    )
                
                await vc.queue.put_wait(song)
                embed = await Embeds.music_embed(ctx, f'{song}', f'{song.uri}', f'{song.thumbnail}', f'Đã thêm vào danh sách phát')
                await ctx.reply(embed=embed, mention_author=False)
                
            vc.ctx = ctx
            if not hasattr(vc, "loop"):
                setattr(vc, "loop", False)
            if not hasattr(vc, "previous"):
                setattr(vc, "previous", None)
        except Exception as e:
            print(e)
            return
                
    
    @commands.command(name='pause', aliases=['pa'], help=config.HELP_PAUSE)
    async def pause_cmd(self, ctx):
        try:
            if not getattr(ctx.author.voice, 'channel', None):
                return await ctx.reply(
                    embed = await Embeds.Music_checks.check_join(ctx)
                )
            elif not ctx.guild.voice_client:
                return await ctx.reply(
                    embed = await Embeds.Music_checks.check_connected(ctx)
                )
            else:
                vc: wavelink.Player = ctx.voice_client
            
            if vc.is_playing() is False:
                return await ctx.reply(
                    embed = await Embeds.create_embed(ctx, f'Không có bài nào đang phát', Color.red())
                )
            
            if vc.is_paused() == False:
                await vc.pause()
                await ctx.reply(
                    embed = await Embeds.create_embed(ctx, f'Đã tạm dừng bài hát'), mention_author=False
                )
            else:
                return await ctx.reply(
                    embed = await Embeds.create_embed(ctx, f'Bài hát đã được tạm dừng', Color.red())
                )
        except Exception as e:
            print(e)
            return
     
    
    @commands.command(name='resume', aliases=['re'], help=config.HELP_RESUME)
    async def resume_cmd(self, ctx):
        try:
            if not getattr(ctx.author.voice, 'channel', None):
                return await ctx.reply(
                    embed = await Embeds.Music_checks.check_join(ctx)
                    )
            elif not ctx.guild.voice_client:
                return await ctx.reply(
                    embed = await Embeds.Music_checks.check_connected(ctx)
                )
            else:
                vc: wavelink.Player = ctx.voice_client
            
            if vc.is_paused() == True:
                await vc.resume()
                embed = await Embeds.create_embed(ctx, f'Đã tiếp tục bài hát')
                await ctx.reply(embed=embed, mention_author=False)
            else:
                return await ctx.reply(
                    embed = await Embeds.create_embed(ctx, f'Bài hát đã được phát', Color.red())
                )
        except Exception as e:
            print(e)
            return
            
    
    @commands.command(name='skip', aliases=['sk'], help=config.HELP_SKIP)
    async def skip_cmd(self, ctx):
        try:
            if not getattr(ctx.author.voice, 'channel', None):
                return await ctx.reply(
                    embed = await Embeds.Music_checks.check_join(ctx)
                    )
            elif not ctx.guild.voice_client:
                return await ctx.reply(
                    embed = await Embeds.Music_checks.check_connected(ctx)
                )
            else:
                vc: wavelink.Player = ctx.voice_client
            
            if vc.queue.is_empty:
                return await ctx.reply(
                    embed = await Embeds.create_embed(ctx, f'Không có bài nào trong danh sách phát', Color.red())
                )
            
            if vc.loop:
                return await ctx.reply(
                    embed = await Embeds.create_embed(ctx, f'Vui lòng tắt lặp lại bài hát trước khi bỏ qua bài hát', Color.red())
                )
            
            track = vc.current
            vc.previous = track
            
            position = int(vc.current.duration) * 10000 
            await vc.seek(position=position)
            await ctx.reply(
                embed = await Embeds.create_embed(ctx, f'Đã bỏ qua bài hát'), mention_author=False
            )
        except Exception as e:
            print(e)
            return
        
    
    @commands.command(name='previous', aliases=['pre'], help=config.HELP_PREVIOUS)
    async def previous_cmd(self, ctx):
        try:
            if not getattr(ctx.author.voice, 'channel', None):
                return await ctx.reply(
                    embed = await Embeds.Music_checks.check_join(ctx)
                    ) 
            elif not ctx.guild.voice_client:
                return await ctx.reply(
                    embed = await Embeds.Music_checks.check_connected(ctx)
                )
            else:
                vc: wavelink.Player = ctx.voice_client

            if vc.loop:
                return await ctx.reply(
                    embed = await Embeds.create_embed(ctx, f'Vui lòng tắt lặp lại bài hát trước khi quay lại bài hát', Color.red())
                )
            
            if vc.previous is not None:
                vc.queue.put_at_front(vc.current)
                vc.queue.put_at_front(vc.previous)
                
                postition = int(vc.previous.duration) * 10000
                await vc.seek(position=postition)
                
                vc.previous = None
                
                await ctx.reply(
                    embed = await Embeds.create_embed(ctx, f'Đã quay lại bài hát trước'), mention_author=False
                )
            else:
                return await ctx.reply(
                    embed = await Embeds.create_embed(ctx, f'Không có bài hát trước đó', Color.red())
                )
            
        except Exception as e:
            print(e)
            return
            
    
    
    @commands.command(name='stop', aliases=['st'], help=config.HELP_STOP)
    async def stop_cmd(self, ctx):
        try:
            if not getattr(ctx.author.voice, 'channel', None):
                return await ctx.reply(
                    embed = await Embeds.Music_checks.check_join(ctx)
                    ) 
            elif not ctx.guild.voice_client:
                return await ctx.reply(
                    embed = await Embeds.Music_checks.check_connected(ctx)
                )
            else:
                vc: wavelink.Player = ctx.voice_client
                
            if not vc.is_playing():
                return await ctx.reply(
                    embed = await Embeds.create_embed(ctx, f'Không có bài nào đang phát', Color.red())
                )    
            
            await vc.stop()
            await vc.disconnect()
        except Exception as e:
            print(e)
            return


    @commands.command(name='loop', aliases=['l'], help=config.HELP_LOOP)
    async def loop_cmd(self, ctx):
        try:
            if not getattr(ctx.author.voice, 'channel', None):
                return await ctx.reply(
                    embed = await Embeds.Music_checks.check_join(ctx)
                    )
            elif not ctx.guild.voice_client:
                return await ctx.reply(
                    embed = await Embeds.Music_checks.check_connected(ctx)
                )
            else:
                vc: wavelink.Player = ctx.voice_client
                
            if vc.is_playing() is False:
                return await ctx.reply(
                    embed = await Embeds.create_embed(ctx, f'Không có bài nào đang phát', Color.red())
                )    
            
            if vc.loop:
                vc.loop = False
                await ctx.reply(
                    embed = await Embeds.create_embed(ctx, f'Đã tắt lặp lại bài hát'), mention_author=False
                )
            else:
                vc.loop = True
                await ctx.reply(
                    embed = await Embeds.create_embed(ctx, f'Đã bật lặp lại bài hát'), mention_author=False
                )
        except Exception as e:
            print(e)
            return
    
    
    @commands.command(name='volume', aliases=['vol', 'v'], help=config.HELP_VOLUME)
    async def volume_cmd(self, ctx, volume: int = None):
        try:
            if not getattr(ctx.author.voice, 'channel', None):
                return await ctx.reply(
                    embed = await Embeds.Music_checks.check_join(ctx)
                    )
            elif not ctx.guild.voice_client:
                return await ctx.reply(
                    embed = await Embeds.Music_checks.check_connected(ctx)
                )
            else:
                vc: wavelink.Player = ctx.voice_client
                
            if (volume is None) or (type(volume) is not int):
                return await ctx.reply(
                    embed = await Embeds.create_embed(ctx, f'Vui lòng nhập âm lượng chính xác', Color.red())
                )
            
            if not(0 <= volume <= 100):
                return await ctx.reply(
                    embed = await Embeds.create_embed(ctx, f'Vui lòng nhập âm lượng từ 0 đến 200', Color.red())
                )
            
            await vc.set_volume(volume)
            await ctx.reply(
                embed = await Embeds.create_embed(ctx, f'Đã thay đổi âm lượng thành {volume}'), mention_author=False
            )
        except Exception as e:
            print(e)
            return
            
            
        
def setup(client):
    client.add_cog(Music(client))