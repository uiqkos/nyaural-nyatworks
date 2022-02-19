import re
from datetime import datetime
from functools import partial
from operator import itemgetter

import vk

from nya_scraping.comment import Comment, Author
from nya_scraping.parsers.parser import Parser
from nya_utils.itertools import find


def _convert_id_to_name(author, profiles):
    profile = find(profiles, abs(author), key=itemgetter('id'))

    if not profile:
        return author

    if author < 0:
        return profile['name']

    return profile['first_name'] + ' ' + profile['last_name']


def _get_photo_by_id(author, profiles):
    profile = find(profiles, abs(author), key=itemgetter('id'))
    if not profile:
        return author
    return profile['photo_100']


def _convert_appeals(text):
    return re.sub(r'\[(id|club)\w+\|(.*)]', r'\g<2>', text)


class VKParser(Parser):
    def __init__(self):
        self.session = None
        self.api = None

    def setup(self, app_id=None, login=None, password=None, token=None, api_v=None):
        if app_id and login and password:
            self.session = vk.AuthSession(app_id=app_id, user_login=login, user_password=password)
        elif token:
            self.session = vk.Session(token)
        else:
            self.session = vk.Session()

        self.api = vk.API(self.session, v=api_v, lang='ru')

        return self

    def _extract_comment(self, json_comment, profiles) -> Comment:
        return Comment(
            text=
                _convert_appeals(str(json_comment['text'])),
            author=
                Author(
                    name=_convert_id_to_name(json_comment['from_id'], profiles),
                    photo=_get_photo_by_id(json_comment['from_id'], profiles)
                ),
            date=
                datetime.fromtimestamp(int(json_comment['date'])).strftime('%Y-%m-%d'),
            comments=
                list(map(
                    partial(self._extract_comment, profiles=profiles),
                    json_comment['thread']['items'] if 'thread' in json_comment
                    else []
                ))
        )

    def parse(self, url):
        owner_id, post_id = re.findall(r'wall(-?\d+)_(\d+)', url)[0]

        post = self.api.wall.getById(
            posts=[f'{owner_id}_{post_id}'],
            extended=True
        )

        root = post['items'][0]

        comments = self.api.wall.getComments(
            owner_id=owner_id,
            post_id=post_id,
            need_likes=True,
            extended=True,
            thread_items_count=10
        )

        # print(json.dumps(comments, sort_keys=True, indent=4))

        return self._extract_comment({
            'text': root['text'],
            'from_id': root['from_id'],
            'date': root['date'],
            'thread': comments
        }, profiles=comments['profiles'] + post['groups'])

