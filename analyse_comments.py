import re
import json
import time


def analyse_comments(item: str):
    # 统计有关键字的评论数量
    count = 0
    for x in range(1, 100):
        # 打开获取到的评论
        with open("./" + item + "_" + str(x) + ".json", "r", encoding="utf-8") as f:
            # 把评论json文件加载为字典，然后通过键值获取评论
            comment_dick = json.load(f)

            for comments in comment_dick['rateDetail']['rateList']:
                if comments['appendComment']:  # 如果有追加评论，就拼接到评论里面
                    comment = comments['rateContent'] + comments['appendComment']['content']
                comment = comments['rateContent']

                # 用正则表达式，判断评论中是否有“男朋友,老公”等词语
                ret = re.search(r"男朋友|男票|男友|老公", comment)
                if ret:  # 匹配中count就加1
                    # print(ret.group())
                    # print(comment)
                    count += 1
    return count


def main():
    goods_id1 = "39457378637"
    goods_id2 = "42487922508"

    count1 = analyse_comments(goods_id1)
    count2 = analyse_comments(goods_id2)
    # print(count1,count2)
    print("在商品https://detail.tmall.com/item.htm?id=%s\n的评论中包含关键字男朋友，老公的评论有%s条\n" % (goods_id1, count1))
    print("在商品https://detail.tmall.com/item.htm?id=%s\n的评论中包含关键字男朋友，老公的评论有%s条" % (goods_id2, count2))
    print("=" * 70)
    if count1 > count2:
        print("因此，在女生眼中商品https://detail.tmall.com/item.htm?id=%s比较好" % goods_id1)
    elif count1 == count2:
        print("因此，在女生眼中这两个商品没什么区别")
    else:
        print("因此，在女生眼中商品https://detail.tmall.com/item.htm?id=%s比较好" % goods_id2)
    time.sleep(10)


if __name__ == '__main__':
    main()
