import datetime

import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import Bot
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import Filters
from telegram.ext import MessageHandler, CommandHandler
from telegram.ext import Updater
from telegram.utils.request import Request
import re
import uuid
from ugc.models import Profile
from bs4 import BeautifulSoup
from ugc.models import Message_url

def log_errors(f):
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message = f'Error: {e}'
            print(error_message)
            raise e

    return inner


@log_errors
def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    url = update.message.text

    # save user data
    try:
        Profile(
            external_id=chat_id,
            name=update.message.from_user.username,
            first_name=update.message.from_user.first_name,
            l_name=update.message.from_user.last_name,
            created_at=datetime.datetime.now(),
            # avatar=update.message.from_user.get_profile_photos()
        ).save()
        update.message.reply_text('Please send a link')
    except Exception as e:
        print(e)
        update.message.reply_text('Please send a link')


@log_errors
def do_echo(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    url = update.message.text

    # show status
    print('start writing')

    # making soup and get link
    try:
        # print(datetime.datetime.now())
        update.message.reply_text('Please wait ...')
        data = requests.get(url)
        soup = BeautifulSoup(data.text, 'html.parser')
        video_url = soup.find(attrs={"data-quality": "240p"})['src']
        r = requests.get(video_url, allow_redirects=True)
    except Exception as e:
        print(e)
        update.message.reply_text('Oops...Invalid url or the size of video above 50 MB')
        return

    # getting file name
    file_name = f'{uuid.uuid4()}.mp4'

    # writing to os
    with open(f"../../tga/videos/{file_name}", 'wb') as f:
        f.write(r.content)

    # show status
    update.message.reply_text('Finished ✅')
    print('writing has been ended')

    # save url to db
    Message_url(profile=chat_id, text=url, created_at=datetime.datetime.now()).save()

    # send final result
    update.message.reply_video(video=open(f'../../../tga/videos/{file_name}', 'rb'))
    # update.message.reply_document(document=open(f"../../../videos/{file_name}", 'rb'))


class Command(BaseCommand):
    help = 'Telegram bot'

    def handle(self, *args, **options):
        request = Request(
            connect_timeout=3.5,
            read_timeout=4.0,
            con_pool_size=8
        )

        bot = Bot(
            request=request,
            token=settings.TOKEN
            # base_url=settings.PROXY_URL
        )

        updater = Updater(
            bot=bot,
            use_context=True,
        )
        print('running')

        start_handler = CommandHandler('start', start)
        message_handler = MessageHandler(Filters.text, do_echo)
        updater.dispatcher.add_handler(start_handler)
        updater.dispatcher.add_handler(message_handler)

        updater.start_polling()
        updater.idle()
