import urllib2
import base64
import json
import re
import math
import operator
import sys


# define the parameters in Rocchio algorithm
alpha = 1
beta = 0.75
gamma = 0.15

# read the files for stopwords
infile = open("stopwords.txt", "r")
stopwords = [line.strip() for line in infile]
infile.close()

accountKey = sys.argv[1]
pstr = sys.argv[2]
s = sys.argv[3]
p = int(round(float(pstr) * 10))
precision = 1

slist = s.split()
s = "+".join(slist)

# store all the words already in the query
augmented = []
augmented.append(s)

while (precision != 0 and precision < p):
    # initialize search url
    bingUrl = r'https://api.datamarket.azure.com/Bing/Search/Web?Query=%27' +  s + '%27&$top=10&$format=JSON'
    # accountKey = 'Ib4wTA9BOGjrp2Nug7wqKJN3Sjw++0u84wcBY5oN8U0'
    accountKeyEnc = base64.b64encode(accountKey + ':' + accountKey)
    headers = {'Authorization': 'Basic ' + accountKeyEnc}
    
    # get response
    req = urllib2.Request(bingUrl, headers = headers)
    response = urllib2.urlopen(req)
    content = response.read()
    json_dict = json.loads(content)
    
    precision = 0
    
    # print parameters
    print 'Parameters:'
    print "Client Key = {0:20}".format(accountKey)
    print "Query = {0:20}".format(s)
    print "Precision = {0:20}".format(pstr)
    print "URL: " + bingUrl
    print "Total no of results: 10"
    print "Bing Search Results:"
    print "======================="

    relevant_files = [0] * 10
    tf = []

    for i in range(10):
        title = json_dict['d']['results'][i]['Title'].encode('utf-8')
        descrip = json_dict['d']['results'][i]['Description'].encode('utf-8')
        url = json_dict['d']['results'][i]['Url'].encode('utf-8')

        print 'Result ' + str(i + 1)
        print '['
        print "URL: " + url
        print "Title: " + title
        print "Summary: " + descrip
        print ']'
        
        wordset = set(re.split(r'[^\w]+', descrip)) | set(re.split(r'[^\w]+', title))
        if '' in wordset:
            wordset.remove('')
        
        dic = {}
        count = 0

        # calculate tf
        for word in wordset:
            count += 1
            if word in dic:
                dic[word] += 1
            else:
                dic[word] = 1
        
        for word in dic:
            dic[word] = float(dic[word])/count
            
        tf.append(dic)
        
        # calculate precision according to feedback
        relevance = raw_input('Relevant (Y/N): ')
        if relevance == 'Y':
            relevant_files[i] = 1
            precision = precision + 1
        else:
            relevant_files[i] = 0

    # print feedback
    print "======================="
    print "FEEDBACK SUMMARY"
    print "Query " + s
    print "Precision " ,float(precision)/10
    if (precision < p):
        print "Still below the desired precision of %s" %(pstr)

        # Rocchio algorithm
        vector = {}
        for i in range(10):
            if relevant_files[i] == 1:
                coefficient = beta
            elif relevant_files[i] == 0:
                coefficient = -1 * gamma
            for word in tf[i]:
                if word.lower() not in vector:
                    vector[word.lower()] = coefficient * tf[i][word]
                else:
                    vector[word.lower()] += coefficient * tf[i][word]

        # find the top2 terms that are not augmented and not stopwords
        term_count = 0
        term = []
        temp = {}

        for word in augmented:
            temp[word] = vector[word]

        while term_count < 2:
            term1 = max(vector.iteritems(), key=operator.itemgetter(1))[0]
            if term1 not in stopwords and term1 not in augmented:
                term.append(term1)
                term_count += 1
                temp[term1] = vector[term1]
                print "Indexing results ...."
            vector.pop(term1, None)

        augmented.append(term[0])
        augmented.append(term[1])

        # refine the order by the weight
        sort = [(k,v) for v,k in sorted([(v,k) for k,v in temp.items()],reverse=True)]
        s = ""
        for (key, value) in sort:
            s += key + '+'
        s = s[:-1]
        print s

        print "Augmenting by %s %s"%(term[0], term[1])
    else:
        print "Desired precision reached, done"
    

