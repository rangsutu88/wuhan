from lmf.dbv2 import db_command

from lch.zhulong import ningxia
from lch.zhulong import yinchuan
from lch.zhulong import guyuan


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
def task_guyuan(**args):
    conp = get_conp(guyuan._name_)
    guyuan.work(conp, **args)


# 2
def task_ningxia(**args):
    conp = get_conp(ningxia._name_)
    ningxia.work(conp, **args)


# 3
def task_yinchuan(**args):
    conp = get_conp(yinchuan._name_)
    yinchuan.work(conp,**args)



def task_all():
    bg = time.time()
    try:
        task_guyuan()

    except:
        print("part1 error!")

    try:
        task_ningxia()



    except:
        print("part2 error!")

    try:
        task_yinchuan()

    except:
        print("part3 error!")


    ed = time.time()

    cos = int((ed - bg) / 60)

    print("共耗时%d min" % cos)


# write_profile('postgres,since2015,127.0.0.1,shandong')


def create_schemas():
    conp = get_conp('public')
    arr = ['guyuan','ningxia','yinchuan']
    for diqu in arr:
        sql = "create schema if not exists %s" % diqu
        db_command(sql, dbtype="postgresql", conp=conp)




