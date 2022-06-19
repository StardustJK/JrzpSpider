from copy import copy
import scrapy
import time

from jrzp.items import JrzpItem

PAGE_NUM=13
POS_KEYWORD='系统维护工程师'
POS_DOMAIN='测试运维'
class JrzpspiderSpider(scrapy.Spider):
    name = 'jrzpspider'
    allowed_domains = ['www.jrzp.com']
    base_url='https://www.jrzp.com/main/job/moreJob.aspx?jobs=19_45&px=0&page='

    start_urls = [base_url+"0"]
    degreelist=['不限','中专','大专','本科','硕士','博士','博士后','海外留学']
 
    def parse(self, response):
        job_list=response.xpath('/html/body/div[2]/div[1]/div[2]/div[4]/div[1]/ul/li')
        for job in job_list:
            item=JrzpItem()
            item['pos_name']=job.xpath('normalize-space(./a/div/div[1]/span[1]/text())').get()
            item['enterprise']=job.xpath('./div[1]/a/span/text()').get()
            
            item['city']=job.xpath('./a/div/div[2]/span[1]/text()').get()
            
            salary=job.xpath('./a/div/div[1]/span[2]/text()').get()
            if salary=='面议':
                item['salary_low_bound']=0
                item['salary_high_bound']=0
            else:
                salary=salary.split('-')
                item['salary_low_bound']=int(salary[0])/1000
                item['salary_high_bound']=int(salary[1][0:-1])/1000

            item['salary_fee_months']=12

            degree=job.xpath('./a/div/div[2]/span[3]/text()').get()
            exp=job.xpath('./a/div/div[2]/span[2]/text()').get()
            
            if degree not in self.degreelist:
                item['degree']='其他'
            else:
                item['degree']=degree

            if exp=='应届毕业生' or exp=='在校学生':
                item['exp']='应届生'
            elif exp=='1年以上' or exp=='2年以上':
                item['exp']='1-3年'
            elif exp=='3年以上' or exp=='4年以上':
                item['exp']='3-5年'
            elif exp=='5年以上' or exp=='8年以上':
                item['exp']='5-10年'
            else :
                item['exp']=exp


            item['pos_keyword']=POS_KEYWORD
            url=job.xpath('./a/@href').get()
            item['url']=url

            item['pos_domain']=POS_DOMAIN
            item['pos_source']='今日招聘'
            if url:
                print('正在爬取详情页',url)
                details_request=scrapy.Request(url=url,callback=self.details,meta={'item':item})
                yield details_request
            else:
                yield item

            next_url=self.get_next_url(response.url)
            if next_url!=None:
                yield scrapy.Request(next_url,callback=self.parse)
            
        pass

    def get_next_url(self,oldurl):

        l=oldurl.split('=')
        oldPage=l[-1]
        newPage=int(oldPage)+1
        if newPage>PAGE_NUM:
            return
        newURL=self.base_url+str(newPage)
        return str(newURL)

    def details(self,response):
        item=response.meta['item']
        body=response.xpath('/html/body/div[2]')
        item['location']=body.xpath('./div[2]/div/div[1]/div[3]/div[2]/span/text()').get()[3:]
        date_time_str=body.xpath('./div[1]/div/div[2]/div[1]/div[4]/span[1]/text()')[1].get()
        item['create_time']=date_time_str.replace('-','/')
        item['charge_pos']=body.xpath('normalize-space(./div[2]/div/div[2]/div[1]/div[2]/div/span/text())').get()
        item['person_in_charge']=body.xpath('normalize-space(./div[2]/div/div[2]/div[1]/div[2]/div/span/text())').get()

       
        enterprise_scale=body.xpath('normalize-space(./div[2]/div/div[2]/div[2]/ul/li[2]/span/text())').get()
        if enterprise_scale=='公司规模未知':
            item['enterprise_scale']='其他'
            item['scale_mapping']=0
        elif enterprise_scale=='1000人以上':
            item['enterprise_scale']='1000-2000人'
            item['scale_mapping']=5
        else:
            maxscale=int(enterprise_scale.split('-')[1][0:-1])
            if maxscale<=50:
                item['enterprise_scale']='1-49人'
                item['scale_mapping']=1
            elif maxscale<=100:
                item['enterprise_scale']='50-99人'
                item['scale_mapping']=2
            elif maxscale<=500:
                item['enterprise_scale']='100-499人'
                item['scale_mapping']=3
            elif maxscale<=1000:
                item['enterprise_scale']='500-999人'
                item['scale_mapping']=4
        
        item['pos_detail']=body.xpath('normalize-space(./div[2]/div/div[1]/div[1]/div[3]/text())').getall()
        
        


        return item