import scrapy


class CarscraperSpider(scrapy.Spider):
    name = "carscraper"
    allowed_domains = ["www.olx.co.id"]

    def start_requests(self):
        base_url = "https://www.olx.co.id/mobil-bekas_c198?page={}"
        for page_number in range(51):
            url = base_url.format(page_number)
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        items = response.css('div._2v8Tq')

        for item in items:
            brand = item.css('._2Gr10::text').extract_first()

            desc = item.css('._21gnE::text').extract_first()
            split_desc = desc.split(' - ')
            year = split_desc[0] if len(split_desc) > 0 else 'None'
            km = split_desc[1] if len(split_desc) > 1 else 'None'

            price = item.css('._1zgtX::text').extract_first()

            yield {
                'brand': brand,
                'year': year,
                'kilometers': km,
                'price': price
            }