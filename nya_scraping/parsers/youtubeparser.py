import json
import re
from datetime import datetime
from typing import Union, Tuple

import dateutil.parser
from googleapiclient import discovery
from munch import DefaultMunch

from nya_scraping.comment import Comment, Author
from nya_scraping.parsers import Parser

munch = DefaultMunch.fromDict


class YoutubeParser(Parser):
    def __init__(self, api_v: str, key: str):
        self.api_v = api_v
        self.key = key
        self.api = discovery.build('youtube', api_v, developerKey=key)

    def parse_comment(self, comment: dict, comments: list = None):
        comment = munch(comment).snippet
        return Comment(
            text=comment.textOriginal,
            author=Author(
                name=comment.authorDisplayName,
                photo=comment.authorProfileImageUrl
            ),
            date=dateutil.parser.isoparse(comment.publishedAt)
                .strftime('%Y-%m-%d'),
            comments=list(map(self.parse_comment, comments))
                if comments else []
        )

    def parse_thread(self, thread: dict) -> Comment:
        thread = munch(thread)
        if thread.kind == 'youtube#commentThread':
            replies = thread.replies
            thread = thread.snippet.topLevelComment

            if replies is not None:
                return self.parse_comment(thread, replies.comments)

        return self.parse_comment(thread)

    def parse(self, inputs, skip: int = 0, take: int = None) -> Union[Comment, Tuple[Comment, int]]:
        video_id = re.findall(r'v=([\w\-]+)', inputs)[0]

        request = self.api.videos().list(
            part="snippet",
            id=video_id
        )
        response = request.execute()
        response = munch(response)['items'][0].snippet

        root = Comment(
            text=response.title + '\n\n' + response.description,
            author=Author(
                name=response.channelTitle,
                photo=''  # todo
            ),
            date=dateutil.parser.isoparse(response.publishedAt)
                .strftime('%Y-%m-%d'),
        )

        page_token = ''
        count = 0

        while page_token is not None and (not take or count - skip < take):
            request = self.api.commentThreads().list(
                part="snippet,replies",
                maxResults=20,
                pageToken=page_token,
                videoId=video_id,
                order='relevance'
            )
            response = munch(request.execute())
            # print(json.dumps(response, indent=4, ensure_ascii=False))

            for thread in response['items']:
                comment = self.parse_thread(thread)

                start = max(0, min(len(comment.comments), skip - count))
                end = min(len(comment.comments), (skip + take - count) if take else len(comment.comments))

                comment.comments = comment.comments[start:end]

                count += len(comment)

                # if len(comment.comments) > 0:
                root.comments.append(comment)

            # page_token = None
            page_token = response.nextPageToken

        return root
