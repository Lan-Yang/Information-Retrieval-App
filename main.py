import urllib2
import base64
import json

s = raw_input('Please input word: ')
p = input('Please input value: ')
bingUrl = r'https://api.datamarket.azure.com/Bing/Search/Web?Query=%27' +  s + '%27&$top=10&$format=JSON'
#Provide your account key here
accountKey = 'Ib4wTA9BOGjrp2Nug7wqKJN3Sjw++0u84wcBY5oN8U0'

accountKeyEnc = base64.b64encode(accountKey + ':' + accountKey)
headers = {'Authorization': 'Basic ' + accountKeyEnc}
req = urllib2.Request(bingUrl, headers = headers)
response = urllib2.urlopen(req)
content = response.read()
#root = ET.fromstring(content)
#content contains the xml/json response from Bing.
json_dict = json.loads(content)

for i in range(10):
    print json_dict['d']['results'][i]['Title'].encode('utf-8')
    print json_dict['d']['results'][i]['Description'].encode('utf-8')
    print json_dict['d']['results'][i]['Url'].encode('utf-8')
# print root.tag
# print root.attrib
# print root[6][2].text
# for child in root:
#     print child.tag, child.attrib
