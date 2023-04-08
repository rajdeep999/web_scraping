import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class TranscriptSpider(CrawlSpider):
    name = "transcript"
    allowed_domains = ["subslikescript.com"]
    start_urls = ["https://subslikescript.com/movies_letter-A"]

    rules = (Rule(LinkExtractor(restrict_xpaths=("//ul[@class='scripts-list']/a")), callback="parse_item", follow=True),
             Rule(LinkExtractor(restrict_xpaths=("(//a[@rel='next'])[1]")))
             )

    def parse_item(self, response):
        article = response.xpath("//article[@class='main-article']")
        name = article.xpath("./h1/text()").get()
        plot = article.xpath("./p[@class='plot']/text()").get()
        script = article.xpath("./div[@class='full-script']/text()").getall()

        yield {
            'name': name,
            'plot': plot,
            'script': script
        }