from telegram.ext import Updater
from django.core.management.base import BaseCommand


class BotBase(BaseCommand):
    def __init__(self, *args, **kwargs):
        super(BotBase, self).__init__(*args, **kwargs)

        self.updater = Updater("1923758971:AAFd2D0aKwtEb1yWCIqk-rsXzD1hav7GTSs")