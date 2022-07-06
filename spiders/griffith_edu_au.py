import scrapy


class GriffithEduAuSpider(scrapy.Spider):
    name = 'griffith.edu.au'
    # allowed_domains = ['https://www.griffith.edu.au/']
    start_urls = ['https://www.griffith.edu.au/griffith-sciences/research/projects']


    def get_info(self, project):
        return {
            'name' : project.css('td.project>h3::text').get(),
            'description' : project.css('td.project>p::text').get(),
            'supervisor_name' : project.css('td.supervisor>p>a::text').get(),
            'supervisor_link' : project.css('td.supervisor>p>a::attr(href)').get(),
            'project_url': "",
            "closing_date": "",
            'profile_url': "",
        }

    def process_profess_link(self, response, **project):
        project['supervisor_email'] = response.json()['emailAddress']['address']
        return project

    def parse(self, response):
        projects = [self.get_info(project) for project in  response.css('tr.result')]
        for project in projects:
            supervisor_id = project['supervisor_link'].rsplit('/',1)[-1]
            profess_link = project['supervisor_link'].replace(supervisor_id,f'api/users/{supervisor_id}')
            yield scrapy.Request(profess_link,callback=self.process_profess_link,cb_kwargs=project)




        

