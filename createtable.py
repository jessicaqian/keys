import STPython
def main():
    conn =STPython.connect('SYSDBA','szoscar55',dsn='127.0.0.1:2003/osrdb')
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
    cur.execute('create table input_select (dev_ID text,description text,free integer)')
    conn.commit()
    rows = [(51, '一厅首长讲话主1', 0), (52, '一厅首长讲话主2\n(D01-in02)', 0), (53, '长城主\n(D01-in03)', 0), (54, '一厅通信测站\n(D01-in04)', 0), (55, '一厅通信厅内扩声\n(D01-in05)', 0), (56, '一厅通信自管站\n(D01-in06)', 0), (57, '一厅测控测站\n(D01-in07)', 0), (58, '一厅测控厅内扩声\n(D01-in08)', 0), (59, '一厅测控自管站\n(D01-in09)', 0), (60, '一厅指挥通信话筒主\n(D01-in10)', 0), (61, '一厅指挥测控话筒主\n(D01-in11)', 1), (62, '一厅首长席位主1\n(D02-in01)', 1), (63, '一厅首长席位主2\n(D02-in02)', 1), (64, '一厅参观席位主1\n(D02-in03)', 1), (65, '一厅参观席位主1\n(D02-in03)', 1), (66, '一厅电脑音频2\n(D02-in05)', 1), (67, '一厅无线话筒主1\n(D02-in06)', 1), (68, '一厅无线话筒主2\n(D02-in07)', 1), (69, '一厅无线话筒主3\n(D02-in08)', 1), (70, '一厅图像伴音主1\n(D03-in01)', 1), (71, '一厅图像伴音主2\n(D03-in02)', 1), (72, '一厅首长讲话备1\n(D01-in01)', 1), (73, '一厅首长讲话备2\n(D01-in02)', 1), (74, '长城备\n(D01-in03)', 1), (75, '一厅通信测站(备)\n(D01-in04)', 1), (76, '一厅通信厅内扩声(备)\n(D01-in05)', 1), (77, '一厅通信对内(备)\n(D01-in06)', 1), (78, '一厅测控测站(备)\n(D01-in07)', 1), (79, '一厅测控厅内扩声(备)\n(D01-in08)', 1), (80, '一厅测控中心(备)\n(D01-in09)', 1), (81, '一厅指挥通信话筒备\n(D01-in10)', 1), (82, '一厅指挥测控话筒备\n(D01-in11)', 1), (83, '一厅首长席位备1\n(D02-in01)', 1), (84, '一厅首长席位备2\n(D02-in02)', 1), (85, '一厅参观席位备1\n(D02-in03)', 1), (86, '一厅参观席位备2\n(D02-in04)', 1), (87, '一厅电脑音频\n(D02-in05)', 1), (88, '一厅无线话筒备1\n(D02-in06)', 1), (89, '一厅无线话筒备2\n(D02-in07)', 1), (90, '一厅无线话筒备3\n(D02-in08)', 1), (91, '一厅图像伴音备1\n(D03-in01)', 1), (92, '一厅图像伴音备2\n(D03-in02)', 1), (93, '二厅测控自管站', 1), (94, '二厅测控对内', 1), (95, '二厅通信自管站', 1), (96, '二厅对外', 1), (97, '二厅岗位话筒主5', 1), (98, '二厅长城', 1), (99, '二厅电脑音频', 1), (100, '二厅音源主', 0)]
    # # #
    sql = "insert into input_select (dev_id,description,free) values (:a,:b,:o)"
    cur.executemany(sql,rows)
    # cur.execute('INSERT INTO input_select (description ,free) values (:1,:2)',("ces",'ces'))
    conn.commit()
    sql = "SELECT * FROM input_select"
    cur.execute(sql)
    results = cur.fetchall()
    print(results)
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
    # #
    # cur.execute('INSERT INTO tcp_status (ip,status) values (:1,:2)',('192.1.1.1','off'))
    # conn.commit()
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
    conn.commit()
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