import json
from collections import OrderedDict

def add_info(f,info):
    def wrap(*arg):
        df=f(*arg)
        df["info"]=json.dumps(info,ensure_ascii=False)
        return df
    return wrap

def f1():
    pass

def f2():
    pass

def get_data():
    data = []

    ggtype1 = OrderedDict([("zhaobiao", "001"), ("biangeng", "002"), ("zhongbiao", "003"), ("yucai", "004")])
    ggtype2 = OrderedDict(
        [("zhaobiao", "001"), ("biangeng", "002"), ("zhongbiao", "003"), ("liubiao", "004"), ("yucai", "006")])
    ggtype3 = OrderedDict([("zhaobiao", "001"), ("biangeng", "002"), ("zhongbiao", "003")])
    ggtype4 = OrderedDict(
        [("zhaobiao", "001"), ("biangeng", "002"), ("zhongbiao", "003"), ("liubiao", "004"), ("yucai", "005")])

    gctype = OrderedDict([("勘察设计", "001"), ("施工", "002"), ("监理", "003"), ("专业工程", "004")])

    zbfs = OrderedDict(
        [("公开招标", "001"), ("邀请招标", "002"), ("竞争性磋商", "003"), ("竞争性谈判", "004"), ("询价", "005"), ("单一来源公示", "006")])
    for w1 in ggtype1.keys():
        for w2 in gctype.keys():
            p1 = "079001%s" % (ggtype1[w1])
            p2 = "079001%s%s" % (ggtype1[w1], gctype[w2])
            href = "http://ggzy.linqing.gov.cn/lqweb/jyxx/079001/%s/%s" % (p1, p2)
            tmp = ["gcjs_%s_gctype%s_gg" % (w1, gctype[w2]), href, ["name", "ggstart_time", "href", "info"],
                   add_info(f1, {"gctype": w2}), f2]
            data.append(tmp)

    # for w1 in ggtype2.keys():
    #     for w2 in zbfs.keys():
    #         p1 = "079002%s" % (ggtype2[w1])
    #         p2 = "079002%s%s" % (ggtype2[w1], zbfs[w2])
    #         href = "http://ggzy.linqing.gov.cn/lqweb/jyxx/079002/%s/%s" % (p1, p2)
    #         tmp = ["zfcg_%s_zbfs%s_gg" % (w1, zbfs[w2]), href, ["name", "ggstart_time", "href", "info"],
    #                add_info(f1, {"zbfs": w2}), f2]
    #         data.append(tmp)
    #
    # for w1 in ggtype3.keys():
    #     p1 = "079005%s" % (ggtype3[w1])
    #
    #     href = "http://ggzy.linqing.gov.cn/lqweb/jyxx/079005/%s" % p1
    #     tmp = ["yiliao_%s_gg" % (w1), href, ["name", "ggstart_time", "href", "info"], f1, f2]
    #     data.append(tmp)
    #
    # for w1 in ggtype4.keys():
    #     p1 = "079006%s" % (ggtype4[w1])
    #
    #     href = "http://ggzy.linqing.gov.cn/lqweb/jyxx/079006/%s" % p1
    #     tmp = ["qsydw_%s_gg" % (w1), href, ["name", "ggstart_time", "href", "info"], f1, f2]
    #     data.append(tmp)
    # remove_arr = ["gcjs_biangeng_gctype001_gg", "gcjs_biangeng_gctype004_gg", "gcjs_yucai_gctype004_gg",
    #               "gcjs_yucai_gctype003_gg"
    #     , "zfcg_zhaobiao_zbfs002_gg", "zfcg_biangeng_zbfs002_gg", "zfcg_biangeng_zbfs006_gg",
    #               "zfcg_liaobiao_zbfs006_gg", "zfcg_liubiao_zbfs002_gg", "zfcg_liubiao_zbfs005_gg",
    #               "zfcg_liubiao_zbfs006_gg"
    #     , "zfcg_yucai_zbfs003_gg", "zfcg_yucai_zbfs004_gg"]
    # data1 = data.copy()
    # for w in data:
    #     if w[0] in remove_arr: data1.remove(w)
    # return data1

    return data
data = get_data()

print(data)

