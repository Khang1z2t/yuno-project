from yuno_import import *

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.client.remove_command('help')

    @commands.command(name='help')
    async def help_cmd(self, ctx):
        await ctx.reply('help')

def setup(client):
    client.add_cog(Help(client))