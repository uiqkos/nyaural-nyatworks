import re
from datetime import datetime
from functools import partial
from operator import itemgetter

from nya_scraping.apis.vkapi import VKApi
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
    regex = r'wall(-?\d+)_(\d+)'

    def __init__(self, api: VKApi):
        self.api = api

    @classmethod
    def create(cls, *args, **kwargs):
        return cls(VKApi(*args, **kwargs))

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
                )),
            id=json_comment['id']
        )

    def parse(self, url, skip: int = 0, take: int = None):
        return self.parse_id(*re.findall(self.regex, url)[0], skip, take)

    def parse_id(self, owner_id, post_id, skip: int = 0, take: int = None):
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

        # print(json.dumps(comments, sort_keys=True, indent=4, ensure_ascii=False))

        comment = self._extract_comment({
            'text': root['text'],
            'from_id': root['from_id'],
            'date': root['date'],
            'thread': comments,
            'id': root['id']
        }, profiles=comments['profiles'] + post['groups'])

        return comment

    @classmethod
    def can_parse(cls, url) -> bool:
        return 'vk.com' in url and re.findall(cls.regex, url)
