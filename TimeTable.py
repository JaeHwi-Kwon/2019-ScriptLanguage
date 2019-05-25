# -*- coding: utf-8 -*-

from urllib.request import urlopen,Request
from urllib.parse import quote_plus
from xml.etree import ElementTree



def GetTimeTable(ID, day, way):
    key = 'e20GlP6AHkpkkdAr0AYT50r6zfv%2Fgj8KNbomL7RzhiSCSxpFb0vhZgYU7DADHoto16Zxg7xK01%2BCd69yoAssag%3D%3D'
    url = 'http://openapi.tago.go.kr/openapi/service/SubwayInfoService/getSubwaySttnAcctoSchdulList'
    queryParams = '?' + 'ServiceKey=' + key + '&subwayStationId=' + quote_plus(ID)
    queryParams +='&dailyTypeCode=' + quote_plus(day)
    queryParams +='&upDownTypeCode=' + quote_plus(way)
    queryParams +='&pageNo=' + '1'
    queryParams +='&numOfRows=' + '300'

    req = Request(url + queryParams)
    req.get_method = lambda: 'GET'
    res_body = urlopen(req).read()
    print(res_body)
    dataTree = ElementTree.fromstring(res_body)

    table = []

    list = dataTree.getiterator('item')
    for item in list:
        time = item.findtext('depTime')
        table.append(time)

    return table


if __name__ == '__main__':
    GetTimeTable('SUB214', '01', 'U')