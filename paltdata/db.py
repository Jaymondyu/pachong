# -- coding: utf-8 --
import mysql.connector
conn = mysql.connector.connect(host='183.66.213.82',port="8803",user= 'tylin',password ='Tylin@123', database = 'regandaccess', auth_plugin='mysql_native_password')
def Add2DetailTable(location, date, orgName, regNum):
    conn = mysql.connector.connect(host='183.66.213.82',port="8803",user= 'tylin',password ='Tylin@123', database = 'regandaccess', auth_plugin='mysql_native_password')
    c = conn.cursor()
    sql = "INSERT INTO reg_Detail (location, date, orgName, regNum) VALUES(%s,%s,%s,%d)"%("'"+location+"'", "'"+date+"'", "'"+orgName+"'", regNum)
    print(sql)
    c.execute(sql)
    conn.commit()

def Add2ChangeTable(location, date, allNum, addNum, deleNum):
    c = conn.cursor()
    sql = "INSERT INTO reg_Change (location, date, allNum, addNum, deleNum) VALUES(%s,%s,%s,%s,%s)"
    data = (location, date, allNum, addNum, deleNum)
    c.execute(sql, data)
    conn.commit()

def SeleAllNumFromChangeTable(location, date):
    c = conn.cursor()
    sql = "SELECT allNum FROM reg_Change WHERE location = '%s' AND date = '%s'" %(location, date)
    c.execute(sql)
    return c.fetchall()[0][0]

def SeleAddNumFromChangeTable(location, date):
    c = conn.cursor()
    sql = "SELECT addNum FROM reg_Change WHERE location = '%s' AND date = '%s'" %(location, date)
    c.execute(sql)
    return c.fetchall()[0][0]

def Getregorgbylocationanddate(location, date1, date2):
    c = conn.cursor()
    sql = "SELECT orgName, regNum, date FROM reg_Detail WHERE location = '%s' AND date BETWEEN'%s' AND '%s' ORDER BY date" %(location, date1, date2)
    # print sql
    c.execute(sql)
    # print c.fetchall()
    return c.fetchall()

def Getregnumbylocationanddate(location, date1, date2, limit1, limit2):
    c = conn.cursor()
    sql = "SELECT allNum, addNum, deleNum, date FROM reg_Change WHERE location = '%s' AND date >= '%s' AND date <= '%s' ORDER BY date  LIMIT %s, %s" %(location, date1, date2, limit1, limit2)
    # print sql
    c.execute(sql)
    # print c.fetchall()
    return c.fetchall()

def Getprojects():
    c = conn.cursor()
    sql = "SELECT DISTINCT location FROM reg_Detail"
    c.execute(sql)
    # print c.fetchall()
    return c.fetchall()


# print Getregnumbylocationanddate("昆明市综合交通国际枢纽建设项目", "2019-09-06", "2019-09-06", 0, 1)[0][0]
