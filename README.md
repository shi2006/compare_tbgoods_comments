# compare_tbgoods_comments
使用方法：
  1.先用spider.py把你想要获取的淘宝商品评论获取下来
    默认商品id是：39457378637，你要替换掉。只能一个个的来，没有多线程
    如果因为错误程序自动关闭，要根据已经获取的页数，修改start_page的值，
    要不然就是在重复获取。
  2.在运行analyse_comments.py
    注意文件的读取路径，可根据实际情况修改
