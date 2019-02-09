import scrapy
from scrapy.crawler import CrawlerProcess
import time
from myio import MyIO
from queue import Queue
import copy
from mythread import myThread

class W3Spider(scrapy.Spider):
    name = "w3"

    def start_requests(self):
        """打开本地文件，写入文件"""
        self.file = 0
        self.mydic = {}
        self.store = MyIO('store.xls')
       
        #创建线程的读写队列
        self.queue = Queue()
        
        #创建IO线程
        thread_io = myThread("thread_io", self.queue, self.store)
        thread_io.start()

        return [scrapy.Request('https://login.huawei.com/login/', callback=self.login)]

    def login(self, response):
        print('Preparing login')
        # FormRequeset.from_response是Scrapy提供的一个函数, 用于post表单
        # 登陆成功后, 会调用after_login回调函数
        return [scrapy.FormRequest(url="https://login.huawei.com/login/login.do",
                                   formdata={
                                       'actionFlag': 'loginAuthenticate',
                                       'lang': 'zh-CN',
                                       'loginMethod': 'login',
                                       'loginPageType': 'mix',
                                       'uid': 'xxxx',
                                       'password': 'xxxx',
                                       'verifyCode': '2345'
                                   },
                                   callback=self.after_login
                                   )]

    def after_login(self, response):
        num = 1600000
        # num = 102300
        for i in range(1400000, num):
            yield scrapy.Request(
                'url'+str(i),
                callback=self.parse
            )
            if i%200 == 0 or i == num-1:
                if len(self.mydic) != 0:
                    data = copy.deepcopy(self.mydic)
                    self.queue.put(data)
                    # self.store.putData(self.mydic)
                    self.mydic.clear()
                print("Current index is ", i)
            # time.sleep(0.001)

    def parse(self, response):
        divs = response.xpath('//div[@class="write_info"]//p//text()')
        try:
            mylist = []
            key = 0
            for p in divs:
                str1 = p.extract()
                pair = str1.strip().split('：', -1)
                if len(pair) == 1 or pair[1] == "":
                    #如果名字为空，中断此次操作
                    if pair[0] == "Chinese Name":
                        key = 0
                        break
                    continue
                mylist.append(pair)
                if pair[0] == "Employee ID":
                    key = pair[1]
            
            #解析完成，生成一条记录
            if len(mylist) == 0:
                mylist.clear()
            else:
                self.mydic[key] = mylist
        except:
            with open(str(self.file)+".html", 'wb') as f:
                f.write(response.body)
            self.log('Saved file %s' % self.file+".html")
            self.file = self.file + 1
        else:
            print("Current process id is", key)
            
process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

process.crawl(W3Spider)
process.start()