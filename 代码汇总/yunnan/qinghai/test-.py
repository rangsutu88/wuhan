import requests

url='http://www.qhggzyjy.gov.cn/inteligentsearch/rest/inteligentSearch/getFullTextData'
'''
{
"token":"",
"pn":20,
"rn":10,
"sdt":"",
"edt":"",
"wd":"",
"inc_wd":"",
"exc_wd":"",
"fields":"title",
"cnum":"001;002;003;004;005;006;007;008;009;010",
"sort":"{\"showdate\":\"0\"}",
"ssort":"title",
"cl":200,
"terminal":"",
"condition":[
    {"fieldName":"categorynum",
    "isLike":true,
    "likeType":2,
    "equal":"001001001"}
    ],
"time":null,
"highlights":"title",
"statistics":null,
"unionCondition":null,
"accuracy":"100",
"noParticiple":"0",
"searchRange":null,
"isBusiness":1
    }: 
'''


requests.post(url,)