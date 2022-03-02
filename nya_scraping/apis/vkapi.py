import re
from typing import List

import vk

from nya_scraping.apis.api import Api
from nya_scraping.comment import Comment


class VKApi(Api, vk.API):
    def __init__(self, app_id=None, login=None, password=None, token=None, api_v=None):
        if app_id and login and password:
            self.session = vk.AuthSession(app_id=app_id, user_login=login, user_password=password)
        elif token:
            self.session = vk.Session(token)
        else:
            self.session = vk.Session()

        super(VKApi, self).__init__(self.session, v=api_v, lang='ru')
