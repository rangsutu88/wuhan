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

    for w1 in ggtype2.keys():
        for w2 in zbfs.keys():
            p1 = "079002%s" % (ggtype2[w1])
            p2 = "079002%s%s" % (ggtype2[w1], zbfs[w2])
            href = "http://ggzy.linqing.gov.cn/lqweb/jyxx/079002/%s/%s" % (p1, p2)
            tmp = ["zfcg_%s_zbfs%s_gg" % (w1, zbfs[w2]), href, ["name", "ggstart_time", "href", "info"],
                   add_info(f1, {"zbfs": w2}), f2]
            data.append(tmp)

    for w1 in ggtype3.keys():
        p1 = "079005%s" % (ggtype3[w1])

        href = "http://ggzy.linqing.gov.cn/lqweb/jyxx/079005/%s" % p1
        tmp = ["yiliao_%s_gg" % (w1), href, ["name", "ggstart_time", "href", "info"], f1, f2]
        data.append(tmp)

    for w1 in ggtype4.keys():
        p1 = "079006%s" % (ggtype4[w1])

        href = "http://ggzy.linqing.gov.cn/lqweb/jyxx/079006/%s" % p1
        tmp = ["qsydw_%s_gg" % (w1), href, ["name", "ggstart_time", "href", "info"], f1, f2]
        data.append(tmp)
    remove_arr = ["gcjs_biangeng_gctype001_gg", "gcjs_biangeng_gctype004_gg", "gcjs_yucai_gctype004_gg",
                  "gcjs_yucai_gctype003_gg"
        , "zfcg_zhaobiao_zbfs002_gg", "zfcg_biangeng_zbfs002_gg", "zfcg_biangeng_zbfs006_gg",
                  "zfcg_liaobiao_zbfs006_gg", "zfcg_liubiao_zbfs002_gg", "zfcg_liubiao_zbfs005_gg",
                  "zfcg_liubiao_zbfs006_gg"
        , "zfcg_yucai_zbfs003_gg", "zfcg_yucai_zbfs004_gg"]
    data1 = data.copy()
    for w in data:
        if w[0] in remove_arr: data1.remove(w)
    return data1


data = get_data()



