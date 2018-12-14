def db_write(self, conp, href, page):
    dbtype = "postgresql"
    if dbtype == 'postgresql':
        con = psycopg2.connect(user=conp[0], password=conp[1], host=conp[2], port="5432", database=conp[3])
    elif dbtype == 'mssql':
        con = pymssql.connect(user=conp[0], password=conp[1], host=conp[2], database=conp[3])
    elif dbtype == 'oracle':
        con = cx_Oracle.connect("%s/%s@%s/%s" % (conp[0], conp[1], conp[2], conp[3]))
    else:
        con = MySQLdb.connect(user=conp[0], passwd=conp[1], host=conp[2], db=conp[3])
    sql = """insert into %s.%s values($lmf$%s$lmf$,$lmf$%s$lmf$)""" % (conp[4], conp[5], href, page)
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    cur.close()
    con.close()
