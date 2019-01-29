from lmf.dbv2 import db_command

from lch.zhulong import baoshan
from lch.zhulong import chuxiong
from lch.zhulong import dali
from lch.zhulong import lijiang
from lch.zhulong import lincang
from lch.zhulong import puer
from lch.zhulong import tengchong
from lch.zhulong import wenshan
from lch.zhulong import yunnan
from lch.zhulong import yuxi
from lch.zhulong import zhaotong
from lch.zhulong import kunming


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
def task_baoshan(**args):
    conp = get_conp(baoshan._name_)
    baoshan.work(conp, **args)


# 2
def task_chuxiong(**args):
    conp = get_conp(chuxiong._name_)
    chuxiong.work(conp, **args)


# 3
def task_dali(**args):
    conp = get_conp(dali._name_)
    dali.work(conp,**args)


# 4
def task_lijiang(**args):
    conp = get_conp(lijiang._name_)
    lijiang.work(conp, **args)


# 5
def task_puer(**args):
    conp = get_conp(puer._name_)
    puer.work(conp , **args)



# 6
def task_tengchong(**args):
    conp = get_conp(tengchong._name_)
    tengchong.work(conp, **args)


# 7
def task_wenshan(**args):
    conp = get_conp(wenshan._name_)
    wenshan.work(conp, **args)




# 8
def task_yunnan(**args):
    conp = get_conp(yunnan._name_)
    yunnan.work(conp, **args)


# 9
def task_yuxi(**args):
    conp = get_conp(yuxi._name_)
    yuxi.work(conp, **args)


# 10
def task_zhaotong(**args):
    conp = get_conp(zhaotong._name_)
    zhaotong.work(conp, **args)


# 11
def task_lincang(**args):
    conp = get_conp(lincang._name_)
    lincang.work(conp ,**args)

def task_kunming(**args):
    conp = get_conp(kunming._name_)
    kunming.work(conp,**args)




def task_all():
    bg = time.time()
    try:
        task_baoshan()
        task_chuxiong()
        task_dali()
        task_lijiang()
        task_lincang()
    except:
        print("part1 error!")

    try:
        task_puer()
        task_tengchong()
        task_wenshan()
        task_yunnan()
        task_yuxi()


    except:
        print("part2 error!")

    try:
        task_zhaotong()
        task_kunming()
    except:
        print("part3 error!")


    ed = time.time()

    cos = int((ed - bg) / 60)

    print("共耗时%d min" % cos)


# write_profile('postgres,since2015,127.0.0.1,shandong')


def create_schemas():
    conp = get_conp('public')
    arr = ['baoshan','chuxiong','dali','lijiang','lincang','puer','tengchong','wenshan','yunnan','yuxi','zhaotong','kunming']
    for diqu in arr:
        sql = "create schema if not exists %s" % diqu
        db_command(sql, dbtype="postgresql", conp=conp)




