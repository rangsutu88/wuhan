from lmf.dbv2 import db_command

from zhulong.xizang import xizang
from zhulong.xizang import lasa
from zhulong.xizang import rikaze


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
def task_xizang(**args):
    conp = get_conp(xizang._name_)
    xizang.work(conp, **args)


# 2
def task_rikaze(**args):
    conp = get_conp(rikaze._name_)
    rikaze.work(conp, **args)


# 3
def task_lasa(**args):
    conp = get_conp(lasa._name_)
    lasa.work(conp,**args)


def task_all():
    bg = time.time()
    try:
        task_lasa()

    except:
        print("part1 error!")
    try:

        task_xizang()

    except:
        print("part2 error!")
    try:

        task_rikaze()
    except:
        print("part3 error!")


    ed = time.time()

    cos = int((ed - bg) / 60)

    print("共耗时%d min" % cos)


# write_profile('postgres,since2015,127.0.0.1,shandong')


def create_schemas():
    conp = get_conp('public')
    arr = ['xizang','lasa','rikaze']
    for diqu in arr:
        sql = "create schema if not exists %s" % diqu
        db_command(sql, dbtype="postgresql", conp=conp)




