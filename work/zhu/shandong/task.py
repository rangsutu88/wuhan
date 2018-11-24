from zhulong.shandong import anqiu

from zhulong.shandong import binzhou

from zhulong.shandong import dezhou 


from zhulong.shandong import dongying 

from zhulong.shandong import feicheng 

from zhulong.shandong import jiaozhou 

from zhulong.shandong import jinan 

from zhulong.shandong import laiwu 

from zhulong.shandong import leling 

from zhulong.shandong import linqing

from zhulong.shandong import linyi 

from zhulong.shandong import pingdu 

from zhulong.shandong import qingdao 

from zhulong.shandong import rizhao 

from zhulong.shandong import rongcheng

from zhulong.shandong import rushan

from zhulong.shandong import shenghui 

from zhulong.shandong import taian 

from zhulong.shandong import tengzhou 

from zhulong.shandong import weifang 

from zhulong.shandong import weihai 

from zhulong.shandong import xintai 

from zhulong.shandong import yantai

from zhulong.shandong import zaozhuang

from zhulong.shandong import zibo


from os.path import join ,dirname 

# import time 

def get_profile():
    path1=join(dirname(__file__),'profile')
    with open(path1,'r') as f:
        p=f.read()
    
    return p


def write_profile(txt):
    path1=join(dirname(__file__),'profile')
    with open(path1,'w') as f:
        f.write(txt)


def get_conp(txt):
    x=_conp+','+txt
    arr=x.split(',')
    return arr

_conp=get_profile()

#1
def task_anqiu(**args):
    conp=get_conp(anqiu._name_)
    anqiu.work(conp,**args)
#2
def task_binzhou(**args):
    conp=get_conp(binzhou._name_)
    binzhou.work(conp,**args)
#3
def task_dezhou(**args):
    conp=get_conp(dezhou._name_)
    dezhou.work(conp,**args)


#4
def task_dongying(**args):
    conp=get_conp(dongying._name_)
    dongying.work(conp,**args)
#5
def task_feicheng(**args):
    conp=get_conp(feicheng._name_)
    feicheng.work(conp,**args)
#6
def task_jiaozhou(**args):
    conp=get_conp(jiaozhou._name_)
    jiaozhou.work(conp,**args)


#7
def task_jinan(**args):
    conp=get_conp(jinan._name_)
    jinan.work(conp,**args)
#8
def task_laiwu(**args):
    conp=get_conp(laiwu._name_)
    laiwu.work(conp,**args)
#9
def task_leling(**args):
    conp=get_conp(leling._name_)
    leling.work(conp,**args)


#10
def task_linqing(**args):
    conp=get_conp(linqing._name_)
    linqing.work(conp,**args)
#11
def task_linyi(**args):
    conp=get_conp(linyi._name_)
    linyi.work(conp,**args)
#12
def task_pingdu(**args):
    conp=get_conp(pingdu._name_)
    pingdu.work(conp,**args)

#13
def task_qingdao(**args):
    conp=get_conp(qingdao._name_)
    qingdao.work(conp,**args)
#14
def task_rizhao(**args):
    conp=get_conp(rizhao._name_)
    rizhao.work(conp,**args)
#15
def task_rongcheng(**args):
    conp=get_conp(rongcheng._name_)
    rongcheng.work(conp,**args)

#16
def task_rushan(**args):
    conp=get_conp(rushan._name_)
    rushan.work(conp,**args)
#17
def task_shenghui(**args):
    conp=get_conp(shenghui._name_)
    shenghui.work(conp,**args)
#18
def task_taian(**args):
    conp=get_conp(taian._name_)
    taian.work(conp,**args)

#19
def task_tengzhou(**args):
    conp=get_conp(tengzhou._name_)
    tengzhou.work(conp,**args)
#20
def task_weifang(**args):
    conp=get_conp(weifang._name_)
    weifang.work(conp,**args)

#21
def task_weihai(**args):
    conp=get_conp(weihai._name_)
    weihai.work(conp,**args)
#22
def task_xintai(**args):
    conp=get_conp(xintai._name_)
    xintai.work(conp,**args)

#23
def task_yantai(**args):
    conp=get_conp(yantai._name_)
    yantai.work(conp,**args)

#24
def task_zaozhuang(**args):
    conp=get_conp(zaozhuang._name_)
    zaozhuang.work(conp,**args)

#25

def task_zibo(**args):
    conp=get_conp(zibo._name_)
    zibo.work(conp,**args)


def task_all():
    bg=time.time()
    try:
        task_anqiu()
        task_binzhou()
        task_dezhou()
        task_dongying()
        task_feicheng()
    except:
        print("part1 error!")

    try:
        task_jiaozhou()
        task_jinan()
        task_laiwu()
        task_leling()
        task_linqing()
    except:
        print("part2 error!")

    try:
        task_linyi()
        task_pingdu()
        task_qingdao()
        task_rizhao()
        task_rongcheng()
    except:
        print("part3 error!")

    try:


        task_rushan()
        task_shenghui()
        task_taian()
        task_tengzhou()
        task_weifang()
    except:
        print("part4 error!")

    try:
        task_weihai()
        task_xintai()
        task_yantai()
        task_zaozhuang()
        task_zibo()
    except:
        print("part5 error!")

    ed=time.time()


    cos=int((ed-bg)/60)

    print("共耗时%d min"%cos)


#write_profile('postgres,since2015,127.0.0.1,shandong')



def create_schemas():
    conp=get_conp('public')
    arr=["anqiu","binzhou","dongying","feicheng","jiaozhou",
         "dezhou","jinan","laiwu","leling","linqing",
         "pingdu","qingdao","rizhao","rongcheng","rushan",
        "shenghui","taian","tengzhou","weifang","weihai",
        "xintai","yantai","zaozhuang","zibo","linyi"
    ]
    for diqu in arr:
        sql="create schema if not exists %s"%diqu
        db_command(sql,dbtype="postgresql",conp=conp)




