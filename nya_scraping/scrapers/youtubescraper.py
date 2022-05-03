import re
from datetime import datetime
from operator import attrgetter
from typing import List, Iterable

import dateutil.parser
from googleapiclient import discovery
from more_itertools import first
from munch import DefaultMunch, Munch

from nya_scraping.comment import Comment, Author, CommentOneDim
from nya_scraping.scrapers.scraper import Scraper
from nya_utils.datatools import supplier
from nya_utils.functools import identity

munch = DefaultMunch.fromDict


class YoutubeScraper(Scraper):
    input_method = 'youtube'
    _regex = r'(v=([\w\-]+))|(youtu.be/([\w\-]+))'

    def __init__(self, api_v: str, key: str):
        self.api_v = api_v
        self.key = key
        self.api = discovery.build('youtube', api_v, developerKey=key)

    @staticmethod
    def _parse_comment(comment: Munch, comments: int = 0):
        snippet = comment.snippet
        return Comment(
            text=snippet.textOriginal,
            author=Author(
                name=snippet.authorDisplayName,
                photo=snippet.authorProfileImageUrl
            ),
            id=comment.id,
            date=(
                (dateutil.parser.isoparse(snippet.publishedAt))
                if snippet.publishedAt
                else datetime.now()
            ).strftime('%Y-%m-%d'),
            comments=comments
        )

    @staticmethod
    def _parse_thread(thread: Munch) -> Iterable[Comment]:
        if thread.kind == 'youtube#commentThread':
            for reply in thread.replies.comments:
                yield CommentOneDim(YoutubeScraper._parse_comment(reply), 2)

    def get_post_from_url(self, url):
        _, m1, _, m2 = first(re.findall(self._regex, url))
        video_id = m2 or m1

        request = self.api.videos().list(
            part="snippet,statistics",
            id=video_id
        )

        post = self.get_post_from_json(request.execute())

        request = self.api.channels().list(
            part="snippet",
            id=post.snippet.channelId
        )

        post.snippet['photo'] = request.execute()['items'][0]['snippet']['thumbnails']['default']['url']
        return post

    @staticmethod
    def get_post_from_json(json_response):
        return munch(json_response['items'][0])

    def get_comments(self, url, path: List[str] = None, *args, **kwargs) -> Iterable[Comment]:
        post = self.get_post_from_url(url)

        root = Comment(
            text=post.snippet.title + '\n\n' + post.snippet.description,
            author=Author(
                name=post.snippet.channelTitle,
                photo=post.snippet.photo
            ),
            date=dateutil.parser.isoparse(post.snippet.publishedAt)
                .strftime('%Y-%m-%d'),
            id=post.id,
            comments=int(post.statistics['commentCount'])
        )

        if path:
            path.pop(0)
        else:
            yield CommentOneDim(root, 0)
            return

        page_token = ''

        method = self.api.commentThreads()
        kwargs = dict(
            part="snippet,replies",
            maxResults=100,
            videoId=post.id,
            order='relevance'
        )
        comment_getter = attrgetter('snippet.topLevelComment')
        comment_number_getter = attrgetter('snippet.totalReplyCount')
        level = 1

        while page_token is not None:
            request = method.list(**kwargs, pageToken=page_token)
            response = munch(request.execute())
            page_token = response.nextPageToken

            for item in response['items']:
                if not path:
                    yield CommentOneDim(YoutubeScraper._parse_comment(
                        munch(comment_getter(item)),
                        munch(comment_number_getter(item))
                    ), level)
                else:
                    if first(path) == item.id:
                        path.pop(0)

                        method = self.api.comments()
                        kwargs = dict(
                            part="snippet",
                            parentId=item.id
                        )

                        comment_getter = identity
                        comment_number_getter = supplier(0)
                        level += 1

                        page_token = ''

                        break

    @classmethod
    def can_parse(cls, url) -> bool:
        return ('youtube' in url or 'youtu.be' in url) and re.findall(cls._regex, url)
