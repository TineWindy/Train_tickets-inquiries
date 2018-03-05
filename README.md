# Train_tickets-inquiries
A python project to inquiry train tickets
一个python小程序用于查询火车票

使用requests、json、pickle、prettytable等库完成

程序代码可直接运行

## 第一次更新：
查询火车票软件思路解析：
- 第一步是要解析查询车票的URL：
1.  打开12306进入火车票查询界面，随便查询一下（例如武汉到成都，2018-03-10，成人票），进入查询界面后提取URL：https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=2018-03-10&leftTicketDTO.from_station=WHN&leftTicketDTO.to_station=BJN&purpose_codes=ADULT 。

2.  打开Chrome的开发者模式，通过查看浏览器接收的文件我们可以发现查询车票的12306网页使用的是get请求，也就意味着我们输入的车站时间等信息都保存在URL当中。因此我们仔细阅读URL发现几个关键词：train_date、from_station、to_station和purpose_codes。

3.  以上四个关键词的意思从其名字就很容易看出来了。再对比我们输入的信息很容易得到的就是date与purpose_code
s这两个参数对应的输入格式即日期就是标准格式，codes视成人和学生票而定；而两个station参数应该是车站名对应的英文简写，然而与我们习惯的首字母缩写并不同，因此我们需要找到车站名与英文字母对应的关系。

4.  这里需要注意的是，网页采用的是get请求方式，因此将我们输入的站名转换为英文字母的js文件应该在本地。经过查看找到了站名与英文字母转换的表，将其保存到本地以供使用，命名为station_name.data。这一步详细过程请看readme文件的末尾补充。

5.  这样我们就获悉了查询URL的构成，我们随便更改一下四个参数，发现按照我们发现的格式使用能得到正确的数据，证明了我们解析正确。进入下一步。
