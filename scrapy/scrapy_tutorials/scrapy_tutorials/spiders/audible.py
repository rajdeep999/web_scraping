import scrapy


class AudibleSpider(scrapy.Spider):
    name = "audible"
    allowed_domains = ["www.audible.in"]
    start_urls = ["https://www.audible.in/search"]

    def parse(self, response):
        books = response.xpath(".//li[contains(@class,'productListItem')]")

        for book in books:
            book_name = book.xpath(".//h3[contains(@class,'bc-heading')]/a/text()").get()
            author_name = book.xpath(".//li[contains(@class,'authorLabel')]/span/a/text()").getall()
            narrator_name = book.xpath(".//li[contains(@class,'narratorLabel')]/span/a/text()").getall()

            yield {
                'book_name': book_name,
                'author_name': author_name,
                'narrator_name': narrator_name
            }

        pagination = response.xpath(".//ul[contains(@class,'pagingElements')]")
        next_page = pagination.xpath("//li/span[contains(@class,'nextButton')]/a")

        if next_page:
            link = next_page.xpath(".//@href").get()
            yield response.follow(url=link, callback=self.parse)
