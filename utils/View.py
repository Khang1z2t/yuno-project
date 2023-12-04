from yuno_import import *

from utils import Embeds

class AddtoServer(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        button = discord.ui.Button(label='Thêm vào server', url='https://discord.com/api/oauth2/authorize?client_id=1163019882795909162&permissions=70368744177663&scope=bot%20applications.commands')
        self.add_item(button)
    
    @discord.ui.button(label='Ủng hộ tôi', style=discord.ButtonStyle.blurple, emoji='<a:omori_victory:1169166458664783985>')
    async def support_callback(self, button:discord.ui.Button, interaction:discord.Interaction):
        embed = await Embeds.Support.momo(interaction)
        view = SupportView()
        await interaction.response.send_message('Cảm ơn bạn đã ủng hộ tôi <a:2nekolove:1181244395006205954>', embed=embed, view=view, ephemeral=True)


class SupportView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.select(placeholder='Ủng hộ ở đây', min_values=1, max_values=1,
                       options=[discord.SelectOption(label='Momo', value='momo', emoji='<:yl_momo:1181228350732247133>'),
                                discord.SelectOption(label='Bank', value='bank', emoji='<:timo:1181230145017753640>'),
                                discord.SelectOption(label='Paypal', value='paypal', emoji='<:paypal:1181228556186030100>')])
    async def support_callback(self, select:discord.ui.Select, interaction:discord.Interaction):
        if select.values[0] == 'momo':
            embed = await Embeds.Support.momo(interaction)
        elif select.values[0] == 'bank':
            embed = await Embeds.Support.bank(interaction)
        elif select.values[0] == 'paypal':
            embed = await Embeds.Support.paypal(interaction)
        await interaction.response.edit_message(embed=embed, view=self)
