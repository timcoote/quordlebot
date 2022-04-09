import scrapy

class QuordleSpider (scrapy.Spider):
    name="quordle"

    def start_requests(self):
        print ("start requests")
        url = 'https://www.quordle.com/#/practice'
        yield scrapy.Request (url=url, callback=self.parse)

    def parse (self, response):
        print("in parse")
        kb = response.css ('div::aria-label'==Keyboard)
        print (f"keyboard {kb}")
       # response.body)