"""
[['gcjs_zhaobiao_gctype001_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079001/079001001/079001001001', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x000002645EC4BE18>, <function f2 at 0x000002645EC4B9D8>], 
['gcjs_zhaobiao_gctype002_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079001/079001001/079001001002', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x000002645EC4BEA0>, <function f2 at 0x000002645EC4B9D8>], 
['gcjs_zhaobiao_gctype003_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079001/079001001/079001001003', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x000002645EC4BF28>, <function f2 at 0x000002645EC4B9D8>], 
['gcjs_zhaobiao_gctype004_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079001/079001001/079001001004', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x000002645EC53048>, <function f2 at 0x000002645EC4B9D8>], 


['gcjs_biangeng_gctype002_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079001/079001002/079001002002', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x000002645EC53158>, <function f2 at 0x000002645EC4B9D8>], 
['gcjs_biangeng_gctype003_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079001/079001002/079001002003', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x000002645EC531E0>, <function f2 at 0x000002645EC4B9D8>], 
['gcjs_zhongbiao_gctype001_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079001/079001003/079001003001', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x000002645EC532F0>, <function f2 at 0x000002645EC4B9D8>], 
['gcjs_zhongbiao_gctype002_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079001/079001003/079001003002', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x000002645EC53378>, <function f2 at 0x000002645EC4B9D8>], 
['gcjs_zhongbiao_gctype003_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079001/079001003/079001003003', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x000002645EC53400>, <function f2 at 0x000002645EC4B9D8>], 
['gcjs_zhongbiao_gctype004_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079001/079001003/079001003004', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x000002645EC53488>, <function f2 at 0x000002645EC4B9D8>], 
['gcjs_yucai_gctype001_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079001/079001004/079001004001', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x000002645EC53510>, <function f2 at 0x000002645EC4B9D8>], 
['gcjs_yucai_gctype002_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079001/079001004/079001004002', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x000002645EC53598>, <function f2 at 0x000002645EC4B9D8>]]


"""

"""
[['gcjs_zhaobiao_gctype001_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079001/079001001/079001001001', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x00000150C962DD90>, <function f2 at 0x00000150C962D950>], 
['gcjs_zhaobiao_gctype002_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079001/079001001/079001001002', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x00000150C962DE18>, <function f2 at 0x00000150C962D950>], 
['gcjs_zhaobiao_gctype003_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079001/079001001/079001001003', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x00000150C962DEA0>, <function f2 at 0x00000150C962D950>], 
['gcjs_zhaobiao_gctype004_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079001/079001001/079001001004', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x00000150C962DF28>, <function f2 at 0x00000150C962D950>], 

['gcjs_biangeng_gctype001_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079001/079001002/079001002001', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x00000150C9633048>, <function f2 at 0x00000150C962D950>], 
['gcjs_biangeng_gctype002_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079001/079001002/079001002002', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x00000150C96330D0>, <function f2 at 0x00000150C962D950>], 
['gcjs_biangeng_gctype003_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079001/079001002/079001002003', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x00000150C9633158>, <function f2 at 0x00000150C962D950>], 
['gcjs_biangeng_gctype004_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079001/079001002/079001002004', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x00000150C96331E0>, <function f2 at 0x00000150C962D950>], 

['gcjs_zhongbiao_gctype001_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079001/079001003/079001003001', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x00000150C9633268>, <function f2 at 0x00000150C962D950>], 
['gcjs_zhongbiao_gctype002_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079001/079001003/079001003002', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x00000150C96332F0>, <function f2 at 0x00000150C962D950>],
 ['gcjs_zhongbiao_gctype003_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079001/079001003/079001003003', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x00000150C9633378>, <function f2 at 0x00000150C962D950>], 
 ['gcjs_zhongbiao_gctype004_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079001/079001003/079001003004', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x00000150C9633400>, <function f2 at 0x00000150C962D950>], 
 
 ['gcjs_yucai_gctype001_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079001/079001004/079001004001', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x00000150C9633488>, <function f2 at 0x00000150C962D950>], 
 ['gcjs_yucai_gctype002_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079001/079001004/079001004002', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x00000150C9633510>, <function f2 at 0x00000150C962D950>], 
 ['gcjs_yucai_gctype003_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079001/079001004/079001004003', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x00000150C9633598>, <function f2 at 0x00000150C962D950>], 
 ['gcjs_yucai_gctype004_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079001/079001004/079001004004', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x00000150C9633620>, <function f2 at 0x00000150C962D950>]]

"""
gctype = OrderedDict([("勘察设计", "001"), ("施工", "002"), ("监理", "003"), ("专业工程", "004")])
for w in gctype.keys():
    print(gctype[w])

# a=dict([("zhaobiao", "001"), ("biangeng", "002"), ("zhongbiao", "003"), ("yucai", "004")])
# b=OrderedDict([("zhaobiao", "001"), ("biangeng", "002"), ("zhongbiao", "003"), ("yucai", "004")])
# print(a)
# print(b)