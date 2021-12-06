from markdown import markdown as markdown_to_html
from markdown_builder import Markdown


class Report:
    def __init__(self,
                 name: str,
                 description: str,
                 scores: dict,
                 ):
        self.report = (
            Markdown()
                .h1(name)
                .quote(description)
                .lst(list(map(': '.join, scores.items())))
                .render()
        )

    @property
    def html(self):
        return markdown_to_html(self.report)
