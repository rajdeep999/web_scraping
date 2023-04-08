import scrapy


class WorldometerSpider(scrapy.Spider):
    name = "worldometer"
    allowed_domains = ["www.worldometers.info"]
    start_urls = ["https://www.worldometers.info/world-population/population-by-country/"]

    def parse(self, response):
        countries = response.xpath(".//tr/td[2]")

        for country in countries:
            country_name = country.xpath(".//a/text()").get()
            link = country.xpath(".//a/@href").get()

            yield response.follow(link, callback=self.parse_population, meta={'country': country_name})

    def parse_population(self, response):
        country = response.meta.get('country')
        rows = response.xpath("(//table[contains(@class,'table')])[1]/tbody/tr")

        for row in rows:
            year = row.xpath('.//td[1]/text()').get()
            population = row.xpath('.//td[2]/strong/text()').get()

            yield {
                'country': country,
                'year': year,
                'population': population
            }
