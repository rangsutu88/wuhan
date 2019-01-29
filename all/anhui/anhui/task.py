from lmf.dbv2 import db_command
from lch.zhulong import anqing
from lch.zhulong import bengbu
from lch.zhulong import bozhou
from lch.zhulong import chaohu
from lch.zhulong import chizhou
from lch.zhulong import chuzhou
from lch.zhulong import fuyang
from lch.zhulong import hefei
from lch.zhulong import huaibei
from lch.zhulong import huainan
from lch.zhulong import huangshan
from lch.zhulong import luan
from lch.zhulong import maanshan
from lch.zhulong import suzhou
from lch.zhulong import tongling
from lch.zhulong import wuhu
from lch.zhulong import xuancheng

from os.path import join, dirname


import time

from lch.zhulong import get_conp,get_conp1


# 1
def task_anqing(**args):
    conp = get_conp(anqing._name_)
    anqing.work(conp, **args)


# 2
def task_bengbu(**args):
    conp = get_conp(bengbu._name_)
    bengbu.work(conp, **args)


# 3
def task_bozhou(**args):
    conp = get_conp(bozhou._name_)
    bozhou.work(conp,cdc_total=None ,**args)


# 4
def task_chaohu(**args):
    conp = get_conp(chaohu._name_)
    chaohu.work(conp, **args)


# 5
def task_chizhou(**args):
    conp = get_conp(chizhou._name_)
    chizhou.work(conp,cdc_total=None , **args)


# 6
def task_chuzhou(**args):
    conp = get_conp(chuzhou._name_)
    chuzhou.work(conp,cdc_total=None , **args)


# 7
def task_fuyang(**args):
    conp = get_conp(fuyang._name_)
    fuyang.work(conp,cdc_total=None , **args)


# 8
def task_hefei(**args):
    conp = get_conp(hefei._name_)
    hefei.work(conp, **args)


# 9
def task_huaibei(**args):
    conp = get_conp(huaibei._name_)
    huaibei.work(conp,cdc_total=None , **args)


# 10
def task_huainan(**args):
    conp = get_conp(huainan._name_)
    huainan.work(conp,cdc_total=None , **args)


# 11
def task_huangshan(**args):
    conp = get_conp(huangshan._name_)
    huangshan.work(conp, **args)


# 12
def task_luan(**args):
    conp = get_conp(luan._name_)
    luan.work(conp, cdc_total=None ,**args)


# 13
def task_maanshan(**args):
    conp = get_conp(maanshan._name_)
    maanshan.work(conp, cdc_total=None ,**args)


# 14
def task_suzhou(**args):
    conp = get_conp(suzhou._name_,'anhui')
    suzhou.work(conp,cdc_total=None , **args)


# 15
def task_tongling(**args):
    conp = get_conp(tongling._name_)
    tongling.work(conp, **args)


# 16
def task_wuhu(**args):
    conp = get_conp(wuhu._name_)
    wuhu.work(conp, **args)


# 17
def task_xuancheng(**args):
    conp = get_conp(xuancheng._name_)
    xuancheng.work(conp ,**args)




def task_all():
    bg = time.time()
    try:
        task_anqing()
        task_bengbu()
        task_bozhou()
        task_chaohu()
        task_chizhou()
    except:
        print("part1 error!")

    try:
        task_chuzhou()
        task_fuyang()
        task_huaibei()
        task_huainan()
        task_huangshan()
    except:
        print("part2 error!")

    try:
        task_luan()
        task_maanshan()
        task_suzhou()
        task_tongling()
        task_wuhu()
    except:
        print("part3 error!")

    try:

        task_xuancheng()
        task_hefei()

    except:
        print("part4 error!")


    ed = time.time()

    cos = int((ed - bg) / 60)

    print("共耗时%d min" % cos)


# write_profile('postgres,since2015,127.0.0.1,shandong')


def create_schemas():
    conp = get_conp1('anhui')
    arr = ["anqing","bengbu","bozhou","chaohu","chizhou","chuzhou","fuyang",
           "huaibei","huainan","huangshan","luan","maanshan"
           ,"suzhou","tongling","wuhu",'xuancheng','hefei'
           ]
    for diqu in arr:
        sql = "create schema if not exists %s" % diqu
        db_command(sql, dbtype="postgresql", conp=conp)




