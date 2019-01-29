from lmf.dbv2 import db_command
from lch.zhulong import xinjiang
from lch.zhulong import wulumuqi
from lch.zhulong import atushen
from lch.zhulong import beitun


from os.path import join, dirname


import time

from lch.zhulong import get_conp,get_conp1


# 1
def task_xinjiang(**args):
    conp = get_conp(xinjiang._name_)
    xinjiang.work(conp,pageLoadStrategy = "none",pageloadtimeout=80, **args)


# 2
def task_wulumuqi(**args):
    conp = get_conp(wulumuqi._name_)
    wulumuqi.work(conp, **args)


# 3
def task_beitun(**args):
    conp = get_conp(beitun._name_)
    beitun.work(conp,pageLoadStrategy = "none",**args)


# 4
def task_atushen(**args):
    conp = get_conp(atushen._name_)
    atushen.work(conp, **args)




def task_all():
    bg = time.time()
    try:
        task_xinjiang()
        task_wulumuqi()


    except:
        print("part1 error!")

    try:
        task_beitun()
        task_atushen()

    except:
        print("part2 error!")



    ed = time.time()

    cos = int((ed - bg) / 60)

    print("共耗时%d min" % cos)


# write_profile('postgres,since2015,127.0.0.1,shandong')


def create_schemas():
    conp = get_conp1('xinjiang')
    arr = ["xinjiang","beitun","atushen","wulumuqi"]
    for diqu in arr:
        sql = "create schema if not exists %s" % diqu
        db_command(sql, dbtype="postgresql", conp=conp)


