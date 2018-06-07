# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy_splash import SplashRequest

from VerifyBuildList.items import VerifybuildlistItem

class CmverifySpider(scrapy.Spider):
    name = 'cmverify'
    allowed_domains = ['10.0.64.29']
    start_urls = [
        'http://10.0.64.29:8080/jenkins/view/Verify/job/gerrit_do_verify_sprdroid8.x/build?delay=0sec',
        'http://10.0.64.29:8080/jenkins/view/Verify/job/gerrit_do_verify_sprdroidn/build?delay=0sec',
        'http://10.0.64.29:8080/jenkins/view/Verify/job/gerrit_do_verify_sprdroid6.x/build?delay=0sec',
        'http://10.0.64.29:8080/jenkins/view/Verify/job/gerrit_do_verify_sprdroid5.x/build?delay=0sec',
        'http://10.0.64.29:8080/jenkins/view/Verify/job/gerrit_do_verify_sprdroid4.x/build?delay=0sec',
        'http://10.0.64.29:8080/jenkins/view/Verify/job/gerrit_do_verify_sprdroid4.x_for_tbox/build?delay=0sec',
        'http://10.0.64.29:8080/jenkins/view/Verify/job/gerrit_do_verify_sprdIoT/build?delay=0sec',
        'http://10.0.64.29:8080/jenkins/view/Verify/job/gerrit_do_verify_androidpdk/build?delay=0sec',
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, meta={"url":url},args={'wait': 0.5})

    def parse(self, response):
        branch = []
        projects = []
        branchs_projects = []
        hitems = response.xpath("/html/body/div[4]/div[2]/form/table/tbody[2]/tr[1]/td[3]/div/select/option")
        branchx = response.url.split('/')[-2]
        for hitem in hitems:
             branchs_projects.append(unicode.decode(hitem.xpath("text()").extract_first()) + "\n")
             branch_project = hitem.xpath("text()").extract_first().strip()
             if branch_project.endswith('pac'):
                 branch_project = branch_project[:-4]
             projects.append(branch_project)

        item = VerifybuildlistItem()
        item['branchx'] = branchx
        item['branch_project_l'] = ','.join(projects)
        return item