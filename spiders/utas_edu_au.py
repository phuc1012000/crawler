import scrapy


class UtasEduSpider(scrapy.Spider):
    name = 'utas-edu'

    start_urls = ['https://www.utas.edu.au/research/degrees/available-projects']


    def parse_project(self, response):
        description = ''

        description_start = response.css('#content-start > h2:nth-child(2)')

        element = description_start.xpath('following-sibling::*[1]')[0]

        while element.root.tag != 'h3':
            element_text = element.xpath('text()').get() 

            if element_text :
                description += element_text + '\n'

            element = element.xpath('following-sibling::*[1]')[0]

        return {
            'name': response.css('h1.internal-banner__content--title').xpath('text()').get().strip(),
            'description' : description,
            'supervisor_name': response.xpath('//a[contains(@href,"mailto")]')[-1].xpath('text()').get(),
            'supervisor_email': response.xpath('//a[contains(@href,"mailto")]')[-1].xpath('@href').get().split('mailto:')[1],
            'project_url' : response.request.url,
            'closing_date': response.css('div.infographic-stripe--wrapper:nth-child(1) > div:nth-child(2) > p:nth-child(3)::text').get().strip()
        }

    def parse(self, response):
        yield from response.follow_all(css='a.search-result__card--link', callback=self.parse_project)
