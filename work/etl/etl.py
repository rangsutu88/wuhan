from lmf.dbv2 import db_command, db_query

from lmfscrap import page

from .multipage import web


# 表名解析器

# tb="gcjs_jiaotong_zhongbiaohx_gg"

def ext_tb(tbname):
    tb_arr = tbname.split("_")

    a = {}
    jytype_set = {'gcjs', 'zfcg'}
    ggtype_set = {'zhaobiao', 'zhongbiao', 'zhongbiaohx', 'biangen', 'liubiao', 'qita', "kongzhijia"}
    jytype_dict = {"gcjs": "工程建设", "zfcg": "政府采购"}
    ggtype_dict = {"zhaobiao": "招标公告", "zhongbiao": "中标公告", "zhongbiaohx": "中标候选公告", "liubiao": "流标公告",
                   "biangen": "变更公告", "qita": "其他公告", "kongzhijia": "控制价公告"}

    xmztype_set = {"fangwu", "jiaotong", "shuili", "shizheng", "dianli"}
    for w in tb_arr:
        if w in jytype_set:
            a["jytype"] = jytype_dict[w]
        if w in ggtype_set:
            a["ggtype"] = ggtype_dict[w]
    if "ggtype" not in a.keys(): a["ggtype"] = None
    if "jytype" not in a.keys(): a["jytype"] = None
    return a


def create_gg(conp):
    sql1 = """
    drop table if exists %s.gg;
    create table if not exists %s.gg
    (
    name text,
    href text,
    ggstart_time text,
    ggtype text,
    jytype text,
    diqu  text,
    info  text ,
    primary key(name,href,ggstart_time)

    )
    """ % (conp[4], conp[4])

    db_command(sql1, dbtype="postgresql", conp=conp)


def insert_tb(tbname, diqu, conp):
    data = ext_tb(tbname)
    ggtype = data["ggtype"]
    jytype = data["jytype"]
    # info=data["info"]
    ggtype = "'%s'" % ggtype if ggtype is not None else "NULL"

    jytype = "'%s'" % jytype if jytype is not None else "NULL"
    schema = conp[4]

    sql2 = """
    insert into %s.gg
    select  distinct on (name,href,ggstart_time ) name,href,ggstart_time,%s::text as ggtype,%s::text as jytype,
    '%s'::text diqu, info from %s.%s
    where (name,href,ggstart_time) not in(select name,href,ggstart_time from %s.gg)
    """ % (schema, ggtype, jytype, diqu, schema, tbname, schema)

    db_command(sql2, dbtype="postgresql", conp=conp)


# 第一次形成gg表
def gg(conp, diqu, i=-1):
    create_gg(conp)
    sql = """
    select table_name from information_schema.tables where table_schema='%s' and table_name ~'_gg$' order by table_name
    """ % conp[4]

    df = db_query(sql, conp=conp, dbtype="postgresql")
    data = df['table_name'].tolist()
    if i == -1:
        data = data
    else:
        data = data[i:i + 1]
    for tbname in data:
        insert_tb(tbname, diqu=diqu, conp=conp)


# 后续更新公告表

def gg_cdc(conp, diqu, i=-1):
    # create_gg(conp)
    sql = """
    select table_name from information_schema.tables where table_schema='%s' and table_name ~'_gg_cdc$' order by table_name
    """ % conp[4]

    df = db_query(sql, conp=conp, dbtype="postgresql")
    data = df['table_name'].tolist()
    if i == -1:
        data = data
    else:
        data = data[i:i + 1]
    for tbname in data:
        insert_tb(tbname, diqu=diqu, conp=conp)


# 一次爬入所有
def work(conp, data, diqu, i=-1, headless=True):
    data = data.copy()
    if i == -1:
        data = data
    else:
        data = data[i:i + 1]
    for w in data:
        setting = {
            "url": w[1],
            "f1": w[3],
            "f2": w[4],
            "tb": w[0],
            "col": w[2],
            "conp": conp,
            "num": 10,
            "headless": headless
        }
        m = web()
        m.write(**setting)



