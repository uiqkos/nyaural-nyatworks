from nya_scraping.scrapers import scrapers


class ScraperFactory:
    def __init__(self, parsers_config: dict):
        self.config = parsers_config

    def create(self, input_method, text, **create_kwargs):
        for scraper_type in scrapers:
            if input_method == 'auto' and scraper_type.can_parse(text) or scraper_type.input_method == input_method:
                return scraper_type(**{
                    **self.config[scraper_type.input_method],
                    **create_kwargs
                })
