import STPython
def main():
    conn =STPython.connect('SYSDBA','szoscar55')
    cur = conn.cursor()
    """
    usradmin
    """
    cur.execute('create table usradmin (id integer PRIMARY KEY AUTO_INCREMENT,username text,passwd text)')
    conn.commit()
    print('*' * 6 + 'usradmin创建成功')
    cur.execute('INSERT INTO usradmin (username,passwd)values (:a,:b)', ('admin','4c635087df1041bd13681ee3c6eb04d5'))
    conn.commit()
    # sql = "SELECT * FROM usradmin"
    # cur.execute(sql)
    # results = cur.fetchall()
    # print(results)
    # print('*' * 6 + 'usradmin展示')
    """
    暂时关闭删除功能
    """
    # cur.execute('delete from usradmin ;')
    # conn.commit()
    # cur.execute('drop table  usradmin ')
    # conn.commit()
    """
    input
    """

    print('==='*6+'分割副'+'==='*6)
    cur.execute('create table input_select (dev_ID integer PRIMARY KEY AUTO_INCREMENT,description text,free integer)')
    conn.commit()
    # #
    # cur.execute('INSERT INTO input_select (description ,free) values (:1,:2)',("ces",'ces'))
    # conn.commit()
    # sql = "SELECT * FROM input_select"
    # cur.execute(sql)
    # results = cur.fetchall()
    # print(results)
    # cur.execute('delete from input_select ;')
    # conn.commit()
    # cur.execute('drop table  input_select ')
    # conn.commit()
    print('===' * 6 + '分割副' + '===' * 6)
    """
       output
    """
    cur.execute('create table output_list (id integer PRIMARY KEY AUTO_INCREMENT,name text)')
    conn.commit()

    # cur.execute('INSERT INTO output_list (name) values (:1)',('s'))
    # conn.commit()
    # sql = "SELECT * FROM output_list"
    # cur.execute(sql)
    # results = cur.fetchall()
    # print(results)
    # cur.execute('delete from output_list ;')
    # conn.commit()
    # cur.execute('drop table  output_list ')
    # conn.commit()
    """
       tcp_status
    """
    cur.execute('create table tcp_status (id integer PRIMARY KEY AUTO_INCREMENT,ip text ,status text)')
    conn.commit()
    #
    cur.execute('INSERT INTO tcp_status (ip,status) values (:1,:2)',('192.1.1.1','off'))
    conn.commit()
    # sql = "SELECT * FROM tcp_status"
    # cur.execute(sql)
    # results = cur.fetchall()
    # print(results)

    # cur.execute('delete from tcp_status ;')
    # conn.commit()
    # cur.execute('drop table  tcp_status ')
    # conn.commit()
    """
      template
    """
    sql = "create table template (name text ,key1 varchar (200),key2 varchar(200),key3 varchar(200),key4 varchar(200),key5 varchar(200),key6 varchar(200),key7 varchar(200),key8 varchar(200),key9 varchar(200),key10 varchar(200),key11 varchar(200),key12 varchar(200))"
    cur.execute(sql)
    # conn.commit()
    # cur.execute("INSERT INTO template  values ('a,b,c')")
    # sql = "SELECT * FROM template"
    # cur.execute(sql)
    #
    # cur.execute('delete from template ;')
    # conn.commit()
    # cur.execute('drop table  template ')
    # conn.commit()
    """
      keys
    """
    sql = "create table keys_set (id integer PRIMARY KEY AUTO_INCREMENT,inputID integer ,inputName text,ip text,description text,keyName varchar (200),key1 varchar (200),key2 varchar(200),key3 varchar(200),key4 varchar(200),key5 varchar(200),key6 varchar(200),key7 varchar(200),key8 varchar(200),key9 varchar(200),key10 varchar(200),key11 varchar(200),key12 varchar(200),key1id varchar (200),key2id varchar(200),key3id varchar(200),key4id varchar(200),key5id varchar(200),key6id varchar(200),key7id varchar(200),key8id varchar(200),key9id varchar(200),key10id varchar(200),key11id varchar(200),key12id varchar(200),status text)"
    cur.execute(sql)
    conn.commit()

    #
    # cur.execute('delete from keys_set ;')
    # conn.commit()
    # cur.execute('drop table  keys_set ')
    # conn.commit()

if __name__ == '__main__':
    main()