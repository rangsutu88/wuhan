from lmf.dbv2 import db_command
from lch.zhulong import daqing
from lch.zhulong import hegang
from lch.zhulong import heilongjiang
from lch.zhulong import qiqihaer
from lch.zhulong import yichun


from os.path import join, dirname


import time

def get_profile():
    path1 = join(dirname(__file__), 'profile')
    with open(path1, 'r') as f:
        p = f.read()

    return p


def write_profile(txt):
    path1 = join(dirname(__file__), 'profile')
    with open(path1, 'w') as f:
        f.write(txt)


def get_conp(txt):
    x = _conp + ',' + txt
    arr = x.split(',')
    return arr


_conp = get_profile()


# 1
def task_daqing(**args):
    conp = get_conp(daqing._name_)
    daqing.work(conp, **args)


# 2
def task_hegang(**args):
    conp = get_conp(hegang._name_)
    hegang.work(conp, **args)


# 3
def task_heilongjiang(**args):
    conp = get_conp(heilongjiang._name_)
    heilongjiang.work(conp,cdc_total=None ,**args)


# 4
def task_qiqidaer(**args):
    conp = get_conp(qiqihaer._name_)
    qiqihaer.work(conp, **args)


# 5
def task_yichun(**args):
    conp = get_conp(yichun._name_)
    yichun.work(conp,cdc_total=None , **args)







def task_all():
    bg = time.time()
    try:
        task_daqing()
        task_hegang()
        task_qiqidaer()

    except:
        print("part1 error!")

    try:
        task_heilongjiang()
        task_yichun()

    except:
        print("part2 error!")




    ed = time.time()

    cos = int((ed - bg) / 60)

    print("共耗时%d min" % cos)


# write_profile('postgres,since2015,127.0.0.1,shandong')


def create_schemas():
    conp = get_conp('public')
    arr = ["daqing","hegang","heilongjiang",'qiqihaer','yichun'
           ]
    for diqu in arr:
        sql = "create schema if not exists %s" % diqu
        db_command(sql, dbtype="postgresql", conp=conp)




