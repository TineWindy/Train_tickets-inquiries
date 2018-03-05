import requests
import json
import pickle
from prettytable import PrettyTable

def trans(uchar):
    '''
    判断输入的出发地、目的地是否有效
    :param uchar: string
    :return: string
    '''

    #读取已保存的站点英文缩写
    station_name = dict()
    with open('station_name.data', 'rb') as f:
        station_name = pickle.load(f)

    while 1:
        if uchar in station_name:
            return station_name[uchar]
        else:
            uchar = input('输入错误 请重新输入\n')

def get_purpose():
    '''
    获取ticket相关信息
    :return: a tuple consisted by info about ticket
    '''

    fromStation = input('输入 出发地\n')
    fromStation = trans(fromStation)
    toStation = input('输入 目的地\n')
    toStation = trans(toStation)
    while 1:
        purpose_code = input('成人 或 学生\n')
        if purpose_code=='成人':
            purpose_code = 'ADULT'
            break
        elif purpose_code=='学生':
            purpose_code = 'student'
            break
    date = input('出发日期（格式如下：1999-05-01）\n')
    return date,fromStation,toStation,purpose_code



def get_query_url():
    '''构建查询访问url'''

    #获取ticket info
    date,fromStation,toStation,purpose_code = get_purpose()
    #构建查询url
    url = 'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=' + date + '&leftTicketDTO.from_station=' + fromStation + '&leftTicketDTO.to_station=' + toStation + '&purpose_codes=' + purpose_code
    return url

def get_data():
    '''获取url中查询data'''

    #获取查询对应url
    url = get_query_url()
    #url = 'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=2018-03-08&leftTicketDTO.from_station=WHN&leftTicketDTO.to_station=BJP&purpose_codes=ADULT'
    #模拟浏览器登入
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'}
    response = requests.get(url,headers=headers)
    response.encoding = 'UTF-8'
    text = response.text
    #解析获取的信息
    data = json.loads(text)['data']['result']
    return data

def print_ticket(tickets_list):
    '''

    :param ticket_data: a list of all ticket_data_dicts
    :return:
    '''

    table = PrettyTable(['车次','出发地','目的地','出发时间','到达时间','历时','商务座','一等座','二等座','动卧','高级软卧','软卧','硬卧','软座','硬座','无座','其他','预订'])
    for ticket in tickets_list:
        ticket_info = []
        for i in ticket:
            ticket_info.append(ticket[i])
        table.add_row(ticket_info)
    print(table)

def get_data_list(items):
    '''
    #解析获取的信息并选择后存储
    :param items: string of result
    :return:  dict of special info
    '''

    #建立dict存储所需信息
    ticket_data ={
        "station_train_code": '',
        "from_station_name": '',
        "to_station_name": '',
        'start_time': '',
        'arrive_time': '',
        "time": '',
        "swz_num": '',
        "yd_num": '',
        "ed_num": '',
        "dw_num": '',
        "gr_num": '',
        "rw_num": '',
        "yw_num": '',
        "rz_num": '',
        "yz_num": '',
        "wz_num": '',
        "qt_num": '',
        "note_num": ''
    }
    name = {
        "station_train_code": '',
        "from_station_name": '',
        "to_station_name": '',
        'start_time': '',
        'arrive_time': '',
        "time": '',
        "swz_num": '',
        "yd_num": '',
        "ed_num": '',
        "dw_num": '',
        "gr_num": '',
        "rw_num": '',
        "yw_num": '',
        "rz_num": '',
        "yz_num": '',
        "wz_num": '',
        "qt_num": '',
        "note_num": ''
    }

    #分隔items，解码得所需信息
    item = items.split('|')  # 用"|"进行分割
    ticket_data['station_train_code'] = item[3]  # 车次在3号位置
    ticket_data['from_station_name'] = item[6]  # 始发站信息在6号位置
    ticket_data['to_station_name'] = item[7]  # 终点站信息在7号位置
    ticket_data['start_time'] = item[8]  # 出发时间信息在8号位置
    ticket_data['arrive_time'] = item[9]  # 抵达时间在9号位置
    ticket_data['time'] = item[10]  # 经历时间在10号位置
    ticket_data['swz_num'] = item[32] or item[25]  # 特别注意：商务座在32或25位置
    ticket_data['yd_num'] = item[31]  # 一等座信息在31号位置
    ticket_data['ed_num'] = item[30]  # 二等座信息在30号位置
    ticket_data['gr_num'] = item[21]  # 高级软卧信息在31号位置
    ticket_data['rw_num'] = item[23]  # 软卧信息在23号位置
    ticket_data['dw_num'] = item[27]  # 动卧信息在27号位置
    ticket_data['yw_num'] = item[28]  # 硬卧信息在28号位置
    ticket_data['rz_num'] = item[24]  # 软座信息在24号位置
    ticket_data['yz_num'] = item[29]  # 硬座信息在29号位置
    ticket_data['wz_num'] = item[26]  # 无座信息在26号位置
    ticket_data['qt_num'] = item[22]  # 其他信息在22号位置
    ticket_data['note_num'] = item[1]  # 备注在1号位置

    #若无某类信息，则将其键值置为'-'
    for pos in name:
        if ticket_data[pos] == '':
            ticket_data[pos] = '-'

    #输出信息
    #for i in ticket_data:
        #print(ticket_data[i],end='   ')
    #print()
    #print_ticket(ticket_data)
    return ticket_data

def resolve_data():
    data = get_data()
    sum = len(data)
    tickets_list = []
    for i in range(sum):
        tickets_list.append(get_data_list(data[i]))
    print_ticket(tickets_list)

if __name__=='__main__':
    resolve_data()
