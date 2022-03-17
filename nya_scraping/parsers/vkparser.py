import re
from datetime import datetime
from functools import partial
from operator import itemgetter
from typing import overload, Iterator, List

from nya_app.connectors.comments import CommentOneDim
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


def _extract_comment(json_comment, profiles) -> Comment:
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
        id=str(json_comment['id'])
    )


class VKParser(Parser):
    regex = r'wall(-?\d+)_(\d+)'

    def __init__(self, api: VKApi):
        self.api = api

    @classmethod
    def create(cls, *args, **kwargs):
        return cls(VKApi(*args, **kwargs))

    def parse_id(
        self,
        owner_id,
        post_id,
        post_type,
        expand_path: List[str] = None,
        *args, **kwargs
    ) -> Iterator[Comment]:
        expand_path = expand_path or []

        if post_type == 'reply':
            return _extract_comment()

        if post_type == 'post':
            post = self.api.wall.getById(
                posts=[f'{owner_id}_{post_id}'],
                extended=True
            )
            root = post['items'][0]

            root = _extract_comment(root, post['groups'])

            yield CommentOneDim(root, -len(expand_path))

        if not expand_path:
            return

        comments_response = self.api.wall.getComments(
            owner_id=owner_id,
            post_id=post_id,
            need_likes=True,
            extended=True,
            thread_items_count=10
        )

        for comment in self.expand(
            json_comments=comments_response['items'],
            profiles=comments_response['profiles'] + post['groups'],
            expand_path=expand_path[1:]
        ):
            yield comment

    def parse(
        self,
        url,
        expand_path: List[str] = None,
        *args, **kwargs
    ) -> Iterator[Comment]:
        owner_id, post_id = re.findall(self.regex, url)[0]
        return self.parse_id(owner_id, post_id, 'post', expand_path, *args, **kwargs)

    def expand(
        self,
        json_comments,
        expand_path: List[str] = None,
        profiles: list = None
    ):
        profiles = profiles or []

        for json_comment in json_comments:
            comment = _extract_comment(json_comment, profiles)
            comment = CommentOneDim(comment, -len(expand_path))

            if not expand_path:
                yield comment

            elif comment.id == expand_path[0]:
                yield comment

                if 'thread' not in json_comment:
                    return

                for comment in self.expand(
                    json_comment['thread']['items'],
                    expand_path[1:],
                    profiles,
                ):
                    yield comment

    @classmethod
    def can_parse(cls, url) -> bool:
        return 'vk.com' in url and re.findall(cls.regex, url)
