from yuno_import import *
# API key
from apiKey import *

client = commands.Bot(command_prefix='!yuno ', intents=disnake.Intents.all())


@client.event
async def on_ready():
    await client.change_presence(activity=disnake.Game(name='Real Life with Yuno', url='https://youtube.com/@yuno.k?si=JvsrRTZgkGWB_CgM'))
    print('-------------------------------------------')
    print(f'{client.user.name} đã xuất hiện để giúp đỡ bạn.')
    print(f'ID: {client.user.id}')
    print(f'Độ trễ: {client.latency*1000:,.0f} ms')
    print('-------------------------------------------')


initial_extensions = []

script_dir = os.path.dirname(__file__)  # Lấy thư mục của tệp thực thi
cogs_dir = os.path.join(script_dir, 'cogs') # Tạo đường dẫn tuyệt đối đến thư mục cogs

for filename in os.listdir(cogs_dir):
    if filename.endswith('.py'):
        initial_extensions.append("cogs." + filename[:-3])


if __name__ == '__main__':
    for extension in initial_extensions:
        client.load_extension(extension)
    
client.run(token)