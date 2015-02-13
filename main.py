import urllib2
import base64
import json

s = raw_input('Please input word: ')
p = int(round(input('Please input value: ') * 10))
precision = 1
while (precision != 0 and precision < p):
    bingUrl = r'https://api.datamarket.azure.com/Bing/Search/Web?Query=%27' +  s + '%27&$top=10&$format=JSON'
    accountKey = 'Ib4wTA9BOGjrp2Nug7wqKJN3Sjw++0u84wcBY5oN8U0'
    accountKeyEnc = base64.b64encode(accountKey + ':' + accountKey)
    headers = {'Authorization': 'Basic ' + accountKeyEnc}
    req = urllib2.Request(bingUrl, headers = headers)
    response = urllib2.urlopen(req)
    content = response.read()
    json_dict = json.loads(content)
    precision = 0

    for i in range(10):
        print json_dict['d']['results'][i]['Title'].encode('utf-8')
        print json_dict['d']['results'][i]['Description'].encode('utf-8')
        print json_dict['d']['results'][i]['Url'].encode('utf-8')
        relevance = raw_input('Relevant? yes/no: ')
        if relevance == 'yes':
            precision = precision + 1   
    print precision
    print p
    print precision < p
        
          

