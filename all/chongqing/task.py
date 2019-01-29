from lmf.dbv2 import db_command
from lch.zhulong import yongchuan


from os.path import join, dirname


import time

from lch.zhulong import get_conp,get_conp1


# 1
def task_yongchuan(**args):
    conp = get_conp(yongchuan._name_)
    yongchuan.work(conp, **args)






def task_all():
    bg = time.time()
    try:
        task_yongchuan()

    except:
        print("part1 error!")


    ed = time.time()

    cos = int((ed - bg) / 60)

    print("共耗时%d min" % cos)


# write_profile('postgres,since2015,127.0.0.1,shandong')


def create_schemas():
    conp = get_conp1('chongqing')
    arr = ["yongchuan"]
    for diqu in arr:
        sql = "create schema if not exists %s" % diqu
        db_command(sql, dbtype="postgresql", conp=conp)




