import datetime
import re
import uuid
import requests

from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import MessageHandler, CommandHandler, CallbackQueryHandler, CallbackContext, Filters, Updater
from telegram.utils.request import Request

from ugc.models import Profile
from bs4 import BeautifulSoup
from ugc.models import Message_url
from ._base import BotBase


# convert to audio
# import moviepy.editor as mp

class Command(BotBase):

    def start(self, update: Update, context: CallbackContext) -> None:
        chat_id = update.message.chat_id
        url = update.message.text

        # save user data
        try:
            Profile(
                external_id=chat_id,
                name=update.message.from_user.username,
                first_name=update.message.from_user.first_name,
                l_name=update.message.from_user.last_name,
                created_at=datetime.datetime.now()
            ).save()
            update.message.reply_text('Hi! This bot can download videos from a website Muhajeer! \n\n'
                                      'Please send a link from website www.muhajeer.com', disable_web_page_preview=True)
        except Exception as e:
            print(e)
            update.message.reply_text('Hi! This bot can download videos from a website Muhajeer! \n\n'
                                      'Please send a link from website www.muhajeer.com', disable_web_page_preview=True)

    def do_echo(self, update: Update, context: CallbackContext) -> None:
        chat_id = update.message.chat_id
        url = update.message.text
        message_id = update.message.message_id
        # getting Telegram profile information from database
        user = Profile.objects.get(external_id=chat_id)

        # show status
        print('start writing')

        # making soup and get link
        try:
            buttons = [
                [
                    InlineKeyboardButton("🎥 240p", callback_data='down240'),
                    InlineKeyboardButton("🎥 360p", callback_data='down360'),
                    InlineKeyboardButton("🎥 480p", callback_data='down480'),
                    InlineKeyboardButton("🎥 720p", callback_data='down720')
                ]
            ]
            update.message.reply_text('Please wait ...')
            data = requests.get(url)
            soup = BeautifulSoup(data.text, 'html.parser')
            snd_msg = f'🎥  <a href="{url}"> {soup.title.string}</a>\n\n'
            video_url = soup.find(attrs={"data-quality": "480p"})['src']
            # msg = snd_msg
            # try:
            #     video_url = soup.find(attrs={"data-quality": "720p"})['src']
            # except Exception as e:
            #     print(e)
            #     video_url = soup.find(attrs={"data-quality": "480p"})['src']
            # print("vavava")
            # # re_video_url1 = soup.find(attrs={"data-quality": "240p"})['src']
            # try:
            #     if soup.find(attrs={"data-quality": "240p"})['src'] is not None:
            #         print("salom")
            #         # video_url1 = re_video_url1
            #         res1 = requests.head(soup.find(attrs={"data-quality": "240p"})['src'])
            #         keyb = [[InlineKeyboardButton("🎥 240p", callback_data='down240')]]
            #         buttons.extend(keyb)
            #         snd_msg.join(f'<b>📥   240p = {(int(res1.headers["content-length"])) / 1024 / 1024 :.2f} MB\n')
            #         # re_video_url2 = soup.find(attrs={"data-quality": "360p"})['src']
            # except Exception as e:
            #     print(e)
            # try:
            #     if soup.find(attrs={"data-quality": "360p"})['src'] is not None:
            #         # video_url2 = re_video_url2
            #         res2 = requests.head(soup.find(attrs={"data-quality": "360p"})['src'])
            #         keyb = [[InlineKeyboardButton("🎥 360p", callback_data='down360')]]
            #         buttons.extend(keyb)
            #         snd_msg.join(f'<b>📥   360p = {(int(res2.headers["content-length"])) / 1024 / 1024 :.2f} MB\n')
            # # re_video_url3 = soup.find(attrs={"data-quality": "480p"})['src']
            # except Exception as e:
            #     print(e)
            # try:
            #     if soup.find(attrs={"data-quality": "480p"})['src'] is not None:
            #         # video_url3 = re_video_url3
            #         res3 = requests.head(soup.find(attrs={"data-quality": "480p"})['src'])
            #         keyb = [[InlineKeyboardButton("🎥 480p", callback_data='down480')]]
            #         buttons.extend(keyb)
            #         snd_msg.join(f'<b>📥   480p = {(int(res3.headers["content-length"])) / 1024 / 1024 :.2f} MB\n')
            # # re_video_url = soup.find(attrs={"data-quality": "720p"})['src']
            # except Exception as e:
            #     print(e)
            # try:
            #     if soup.find(attrs={"data-quality": "720p"})['src'] is not None:
            #         # video_url = re_video_url
            #         res = requests.head(soup.find(attrs={"data-quality": "720p"})['src'])
            #         keyb = [[InlineKeyboardButton("🎥 720p", callback_data='down720')]]
            #         buttons.extend(keyb)
            #         snd_msg.join(f'<b>📥   720p = {(int(res.headers["content-length"])) / 1024 / 1024 :.2f} MB\n')
            # except Exception as e:
            #     print(e)
            # print("fda")
            res = requests.head(soup.find(attrs={"data-quality": "240p"})['src'])
            res1 = requests.head(soup.find(attrs={"data-quality": "360p"})['src'])
            res2 = requests.head(soup.find(attrs={"data-quality": "480p"})['src'])
            res3 = requests.head(soup.find(attrs={"data-quality": "720p"})['src'])
            update.message.reply_photo(video_url, reply_markup=InlineKeyboardMarkup(buttons),
                                       caption=f'🎥  <a href="{url}"> {soup.title.string}</a>\n\n'
                                       f'<b>📥   240p = {(int(res1.headers["content-length"])) / 1024 / 1024 :.2f} MB\n'
                                       f'📥   360p = {(int(res2.headers["content-length"])) / 1024 / 1024 :.2f} MB\n'
                                       f'📥   480p = {(int(res3.headers["content-length"])) / 1024 / 1024 :.2f} MB\n'
                                       f'📥   720p = {(int(res.headers["content-length"])) / 1024 / 1024 :.2f} MB\n\n'
                                       # caption=f'{snd_msg}'
                                               f'</b> '
                                               f'Link: {url}\n\n',
                                       parse_mode='HTML')
            # print(video_url)
            print(url)

            # adding last url
            Profile(
                external_id=chat_id,
                name=user.name,
                first_name=user.first_name,
                l_name=user.l_name,
                created_at=user.created_at,
                last_url=url
            ).save()
            update.message.delete(message_id)
        except Exception as e:
            print(e)
            update.message.reply_text('Video not found!!!')
            return

    def down240(self, update: Update, context: CallbackContext) -> None:
        chat_id = update.callback_query.message.chat_id
        user = Profile.objects.get(external_id=chat_id)
        url = user.get_last_url()

        query = update.callback_query
        query.answer()
        # show status
        print('start writing')

        # making soup and get link
        try:
            query.message.reply_text('Please wait ...')
            data = requests.get(url)
            soup = BeautifulSoup(data.text, 'html.parser')
            video_url = soup.find(attrs={"data-quality": "240p"})['src']
            r = requests.get(video_url, allow_redirects=True)
        except Exception as e:
            print(e)
            query.message.reply_text('Oops...Invalid url or the size of video above 50 MB')
            return

        # getting file name
        file_name = f'{soup.title.string}.mp4'
        disallowed_characters = "\'\"[]{}<>*?|/|"
        for character in disallowed_characters:
            file_name = file_name.replace(character, "")
        # file_name = file_name_orig.replace("\'", "")
        # writing to os
        with open(f"videos/{file_name}", 'wb') as f:
            f.write(r.content)

        # show status
        query.message.reply_text('Finished ✅')
        print('writing has been ended')

        # save url to db
        Message_url(profile=chat_id, file_name=file_name, text=url, created_at=datetime.datetime.now()).save()

        # send final result
        query.message.reply_video(video=open(f"videos/{file_name}", 'rb'))
        # update.message.reply_document(document=open(f"../../../videos/{file_name}", 'rb'))

    def down360(self, update: Update, context: CallbackContext) -> None:
        chat_id = update.callback_query.message.chat_id
        user = Profile.objects.get(external_id=chat_id)
        url = user.get_last_url()

        query = update.callback_query
        query.answer()
        # show status
        print('start writing')

        # making soup and get link
        try:
            query.message.reply_text('Please wait ...')
            data = requests.get(url)
            soup = BeautifulSoup(data.text, 'html.parser')
            video_url = soup.find(attrs={"data-quality": "360p"})['src']
            r = requests.get(video_url, allow_redirects=True)
        except Exception as e:
            print(e)
            query.message.reply_text('Oops...Invalid url or the size of video above 50 MB')
            return

        # getting file name
        file_name = f'{soup.title.string}.mp4'
        disallowed_characters = "\'\"[]{}<>*?|/|"
        for character in disallowed_characters:
            file_name = file_name.replace(character, "")
        # file_name = file_name_orig.replace("\'", "")
        # writing to os
        with open(f"videos/{file_name}", 'wb') as f:
            f.write(r.content)

        # show status
        query.message.reply_text('Finished ✅')
        print('writing has been ended')

        # save url to db
        Message_url(profile=chat_id, file_name=file_name, text=url, created_at=datetime.datetime.now()).save()

        # send final result
        query.message.reply_video(video=open(f"videos/{file_name}", 'rb'))
        # update.message.reply_document(document=open(f"../../../videos/{file_name}", 'rb'))

    def down480(self, update: Update, context: CallbackContext) -> None:
        chat_id = update.callback_query.message.chat_id
        user = Profile.objects.get(external_id=chat_id)
        url = user.get_last_url()

        query = update.callback_query
        query.answer()
        # show status
        print('start writing')

        # making soup and get link
        try:
            query.message.reply_text('Please wait ...')
            data = requests.get(url)
            soup = BeautifulSoup(data.text, 'html.parser')
            video_url = soup.find(attrs={"data-quality": "480p"})['src']
            r = requests.get(video_url, allow_redirects=True)
        except Exception as e:
            print(e)
            query.message.reply_text('Oops...Invalid url or the size of video above 50 MB')
            return

        # getting file name
        file_name = f'{soup.title.string}.mp4'
        disallowed_characters = "\'\"[]{}<>*?|/|"
        for character in disallowed_characters:
            file_name = file_name.replace(character, "")
        # file_name = file_name_orig.replace("\'", "")
        # writing to os
        with open(f"videos/{file_name}", 'wb') as f:
            f.write(r.content)

        # show status
        query.message.reply_text('Finished ✅')
        print('writing has been ended')

        # save url to db
        Message_url(profile=chat_id, file_name=file_name, text=url, created_at=datetime.datetime.now()).save()

        # send final result
        query.message.reply_video(video=open(f"videos/{file_name}", 'rb'))
        # update.message.reply_document(document=open(f"../../../videos/{file_name}", 'rb'))

    def down720(self, update: Update, context: CallbackContext) -> None:
        chat_id = update.callback_query.message.chat_id
        user = Profile.objects.get(external_id=chat_id)
        url = user.get_last_url()

        query = update.callback_query
        query.answer()
        # show status
        print('start writing')

        # making soup and get link
        try:
            query.message.reply_text('Please wait ...')
            data = requests.get(url)
            soup = BeautifulSoup(data.text, 'html.parser')
            video_url = soup.find(attrs={"data-quality": "720p"})['src']
            r = requests.get(video_url, allow_redirects=True)
        except Exception as e:
            print(e)
            query.message.reply_text('Oops...Invalid url or the size of video above 50 MB')
            return

        # getting file name
        file_name = f'{soup.title.string}.mp4'
        disallowed_characters = "\'\"[]{}<>*?|/|"
        for character in disallowed_characters:
            file_name = file_name.replace(character, "")
        # file_name = file_name_orig.replace("\'", "")
        # writing to os
        with open(f"videos/{file_name}", 'wb') as f:
            f.write(r.content)

        # show status
        query.message.reply_text('Finished ✅')
        print('writing has been ended')

        # save url to db
        Message_url(profile=chat_id, file_name=file_name, text=url, created_at=datetime.datetime.now()).save()

        # send final result
        query.message.reply_video(video=open(f"videos/{file_name}", 'rb'))
        # update.message.reply_document(document=open(f"../../../videos/{file_name}", 'rb'))
    # Converting to audio
    def convert_audio(self, update: Update, context: CallbackContext) -> None:
        chat_id = update.message.chat_id
        url = update.message.text

        clip = mp.VideoFileClip()

    def handle(self, *args, **kwargs):
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
        dispatcher = updater.dispatcher

        dispatcher.add_handler(CommandHandler('start', self.start))
        dispatcher.add_handler(MessageHandler(Filters.all & Filters.text, self.do_echo))
        dispatcher.add_handler(CallbackQueryHandler(self.down240, pattern="^(down240)$"))
        dispatcher.add_handler(CallbackQueryHandler(self.down360, pattern="^(down360)$"))
        dispatcher.add_handler(CallbackQueryHandler(self.down480, pattern="^(down480)$"))
        dispatcher.add_handler(CallbackQueryHandler(self.down720, pattern="^(down720)$"))

        # updater.dispatcher.add_handler(CallbackQueryHandler(button))
        # updater.dispatcher.add_handler(MessageHandler(Filters.all & Filters.command, self.start))
        updater.start_polling()
        updater.idle()
