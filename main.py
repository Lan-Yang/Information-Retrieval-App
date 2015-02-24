import urllib2
import base64
import json
import re
import math
import operator

alpha = 1
beta = 0.75
gamma = 0.15

s = raw_input('Please input word: ')
p = int(round(input('Please input value: ') * 10))
precision = 1

while (precision != 0 and precision < p):
    # initialize search url
    bingUrl = r'https://api.datamarket.azure.com/Bing/Search/Web?Query=%27' +  s + '%27&$top=10&$format=JSON'
    accountKey = 'Ib4wTA9BOGjrp2Nug7wqKJN3Sjw++0u84wcBY5oN8U0'
    accountKeyEnc = base64.b64encode(accountKey + ':' + accountKey)
    headers = {'Authorization': 'Basic ' + accountKeyEnc}
    
    # get response
    req = urllib2.Request(bingUrl, headers = headers)
    response = urllib2.urlopen(req)
    content = response.read()
    json_dict = json.loads(content)
    
    precision = 0
    
    relevant_files = [0] * 10
    tf = []
    wif = {}

    for i in range(10):
        title = json_dict['d']['results'][i]['Title'].encode('utf-8')
        descrip = json_dict['d']['results'][i]['Description'].encode('utf-8')
        url = json_dict['d']['results'][i]['Url'].encode('utf-8')
        
        print 'Result ' + str(i + 1)
        print title
        print descrip
        print url
        
        wordset = set(re.split(r'[^\w]+', descrip)) | set(re.split(r'[^\w]+', title))
        if '' in wordset:
            wordset.remove('')
        
        dict = {}
        count = 0

        for word in wordset:
            count += 1
            if word in dict:
                dict[word] += 1
            else:
                dict[word] = 1
        
        for word in dict:
            dict[word] = float(dict[word])/count
            if word not in wif:
                wif[word] = 1
            else:
                wif[word] += 1
            
        tf.append(dict)
        
        relevance = raw_input('Relevant (Y/N): ')
        if relevance == 'Y':
            relevant_files[i] = 1
            precision = precision + 1
        else:
            relevant_files[i] = 0
    
    for words in tf:
        for word in words:
            idf = math.log(float(10)/(wif[word]+1), 2)
            words[word] = words[word] * idf
    
    vector = {}
    for i in range(10):
        if relevant_files[i] == 1:
            coefficient = beta
        elif relevant_files[i] == 0:
            coefficient = -1 * gamma
        for word in tf[i]:
            if word not in vector:
                vector[word] = coefficient * tf[i][word]
            else:
                vector[word] += coefficient * tf[i][word]
       
    term1 = max(vector.iteritems(), key=operator.itemgetter(1))[0]
    vector.pop(term1, None)
    term2 = max(vector.iteritems(), key=operator.itemgetter(1))[0]
    
    s = s + '+' + term1 + '+' + term2
            
    print 'Precision = '+ str(precision)
    print 'Query = ' + s
