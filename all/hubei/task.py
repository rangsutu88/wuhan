from lmf.dbv2 import db_command
from lch.zhulong import enshi
from lch.zhulong import dangyang
from lch.zhulong import yidu
from lch.zhulong import lichuan


from os.path import join, dirname


import time

from lch.zhulong import get_conp,get_conp1


# 1
def task_dangyang(**args):
    conp = get_conp(dangyang._name_)
    dangyang.work(conp, **args)


# 2
def task_enshi(**args):
    conp = get_conp(enshi._name_)
    enshi.work(conp, **args)


# 3
def task_lichuan(**args):
    conp = get_conp(lichuan._name_)
    lichuan.work(conp,cdc_total=None ,**args)


# 4
def task_yidu(**args):
    conp = get_conp(yidu._name_)
    yidu.work(conp, **args)




def task_all():
    bg = time.time()
    try:
        task_enshi()
        task_dangyang()
        task_lichuan()
        task_yidu()

    except:
        print("part1 error!")


    ed = time.time()

    cos = int((ed - bg) / 60)

    print("共耗时%d min" % cos)


# write_profile('postgres,since2015,127.0.0.1,shandong')


def create_schemas():
    conp = get_conp1('hubei')
    arr = ["dangyang","enshi","lichuan","yidu"]
    for diqu in arr:
        sql = "create schema if not exists %s" % diqu
        db_command(sql, dbtype="postgresql", conp=conp)




