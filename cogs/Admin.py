from yuno_import import *

class Admin(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        
    def bot_color(self, ctx):
        bot_role = ctx.guild.me.top_role
        color = bot_role.color
        return color

    async def send_private_message(self, ctx, user, msg, anonymous=False):
        if user is None:
            await ctx.reply("Không thể tìm thấy người dùng đã cung cấp.")
            return

        await ctx.message.delete()
        embed = discord.Embed(color=0x9812F0)
        if msg and msg.startswith('true '):
            anonymous = True
            arg = msg.split(" ", 1)[1] if len(msg.split(" ")) > 1 else None
        else:
            anonymous = False
            arg = msg
        title = 'Được gửi bởi kẻ trộm Ánh Trăng' if anonymous else f'Được gửi bởi {ctx.author.name}'
        embed.title =  title
        embed.description = arg
        embed.set_footer(text=f'Vào lúc: {datetime.now().strftime("%H:%M")}')
        await user.send(embed=embed)
    
    # kick thành viên
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.reply(f'Người dùng {member.mention} đã bị kick ra khỏi sever.')
        
    @kick.error
    async def kick_error(self, ctx, error):
        await ctx.reply('Nhà ngươi làm gì có tư cách đó.')

    # ban thành viên
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.reply(f'Người dùng {member.mention} đã bị ban ra khỏi sever.')
        
    @ban.error
    async def ban_error(self, ctx, error):
        await ctx.reply('Nhà ngươi làm gì có tư cách đó.') 
            
    # dms một cách bình thường
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def dms(self, ctx, user:discord.Member, *, arg=None):
        await self.send_private_message(ctx, user, arg)


    # chat riêng với id tranhs người nhanh nhạy 
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def dmsid(self, ctx, user_id: int, *, arg=None):
        user = ctx.guild.get_member(user_id)
        await self.send_private_message(ctx, user, arg)
    
    
    # add role 
    @commands.command(pass_context = True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def arole(self, ctx, role: discord.Role, *, user: discord.Member):
        if role in user.roles:
            await ctx.reply(f'{user.mention} đã có role {role}')
        else: 
            await user.add_roles(role)
            await ctx.reply(f'Đã thêm role {role} cho {user.mention}')
            
    @arole.error
    async def role_error(self, ctx, error):
        await ctx.reply('Nhà ngươi làm gì có tư cách đó.')
            
    # remove role
    @commands.command(pass_context = True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def rrole(self, ctx, role: discord.Role, *, user: discord.Member):
        if role in user.roles:
            await user.remove_roles(role)
            await ctx.reply(f'Đã xóa role {role} của {user.mention}')
        else: 
            await ctx.reply(f'{user.mention} không có role {role}')
            
    @rrole.error    
    async def role_error(self, ctx, error):
        await ctx.reply('Nhà ngươi làm gì có tư cách đó.')
    
    
    # error listener event
    @commands.command()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply('Nhà ngươi làm gì có tư cách đó.')
    

    
    
    
    
def setup(client):
    client.add_cog(Admin(client))