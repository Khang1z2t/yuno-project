from yuno_import import *

class SlashCommand(commands.Cog):
    
    def __init__(self, client):
        self.client = client
    
    @commands.slash_command(
        name='id',
        description='Lấy id của người dùng', 
        options=[Option(name='user', description='Chọn người dùng để lấy ID của họ', type=OptionType.user, required=True)])
    async def id(self, ctx: disnake.AppCmdInter):
        user = ctx.options['user']
        await ctx.response.send_message(f'ID của {user} là: {user.id}')



def setup(client):
    client.add_cog(SlashCommand(client))