def est_tables(conp, data, headless=True):
    data = data.copy()
    for w in data:
        setting = {
            "url": w[1],
            "f1": w[3],
            "f2": w[4],
            "tb": w[0],
            "col": w[2],
            "conp": conp,
            "num": 10,
            "headless": headless
        }
        m = web()
        m.write(**setting)


def cdc_sql(conp, tb):
    schema = conp[4]
    sql = """insert into %s.%s
select * from %s.%s_cdc 

except 


select * from %s.%s
""" % (schema, tb, schema, tb, schema, tb)
    db_command(sql, dbtype="postgresql", conp=conp)


def cdc(conp, data, diqu, i=-1, headless=True):
    data = data.copy()
    if i == -1:
        data = data
    else:
        data = data[i:i + 1]
    for w in data:
        setting = {
            "url": w[1],
            "f1": w[3],
            "f2": w[4],
            "tb": w[0] + "_cdc",
            "col": w[2],
            "conp": conp,
            "num": 4,
            "total": 10,
            "headless": headless
        }
        m = web()
        m.write(**setting)
        cdc_sql(conp, w[0])

    gg_cdc(conp, diqu)


def est_tables_cdc(conp, data, headless=True):
    data = data.copy()

    for w in data:
        setting = {
            "url": w[1],
            "f1": w[3],
            "f2": w[4],
            "tb": w[0] + "_cdc",
            "col": w[2],
            "conp": conp,
            "num": 4,
            "total": 10,
            "headless": headless
        }
        m = web()
        m.write(**setting)
        cdc_sql(conp, w[0])


def gg_meta(conp, data, diqu, i=-1, headless=True):
    sql = """select table_name from information_schema.tables where table_schema='%s'""" % (conp[4])
    df = db_query(sql, dbtype="postgresql", conp=conp)
    arr = df["table_name"].values

    work(conp, data, diqu, i, headless)
    # if "gg" in arr:
    #     cdc(conp, data, diqu, i, headless)
    # else:
    #     work(conp, data, diqu, i, headless)


#####################################################get_html##########################################


def html_work(conp, f, size=None, headless=True):
    m = page()
    if size is not None:
        sql = "select href from %s.gg where not coalesce(info,'{}')::jsonb?'hreftype' or coalesce(info,'{}')::jsonb->>'hreftype'='可抓网页' limit %d" % (
        conp[4], size)
    else:
        sql = "select href from %s.gg where not coalesce(info,'{}')::jsonb?'hreftype' or coalesce(info,'{}')::jsonb->>'hreftype'='可抓网页' " % (
        conp[4])

    df = db_query(sql, dbtype="postgresql", conp=conp)
    arr = df["href"].values
    print(arr[:3])
    setting = {"num": 20, "arr": arr, "f": f, "conp": conp, "tb": "gg_html", "headless": headless}
    m.write(**setting)


def html_cdc(conp, f, headless=True):
    m = page()
    sql = "select href from %s.gg where href not in(select href from %s.gg_html where not coalesce(info,'{}')::jsonb?'hreftype' or coalesce(info,'{}')::jsonb->>'hreftype'='可抓网页')" % (
    conp[4], conp[4])

    df = db_query(sql, dbtype="postgresql", conp=conp)
    arr = df["href"].values
    if arr == []:
        print("无href更新")
        return None

    setting = {"num": 5, "arr": arr, "f": f, "conp": conp, "tb": "gg_html", "headless": headless}
    m.write(**setting)


def gg_html(conp, f, headless=True):
    sql = """select table_name from information_schema.tables where table_schema='%s'""" % (conp[4])
    df = db_query(sql, dbtype="postgresql", conp=conp)
    arr = df["table_name"].values

    if "gg_html" in arr:
        html_cdc(conp, f, headless=headless)
    else:
        html_work(conp, f, headless=headless)

