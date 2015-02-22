import urllib2
import base64
import json
import re

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
    goodset = set()
    badset = set()

    for i in range(10):
        title = json_dict['d']['results'][i]['Title'].encode('utf-8')
        descrip = json_dict['d']['results'][i]['Description'].encode('utf-8')
        print 'Result ' + str(i + 1)
        print title
        print descrip
        print json_dict['d']['results'][i]['Url'].encode('utf-8')
        wordset = set(re.split(r'[^\w]+', descrip)) | set(re.split(r'[^\w]+', title))
        wordset.remove('')
        relevance = raw_input('Relevant (Y/N): ')
        if relevance == 'Y':
            precision = precision + 1
            goodset = goodset | wordset
        else:
            badset = badset | wordset
    wordset = goodset - badset
    words = list(wordset)
    if (len(words) > 0):
        for j in words:
            s = s + '+' + j
    print 'Precision ='+ str(precision)
    print 'Query =' + s

        
          

