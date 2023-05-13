# 对B站视频的弹幕和评论进行分析和可视化

## 1.爬虫方面

### 1.1获取bilibili视频热度前50的页的数据

- https://api.bilibili.com/x/v2/reply?pn=+str(num)+&type=1&oid=cid&sort=2
### 1.2获取bilibili视频播放后一个星期的弹幕

- 获取接口数据步骤
  - https://api.bilibili.com/x/player/pagelist?bvid=‘+str(bvid)’+&jsonp=jsonp
  - https://api.bilibili.com/x/v1/dm/list.so?oid=+str(cid)

- 基于时间来查找弹幕数据需要处理seg.so格式的弹幕数据

  - seg.so格式的数据和原本的xml类型不同，它给位了protobuf
    - protobuf 官网的介绍，简单来讲就是一种传输的协议，比 xml 更小、更快、更简单
  - 需要添加cookie内容

  - 需要下载protoc解析器
    - Protoc 是用于将 .proto 文件编译成各种编程语言(如 Python、Golang 等)的编译器，是进行 Protobuf 解析的必要条件，可在下面的链接中下载
    - https://github.com/protocolbuffers/protobuf

  - 导入google.protobuf
    - https://github.com/protocolbuffers/protobuf

  - 主要通过设置的proto格式文件通过protoc解析器翻译成python代码，然后通过使用google.protobuf里的api来调用数据

## 2 .数据清洗

因为互联网中的信息流通和舆论导向变化很快。我们需要选择到获取的热评数据和弹幕数据是在同一时间段的

清洗逻辑：

- json数组中是有时间列的，删除没有存储到时间的热评数据
- 删除和弹幕时间不一致的热评数据

## 3. 可视化

- jieba
  - 使用jieba中文分词库中的精确模式可以使将句子最精确地切开，适合文本分析
- pyecharts
  - 统计词频出现最多的词
- wordcloud
  - 输出词云图

##  4.分析过程

- 1.时间对比：7.25-7.31的弹幕数量和8.7-8.13的弹幕数量
- 2.空间对比：7.25-7.31的弹幕数量和7.25-7.31清洗后的评论数据
- 具体可以看



