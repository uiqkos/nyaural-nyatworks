import json
import re
from datetime import datetime

import vk

from ml.src.comment import Comment
from ml.src.parsers.parser import Parser
from config import config


def _extract_comment(json_comment) -> Comment:
    return Comment(
        text=str(json_comment['text']),
        author=json_comment['from_id'],
        date=datetime.fromtimestamp(int(json_comment['date'])).strftime('%Y-%m-%d'),
        comments=list(map(_extract_comment, json_comment['thread']['items'] if 'thread' in json_comment else []))
    )


class VKParser(Parser):
    def __init__(self):
        self.session = None
        self.api = None

    def setup(self, app_id=None, login=None, password=None, token=None):
        if app_id and login and password:
            self.session = vk.AuthSession(app_id=app_id, user_login=login, user_password=password)
        elif token:
            self.session = vk.Session(token)
        else:
            self.session = vk.Session()

        self.api = vk.API(self.session, v='5.131', lang='ru')  # todo api.v hyperparam

        return self

    def default_setup(self):
        return self.setup(**config['parsers']['vk'])

    def parse(self, url):
        owner_id, post_id = re.findall(r'wall(-.\d+)_(\d+)', url)[0]

        root = self.api.wall.getById(posts=[f'{owner_id}_{post_id}'])[0]

        comments = self.api.wall.getComments(
            owner_id=owner_id,
            post_id=post_id,
            need_likes=True,
            thread_items_count=10
        )

        # print(json.dumps(comments, sort_keys=True, indent=4))

        return _extract_comment({
            'text': root['text'],
            'from_id': root['from_id'],
            'date': root['date'],
            'thread': comments
        })


if __name__ == '__main__':
    VKParser().setup(
        token=''
    ).parse('https://vk.com/feed?w=wall-187455013_1162533')
