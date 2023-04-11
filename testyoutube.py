import logging
import telegram
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater
from googleapiclient.discovery import build
import os
import configparser
# 设置日志等级为 INFO
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# 从环境变量中获取 Telegram 机器人的 API 密钥和 YouTube API 密钥

url = 'https://comp7940-8e8fa-default-rtdb.firebaseio.com'
fb = firebase.FirebaseApplication(url, None)
config = configparser.ConfigParser()
config.read('config.ini')
TELEGRAM_API_KEY = config['TELEGRAM']['ACCESS_TOKEN']
YOUTUBE_API_KEY = config['YOUTUBE']['KEY']
updater = Updater(token=TELEGRAM_API_KEY, use_context=True)
dispatcher = updater.dispatcher

# 创建 Telegram 客户端实例
bot = telegram.Bot(token=TELEGRAM_API_KEY)

# 创建 YouTube 数据 API 客户端实例
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
url = 'https://comp7940-8e8fa-default-rtdb.firebaseio.com'
fb = firebase.FirebaseApplication(url, None)

# 定义 start 命令处理程序
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="欢迎使用视频搜索机器人！发送 /search [关键字] 来搜索相关视频。")

# 定义 search 命令处理程序
def search(update, context):
    # 获取搜索关键字
    query = ' '.join(context.args)

    # 搜索 YouTube 视频
    search_response = youtube.search().list(
        q=query,
        type='video',
        part='id,snippet',
        maxResults=5
    ).execute()

    # 构造视频列表消息
    message = ''
    for search_result in search_response.get('items', []):
        video_title = search_result['snippet']['title']
        video_url = f'https://www.youtube.com/watch?v={search_result["id"]["videoId"]}'
        message += f'{video_title}\n{video_url}\n\n'

    # 发送视频列表消息
    if message:
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='没有找到相关视频。')

# 定义文本消息处理程序
def text(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='请发送 /search [关键字] 来搜索相关视频。')

# 创建 Updater 实例并添加处理程序
updater = Updater(token=TELEGRAM_API_KEY, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('search', search))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, text))

# 启动机器人
updater.start_polling()
updater.idle()