import os
import sys
import urllib.request

conn = None
client_id = 'xLNuUi5YIoKlaW3aytaj'
client_secret = 'HjY8OAmwmM'

#네이버 OpenAPI 접속 정보 information
server = 'openapi.naver.com'

def userURLBuilder(url,**user):
    str = url + '?'
    for key in user.keys():
        str += key + '=' + user[key] + '&'
    return str

def connectOPpenApiServer():
    global conn,server
    conn = HTTPSConnection(server)
    conn.get_debuglevel()

searchkwrd = '한성대입구'


encText = urllib.parse.quote(searchkwrd)
url = 'https://openapi.naver.com/v1/search/local.xml?query=' + encText
request = urllib.request.Request(url)
request.add_header('X-Naver-Client-Id', client_id)
request.add_header('X-Naver-Client-Secret',client_secret)
response = urllib.request.urlopen(request)
rescode = response.getcode()
if rescode == 200:
    response_body = response.read()
    print(response_body.decode('utf-8'))
else:
    print('Error Code:'+rescode)