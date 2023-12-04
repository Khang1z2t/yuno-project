TOKEN = 'MTE2MzAxOTg4Mjc5NTkwOTE2Mg.GSjsN8.8NLkEA5v2Jj677HhquH_2nFpNfMGL7hIVzOaR0'
SPOTIFY_ID: str = ''
SPOTIFY_SECRET: str = ''

PREFIX = '!yuno '

BOT_COLOR = 0x9812f0

VC_TIMEOUT = 600
VC_TIMEOUT_DEFAULT = True
ALLOW_VC_TIMEOUT_EDIT = True

# nodes custom
NODES = [
    {'name' : 'Default', 'uri' : 'http://localhost:8888', 'pass': 'yuno.k', 'secure': False, 'use_http': True},
    {'name' : 'SirPlanCake', 'uri' : 'http://lava-v3.sirplancake.dev:2334', 'pass': 'e0krPn7)yX<@j=REb!x?dWtY', 'secure': False, 'use_http': True},
    {'name' : 'Darren', 'uri' : 'http://n1.ll.darrennathanael.com:2269', 'pass' : 'glasshost1984', 'secure': False, 'use_http': True}
]

# music help
HELP_PLAY = 'Phát âm thanh từ link hoặc tên'
HELP_PAUSE = 'Tạm dừng lại nhạc hiện tại'
HELP_RESUME = 'Tiếp tục phát tại nơi đã tạm dừng'
HELP_SKIP = 'Bỏ qua bài nhạc hiện tại và đến bài tiếp theo'
HELP_PREVIOUS = 'Quay lại bài nhạc trước đó'
HELP_STOP = 'Kết thúc bài hiện tại bao gồm cả danh sách phát'
HELP_PLAYLIST = 'Hiển thị danh sách phát'
HELP_CLEAR_PLAYLIST = 'Làm mới danh sách phát'
HELP_JOIN = 'Tham gia vào voice channel hiện tại'
HELP_LEAVE = 'Rời khỏi voice channel'
HELP_VOLUME = 'Thay đổi âm lượng'
HELP_LOOP = 'Lặp lại bài nhạc hiện tại'
HELP_REMOVE = 'Xóa bài nhạc khỏi danh sách phát'
HELP_SHUFFLE = 'Xáo trộn danh sách phát'
HELP_MOVE = 'Di chuyển bài nhạc trong danh sách phát'
