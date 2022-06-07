import re
from datetime import datetime
from operator import itemgetter
from typing import Iterator, List, Callable, Type

import vk
from munch import DefaultMunch, Munch

from nya_scraping.comment import Comment, Author, CommentOneDim, RawComment
from nya_scraping.scrapers.scraper import Scraper
from nya_utils.datatools import filter_dataclass_kwargs
from nya_utils.functools import get_item_or
from nya_utils.itertools import find

munch = DefaultMunch.fromDict

COMMENTS_COUNT = 100
THREAD_ITEMS_COUNT = 10


class VKScraper(Scraper):
    _regex = r'wall(-?\d+)_(\d+)'
    input_method = 'vk'

    def __init__(
        self,
        app_id=None,
        login=None,
        password=None,
        token=None,
        api_v=None,
        extra: bool = False
    ):
        if app_id and login and password:
            session = vk.AuthSession(app_id=app_id, user_login=login, user_password=password)
        elif token:
            session = vk.Session(token)
        else:
            session = vk.Session()

        self.api = vk.API(session, v=api_v)
        self.extra = extra

    @staticmethod
    def _convert_id_to_name(author, profiles):
        profile = find(profiles, abs(author), key=itemgetter('id'))

        if not profile:
            return author

        if author < 0:
            return profile['name']

        return profile['first_name'] + ' ' + profile['last_name']

    @staticmethod
    def _get_photo_by_id(author, profiles):
        profile = find(profiles, abs(author), key=itemgetter('id'))
        if not profile:
            return author
        return profile['photo_100']

    @staticmethod
    def _convert_appeals(text):
        return re.sub(r'\[(id|club)\w+\|(.*)]', r'\g<2>', text)

    def _extract_comment(self, json_comment, profiles) -> Comment:
        comments = get_item_or(
            json_comment, 'comments',
            default=get_item_or(
                json_comment, 'thread',
                default={'count': 0}
            )
        ).get('count')

        kwargs = dict(
            text=(json_comment['text'] and VKScraper._convert_appeals(str(json_comment['text']))) +
                 ('attachments' in json_comment) * '<вложение>',
            author=
            Author(
                name=VKScraper._convert_id_to_name(json_comment['from_id'], profiles),
                photo=VKScraper._get_photo_by_id(json_comment['from_id'], profiles)
            ),
            date=
            datetime.fromtimestamp(int(json_comment['date'])).strftime('%Y-%m-%d'),
            id=str(json_comment['id']),
            comments=comments
        )

        if self.extra:
            return RawComment(**{**json_comment, **kwargs})

        return Comment(**kwargs)

    @staticmethod
    def get_post_from_json(json_post) -> Munch:
        return munch(json_post)

    def get_post_from_url(self, url) -> Munch:
        owner_id, post_id = re.findall(self._regex, url)[0]

        json_post = self.api.wall.getById(
            posts=[f'{owner_id}_{post_id}'],
            extended=True
        )

        post = munch({**json_post['items'][0], 'groups': json_post['groups']})

        return post

    def get_comments(self, url, path: List[str] = None, *args, **kwargs) -> Iterator[Comment]:
        path = path or []
        post = self.get_post_from_url(url)

        return self.get_comments_from_post(post, path, *args, **kwargs)

    def get_comments_from_post(self, post, path: List[str] = None, *args, **kwargs):
        root = self._extract_comment(post, post.groups)

        if not path:
            yield CommentOneDim(root, 0)

        if post.post_type == 'reply':
            return

        if not path:
            return

        offset = 0

        while (
            comments_response := self.api.wall.getComments(
                owner_id=post.owner_id,
                post_id=post.id,
                need_likes=True,
                extended=True,
                count=COMMENTS_COUNT,
                offset=offset,
                thread_items_count=THREAD_ITEMS_COUNT
            )
        )['items']:

            offset += COMMENTS_COUNT

            for comment in self.expand(
                json_comments=comments_response['items'],
                profiles=comments_response['profiles'] + post.groups,
                level=1,
                expand_path=path[1:]
            ):
                yield comment

    def expand(
        self,
        json_comments,
        expand_path: List[str] = None,
        level: int = 0,
        profiles: list = None
    ):
        profiles = profiles or []

        for json_comment in json_comments:
            comment = self._extract_comment(json_comment, profiles)
            comment = CommentOneDim(comment, level)

            if not expand_path:
                yield comment

            elif comment.id == expand_path[0]:

                if 'thread' not in json_comment:
                    return

                for comment in self.expand(
                    json_comment['thread']['items'],
                    expand_path[1:],
                    level + 1,
                    profiles,
                ):
                    yield comment

                return

    @classmethod
    def can_parse(cls, url) -> bool:
        return 'vk.com' in url and re.findall(cls._regex, url)
