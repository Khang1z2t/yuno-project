from yuno_import import *
from utils import Embeds

class SlashCommand(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        
    
    
    @discord.slash_command(name='id', description='Lấy id từ người dùng')
    async def slash_id(self, ctx, user: Option(discord.Member, "Chọn người dùng", required=True), private: Option(bool, "Chỉ hiển thị với bạn", required=False)):
        if private:
            await ctx.respond(f'ID của `` {user.name} `` là: {user.id}', ephemeral=True)
        else:
            await ctx.respond(f'ID của `` {user.name} `` là: {user.id}')

    @discord.slash_command(name='add_role', description="Thêm role vào thành viên.")
    @commands.has_permissions(manage_roles=True)
    async def slash_add_role(self, ctx, role: discord.Role, user: discord.Member, private: Option(bool, "Chỉ hiển thị với bạn")):
        await user.add_roles(role)
        if private:
            await ctx.respond(f'Đã thêm role {role.name} cho {user.name}', ephemeral=True)
        else:
            await ctx.respond(f'Đã thêm role {role.name} cho {user.name}')

        

    @discord.slash_command(name = "hello", description = "Say hello to the bot")
    async def say_hello(self, ctx):
        await ctx.respond("Hey!")
        

    


    

def setup(client):
    client.add_cog(SlashCommand(client))