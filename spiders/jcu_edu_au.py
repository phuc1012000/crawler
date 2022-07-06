from gc import callbacks
import scrapy


class JcuEduAuSpider(scrapy.Spider):
    name = 'jcu.edu.au'
    
    start_urls = ['https://www.jcu.edu.au/graduate-research-school/available-projects/']

    def parse_project_info(self,response):
        return {
            "name": response.css("p::text")[7].get(),
            "description": response.css("p::text")[10].get(),
            "supervisor_name": response.css("p::text")[8].get(),
            "supervisor_email": "",
            "supervisor_url": "",
            "project_url": response.request.url,
            "closing_date": "",
            "keywords": response.css("p::text")[11].get()
        } 

    def parse_project_in_department(self, response):
        yield from response.follow_all(css='form>div>div>p>a', callback=self.parse_project_info)

    def parse(self, response):
        yield from response.follow_all(css='div.topkeywords>ul>li>a', callback=self.parse_project_in_department)