"""
[
    ['gcjs_zhaobiao_gctype001_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079001/079001001/079001001001', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x000000000A6607B8>, <function f2 at 0x000000000A6606A8>], 
    ['gcjs_zhaobiao_gctype002_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079001/079001001/079001001002', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x000000000A660840>, <function f2 at 0x000000000A6606A8>], 
    ['gcjs_zhaobiao_gctype003_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079001/079001001/079001001003', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x000000000A6608C8>, <function f2 at 0x000000000A6606A8>], 
    ['gcjs_zhaobiao_gctype004_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079001/079001001/079001001004', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x000000000A660950>, <function f2 at 0x000000000A6606A8>],
    ['gcjs_biangeng_gctype002_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079001/079001002/079001002002', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x000000000A660A60>, <function f2 at 0x000000000A6606A8>],
    ['gcjs_biangeng_gctype003_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079001/079001002/079001002003', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x000000000A660AE8>, <function f2 at 0x000000000A6606A8>], 
    ['gcjs_zhongbiao_gctype001_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079001/079001003/079001003001', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x000000000A660BF8>, <function f2 at 0x000000000A6606A8>], 
    ['gcjs_zhongbiao_gctype002_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079001/079001003/079001003002', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x000000000A660C80>, <function f2 at 0x000000000A6606A8>], 
    ['gcjs_zhongbiao_gctype003_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079001/079001003/079001003003', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x000000000A660D08>, <function f2 at 0x000000000A6606A8>], 
    ['gcjs_zhongbiao_gctype004_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079001/079001003/079001003004', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x000000000A660D90>, <function f2 at 0x000000000A6606A8>], 
    ['gcjs_yucai_gctype001_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079001/079001004/079001004001', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x000000000A660E18>, <function f2 at 0x000000000A6606A8>], 
    ['gcjs_yucai_gctype002_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079001/079001004/079001004002', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x000000000A660EA0>, <function f2 at 0x000000000A6606A8>], 
    ['zfcg_zhaobiao_zbfs001_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079002/079002001/079002001001', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x000000000A6660D0>, <function f2 at 0x000000000A6606A8>], 
    ['zfcg_zhaobiao_zbfs003_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079002/079002001/079002001003', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x000000000A6661E0>, <function f2 at 0x000000000A6606A8>], 
    ['zfcg_zhaobiao_zbfs004_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079002/079002001/079002001004', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x000000000A666268>, <function f2 at 0x000000000A6606A8>], 
    ['zfcg_zhaobiao_zbfs005_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079002/079002001/079002001005', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x000000000A6662F0>, <function f2 at 0x000000000A6606A8>], 
    ['zfcg_zhaobiao_zbfs006_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079002/079002001/079002001006', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x000000000A666378>, <function f2 at 0x000000000A6606A8>], 
    ['zfcg_biangeng_zbfs001_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079002/079002002/079002002001', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x000000000A666400>, <function f2 at 0x000000000A6606A8>], 
    ['zfcg_biangeng_zbfs003_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079002/079002002/079002002003', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x000000000A666510>, <function f2 at 0x000000000A6606A8>], 
    ['zfcg_biangeng_zbfs004_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079002/079002002/079002002004', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x000000000A666598>, <function f2 at 0x000000000A6606A8>], 
    ['zfcg_biangeng_zbfs005_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079002/079002002/079002002005', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x000000000A666620>, <function f2 at 0x000000000A6606A8>], 
    ['zfcg_zhongbiao_zbfs001_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079002/079002003/079002003001', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x000000000A666730>, <function f2 at 0x000000000A6606A8>], 
    ['zfcg_zhongbiao_zbfs002_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079002/079002003/079002003002', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x000000000A6667B8>, <function f2 at 0x000000000A6606A8>], 
    ['zfcg_zhongbiao_zbfs003_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079002/079002003/079002003003', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x000000000A666840>, <function f2 at 0x000000000A6606A8>], 
    ['zfcg_zhongbiao_zbfs004_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079002/079002003/079002003004', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x000000000A6668C8>, <function f2 at 0x000000000A6606A8>], 
    ['zfcg_zhongbiao_zbfs005_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079002/079002003/079002003005', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x000000000A666950>, <function f2 at 0x000000000A6606A8>], 
    ['zfcg_zhongbiao_zbfs006_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079002/079002003/079002003006', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x000000000A6669D8>, <function f2 at 0x000000000A6606A8>], 
    ['zfcg_liubiao_zbfs001_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079002/079002004/079002004001', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x000000000A666A60>, <function f2 at 0x000000000A6606A8>], 
    ['zfcg_liubiao_zbfs003_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079002/079002004/079002004003', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x000000000A666B70>, <function f2 at 0x000000000A6606A8>], 
    ['zfcg_liubiao_zbfs004_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079002/079002004/079002004004', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x000000000A666BF8>, <function f2 at 0x000000000A6606A8>], 
    ['zfcg_yucai_zbfs001_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079002/079002006/079002006001', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x000000000A666D90>, <function f2 at 0x000000000A6606A8>], 
    ['zfcg_yucai_zbfs002_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079002/079002006/079002006002', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x000000000A666E18>, <function f2 at 0x000000000A6606A8>], 
    ['zfcg_yucai_zbfs005_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079002/079002006/079002006005', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x000000000A668048>, <function f2 at 0x000000000A6606A8>], 
    ['zfcg_yucai_zbfs006_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079002/079002006/079002006006', ['name', 'ggstart_time', 'href', 'info'], <function add_info.<locals>.wrap at 0x000000000A6680D0>, <function f2 at 0x000000000A6606A8>], 
    ['yiliao_zhaobiao_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079005/079005001', ['name', 'ggstart_time', 'href', 'info'], <function f1 at 0x0000000000BF7E18>, <function f2 at 0x000000000A6606A8>], 
    ['yiliao_biangeng_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079005/079005002', ['name', 'ggstart_time', 'href', 'info'], <function f1 at 0x0000000000BF7E18>, <function f2 at 0x000000000A6606A8>], 
    ['yiliao_zhongbiao_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079005/079005003', ['name', 'ggstart_time', 'href', 'info'], <function f1 at 0x0000000000BF7E18>, <function f2 at 0x000000000A6606A8>], 
    ['qsydw_zhaobiao_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079006/079006001', ['name', 'ggstart_time', 'href', 'info'], <function f1 at 0x0000000000BF7E18>, <function f2 at 0x000000000A6606A8>], 
    ['qsydw_biangeng_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079006/079006002', ['name', 'ggstart_time', 'href', 'info'], <function f1 at 0x0000000000BF7E18>, <function f2 at 0x000000000A6606A8>], 
    ['qsydw_zhongbiao_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079006/079006003', ['name', 'ggstart_time', 'href', 'info'], <function f1 at 0x0000000000BF7E18>, <function f2 at 0x000000000A6606A8>], 
    ['qsydw_liubiao_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079006/079006004', ['name', 'ggstart_time', 'href', 'info'], <function f1 at 0x0000000000BF7E18>, <function f2 at 0x000000000A6606A8>], 
    ['qsydw_yucai_gg', 'http://ggzy.linqing.gov.cn/lqweb/jyxx/079006/079006005', ['name', 'ggstart_time', 'href', 'info'], <function f1 at 0x0000000000BF7E18>, <function f2 at 0x000000000A6606A8>]]

"""


a=dict([("zhaobiao", "001"), ("biangeng", "002"), ("zhongbiao", "003"), ("yucai", "004")])
b=OrderedDict([("zhaobiao", "001"), ("biangeng", "002"), ("zhongbiao", "003"), ("yucai", "004")])
print(a)
print(b)