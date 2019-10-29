# *-* coding:utf-8 *-*
import requests
import time
import random

# 为什么引入下面两个东西呢？因为requests.get(url, verify=False)里面引入了verify参数，
# 就会出现InsecureRequestWarning: Unverified HTTPS request is being made告警
# 然后为了取消告警，就添加这两行代码
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# 来源 :
# https://blog.csdn.net/qq_40946921/article/details/99684483
# https://www.bilibili.com/video/av16701031


class TaoBao():
    url = "https://rate.tmall.com/list_detail_rate.htm"
    header = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Cache-Control": "max-age=0",
        "Connection": "close",
        "Upgrade-Insecure-Requests": "1",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        # 当出现rgv587_flag的时候，可以换为自己的cookie
        "cookie": "cna=eGXNFRhRSkkCAbfhJLKH8aWp; _m_h5_tk=7d827b7269161b2bec1e75221f12e13b_1565891528974; _m_h5_tk_enc=7a2b5c3133447a619a160b42f8bb9335; x=__ll%3D-1%26_ato%3D0; hng=CN%7Czh-CN%7CCNY%7C156; uc1=cookie14=UoTaHoqcxosmvA%3D%3D; uc3=nk2=1DsN4FjjwTp04g%3D%3D&lg2=UIHiLt3xD8xYTw%3D%3D&id2=UondHPobpDVKHQ%3D%3D&vt3=F8dBy3K1GcD57BN%2BveY%3D; t=8d194ab804c361a3bb214233ceb1815c; tracknick=%5Cu4F0F%5Cu6625%5Cu7EA22013; lid=%E4%BC%8F%E6%98%A5%E7%BA%A22013; uc4=nk4=0%401up5I07xsWKbOPxFt%2Bwto8Y%2BdFcW&id4=0%40UOE3EhLY%2FlTwLmADBuTc%2BcF%2B4cKo; lgc=%5Cu4F0F%5Cu6625%5Cu7EA22013; enc=JY20EEjZ0Q4Aw%2BRncd1lfanpSZcoRHGHdAZmqrLUca8sEI9ku3vIBCYdT4Lvd9KJMVpk%2F1TnijPlCpUrJ2ncRQ%3D%3D; _tb_token_=553316e3ee5b5; cookie2=17126dd7c1288f31dc73b09697777108; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; l=cBj2amlRqUrFkhhjBOfgZuI8as7O6CvWGsPzw4_GjICP9H5cIxnlWZeaTSLkCnGVL6Dyr3RhSKO4B8YZjPathZXRFJXn9MpO.; isg=BBMTUm-GSmBFQQYmiWpbMPIdtpf9YKfi0yhVD8U0EzPgRD_mR5uf2DzSfvSPZP-C",
        "referer": "https://detail.tmall.com/item.htm",
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4098.3 Safari/537.37",
    }

    params = {
        "itemId": "0",  # 商品id
        "sellerId": "749901026",  # 店铺id,不是必须带的参数，可以不用修改
        "currentPage": "1",  # 页码
        "order": "1",  # 排序方式:1:按时间降序  3：默认排序
        "callback": "0",
        "_ksTS": "0"
    }

    def __init__(self, id: str):
        # 设置商品id
        self.params["itemId"] = id
        # 设置请求头
        self.header["referer"] = "https://detail.tmall.com/item.htm?id=" + id

    def set_params(self, page_index):
        # 设置url参数

        self.params["currentPage"] = str(page_index)
        # 增加时间戳参数
        t = time.time() * 1000  # t = 1571627847336.7542
        t = str(t).split(".")  # t = ["1571627847336", "7542"]
        self.params["callback"] = "jsonp%s" % (int(t[1]) + 1)  # callback = "jsonp7543"
        self.params["_ksTS"] = "%s_%s" % (t[0], t[1])  # _ksTS = "1571627847336_7542"

    def get_page_data(self, page_index: int, start_flag=0):
        # 为什么要有start_flag参数呢？
        # 是因为只有在第一次开始获取评论的时候，是要根据返回的数据里面获取总的页数的，之后就不用再次获取了

        # 设置url参数
        self.set_params(page_index)

        response = requests.get(self.url, self.params, headers=self.header, timeout=5, verify=False)
        req = response.content.decode("utf-8")
        # 主动关闭链接，以免链接过多
        response.close()

        # req是像 jsonp数字(...) 的字符串。因此需要对req进行切片，只取括号内的数据
        req = req[req.find('{'):req.rfind('}') + 1]

        # 在返回的数据中出现"rgv587_flag"就表示出现错误了，那么就要换cookie
        err_flag = "rgv587_flag"
        if err_flag in req:
            print("获取商品id：%s的第%s页评论失败,下次请从当前页开始" % (self.params["itemId"], page_index))
            print("出错了，请尝试手动更换cookie，或者过段时间再重新获取")
            print(page_index, req)

            # 退出程序
            exit()

            # 如果不想退出也可以自己定义休眠一段时间后重新请求
            # time.sleep(600)
            # self.get_page_data(page_index)

        else:
            # 在当前运行目录下保存评论, 命名格式：商品id_页数.json
            with open(self.params["itemId"] + "_" + str(page_index) + ".json", "w", encoding="utf-8") as f:
                f.write(req)

            if start_flag:  # 如果是第一次开始获取数据，那么就返回评论总页数

                #  如果在req中有字符串：lastPage":98,"page
                #  req.find('lastPage')查找到的是l(L)的索引，
                #  加上10(lastPage":一共10个字符)就是9的索引，
                #  req.find('page')就是，找到"p"的索引，然后减去2("p)，也就是(,)的索引
                #  我们知道list[1:4]是只取list[1],list[2],list[3],是不包括list[4]的
                last_page = req[req.find('lastPage') + 10:req.find('page') - 2]
                return int(last_page)  # 返回评论总页数

    def set_order(self, way: int):

        # 设置排序方式
        self.params["order"] = way

    def get_all_data(self, start_page):

        # 获取评论总页数，并保存第start_page页。虽然评论可能有很多，但最多也就99页
        last_page = self.get_page_data(start_page, start_flag=1)

        print("当前已获取商品id：%s的第%s页评论，共有%s页" % (self.params["itemId"], start_page, last_page))
        time.sleep(10)

        # 循环获取下一页评论
        for i in range(start_page + 1, last_page + 1):
            try:
                self.get_page_data(i)
                print("当前已获取商品id：%s的第%s页评论，共有%s页" % (self.params["itemId"], i, last_page))

                # 要休眠30~60s
                time.sleep(random.randint(30, 60))
            except Exception as ret:
                print("出现错误: ", ret)
                print("""请选择尝试:
                1.手动更换cookie(一般更换cookie就可以了) 
                2.增加休眠时间。
                3.过段时间再重新获取。
                """)
                break


def main():
    taobao1 = TaoBao("39457378637")
    # taobao2 = TaoBao("42487922508")

    # 默认从第一页开始获取
    start_page = 1
    # 如果获取的过程中出错了，然后已经获取了一些评论，就不要从第一页重复获取。
    # 修改start_page的值
    taobao1.get_all_data(start_page)
    # taobao2.get_all_data(start_page)


if __name__ == '__main__':
    main()
