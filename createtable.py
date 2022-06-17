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
    cur.execute('create table input_select (dev_ID integer ,description text,free integer)')
    conn.commit()
    rows = [(51, '一厅首长讲话主1', 0), (52, '一厅首长讲话主2\n(D01-in02)', 0), (53, '长城主\n(D01-in03)', 0), (54, '一厅通信测站\n(D01-in04)', 0), (55, '一厅通信厅内扩声\n(D01-in05)', 0), (56, '一厅通信自管站\n(D01-in06)', 0), (57, '一厅测控测站\n(D01-in07)', 0), (58, '一厅测控厅内扩声\n(D01-in08)', 0), (59, '一厅测控自管站\n(D01-in09)', 0), (60, '一厅指挥通信话筒主\n(D01-in10)', 0), (61, '一厅指挥测控话筒主\n(D01-in11)', 1), (62, '一厅首长席位主1\n(D02-in01)', 1), (63, '一厅首长席位主2\n(D02-in02)', 1), (64, '一厅参观席位主1\n(D02-in03)', 1), (65, '一厅参观席位主1\n(D02-in03)', 1), (66, '一厅电脑音频2\n(D02-in05)', 1), (67, '一厅无线话筒主1\n(D02-in06)', 1), (68, '一厅无线话筒主2\n(D02-in07)', 1), (69, '一厅无线话筒主3\n(D02-in08)', 1), (70, '一厅图像伴音主1\n(D03-in01)', 1), (71, '一厅图像伴音主2\n(D03-in02)', 1), (72, '一厅首长讲话备1\n(D01-in01)', 1), (73, '一厅首长讲话备2\n(D01-in02)', 1), (74, '长城备\n(D01-in03)', 1), (75, '一厅通信测站(备)\n(D01-in04)', 1), (76, '一厅通信厅内扩声(备)\n(D01-in05)', 1), (77, '一厅通信对内(备)\n(D01-in06)', 1), (78, '一厅测控测站(备)\n(D01-in07)', 1), (79, '一厅测控厅内扩声(备)\n(D01-in08)', 1), (80, '一厅测控中心(备)\n(D01-in09)', 1), (81, '一厅指挥通信话筒备\n(D01-in10)', 1), (82, '一厅指挥测控话筒备\n(D01-in11)', 1), (83, '一厅首长席位备1\n(D02-in01)', 1), (84, '一厅首长席位备2\n(D02-in02)', 1), (85, '一厅参观席位备1\n(D02-in03)', 1), (86, '一厅参观席位备2\n(D02-in04)', 1), (87, '一厅电脑音频\n(D02-in05)', 1), (88, '一厅无线话筒备1\n(D02-in06)', 1), (89, '一厅无线话筒备2\n(D02-in07)', 1), (90, '一厅无线话筒备3\n(D02-in08)', 1), (91, '一厅图像伴音备1\n(D03-in01)', 1), (92, '一厅图像伴音备2\n(D03-in02)', 1), (93, '二厅测控自管站', 1), (94, '二厅测控对内', 1), (95, '二厅通信自管站', 1), (96, '二厅对外', 1), (97, '二厅岗位话筒主5', 1), (98, '二厅长城', 1), (99, '二厅电脑音频', 1), (100, '二厅音源主', 0)]
    # # #
    sql = "insert into input_select (dev_id,description,free) values (:a,:b,:o)"
    cur.executemany(sql,rows)
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

    rows = [(1, '一厅主-音柱A'), (2, '一厅主-音柱B'), (3, '一厅主-低音A'), (4, '一厅主-低音B'), (5, '一厅主-中场-中'), (6, '一厅主-远场A'), (7, '一厅主-远场B'), (8, '终端三监听1'), (9, 'YiTingZhu-4-OUTPUT07'), (10, '一厅备-吸顶1'), (11, '一厅备-吸顶2'), (12, '一厅-终端3监听-2'), (13, '一厅备-中场左'), (14, '一厅备-中场右'), (15, 'YiTingBei-4-OUTPUT07'), (16, '二厅主扩左1'), (17, '二厅主扩右1'), (18, '二厅主扩左2'), (19, '二厅主扩右2'), (20, '综合飞控主扩左1'), (21, '综合飞控主扩右1'), (22, '综合飞控主扩左2'), (23, '综合飞控主扩右2'), (24, '航支室主扩左1'), (25, '航支室主扩右1'), (26, '航支室主扩左2'), (27, '航支室主扩右2'), (28, '三区-新音频1收'), (29, '三区-新音频2收'), (30, '三区-新音频3收'), (31, '三区-新音频4收'), (32, '三区-新音频5收'), (33, '三区-新音频6收'), (34, '三区-新音频7收'), (35, '三区-新音频8收'), (36, '三区-新音频9收'), (37, '三区-新音频10收'), (38, '三区-新音频11收'), (39, '三区-新音频12收'), (40, '三区-新音频13收'), (41, '三区-新音频14收'), (42, '三区-新音频15收'), (43, '三区-新音频16收'), (44, '三区-新音频17收'), (45, '三区-新音频18收'), (46, '三区-新音频19收'), (47, '三区-新音频20收'), (48, '三区-新音频21收'), (49, '三区-新音频22收'), (50, '三区-新音频23收'), (51, '三区-新音频24收'), (52, '三区-4-1收'), (53, '三区-4-2收'), (54, '三区-4-3收'), (55, '三区-4-4收'), (56, '三区-4-5收'), (57, '三区-4-6收'), (58, '三区-4-7收'), (59, '三区-4-8收'), (60, '三区-新音频1收(备)'), (61, '三区-新音频2收(备)'), (62, '三区-新音频3收(备)'), (63, '三区-新音频4收(备)'), (64, '三区-新音频5收(备)'), (65, '三区-新音频6收(备)'), (66, '三区-新音频7收(备)'), (67, '三区-新音频8收(备)'), (68, '三区-新音频9收(备)'), (69, '三区-新音频10收(备)'), (70, '三区-新音频11收(备)'), (71, '三区-新音频12收(备)'), (72, '三区-新音频13收(备)'), (73, '三区-新音频14收(备)'), (74, '三区-新音频15收(备)'), (75, '三区-新音频16收(备)'), (76, '三区-新音频17收(备)'), (77, '三区-新音频18收(备)'), (78, '三区-新音频19收(备)'), (79, '三区-新音频20收(备)'), (80, '三区-新音频21收(备)'), (81, '三区-新音频22收(备)'), (82, '三区-新音频23收(备)'), (83, '三区-新音频24收(备)'), (84, '三区-4-1收(备)'), (85, '三区-4-2收(备)'), (86, '三区-4-3收(备)'), (87, '三区-4-4收(备)'), (88, '三区-4-5收(备)'), (89, '三区-4-6收(备)'), (90, '三区-4-7收(备)'), (91, '三区-4-8收(备)'), (92, 'ZongHeZhu-1-OUTPUT01'), (93, 'ZongHeZhu-1-OUTPUT02'), (94, 'ZongHeBei-1-OUTPUT01'), (95, 'ZongHeBei-1-OUTPUT02'), (96, '载人运控主扩左1'), (97, '载人运控主扩右1'), (98, '载人运控主-实况'), (99, '载人运控主-备用2'), (100, '载人运控备_D01_in_11'), (101, '载人运控备_D01_in_12'), (102, '长管17群'), (103, '长管18群'), (104, '长管19群'), (105, '载人运控厅主扩左2'), (106, '载人运控厅主扩右2'), (107, '载人运控备实况'), (108, '载人运控备-备用2'), (109, '载人运控主_D01_in_11'), (110, '载人运控主_D01_in_12'), (111, '长管17群(备)'), (112, '长管18群(备)'), (113, '长管19群(备)'), (114, '一厅测控神舟'), (115, '一厅测控天地通'), (116, '一厅测控天宫'), (117, '一厅通信神州'), (118, '一厅通信天地通'), (119, '一厅通信天宫'), (120, '二厅测控神舟'), (121, '二厅测控天地通'), (122, '二厅测控天宫'), (123, '二厅通信神州'), (124, '二厅通信天地通'), (125, '二厅通信天宫'), (126, '指挥保障机房-NO'), (127, '载航办科工局'), (128, '总师办'), (129, '战支室'), (130, '航科集团'), (131, '卫生室'), (132, '载航办'), (133, '中科院应用中心'), (134, '五院'), (135, '八院'), (136, '航工所'), (137, '首长休息室-NO'), (138, '发回室-NO'), (139, '测控室'), (140, '通信室'), (141, '气象室'), (142, '综合业务室'), (143, '政工室'), (144, '后勤室'), (145, '机要室-No'), (146, '装备室'), (147, '气象机房'), (148, '搜救室-NO'), (149, '指保室-NO'), (150, '录音1'), (151, '录音2'), (152, '录音3'), (153, '录音4'), (154, '录音5'), (155, '录音6'), (156, '录音7'), (157, '录音8'), (158, '录音9'), (159, '录音10'), (160, '录音11'), (161, '录音12'), (162, '录音13'), (163, '录音14'), (164, '录音15'), (165, '录音16'), (166, '录音17'), (167, '录音18'), (168, '录音19'), (169, '录音20'), (170, '录音21'), (171, '录音22'), (172, '录音23'), (173, '录音24'), (174, '录音25'), (175, '录音26'), (176, '录音27'), (177, '录音28'), (178, '录音29'), (179, '录音30'), (180, '录音31'), (181, '录音32')]
    sql = 'insert into output_list (id,name) values (:a,:b)'
    cur.executemany(sql, rows)
    conn.commit()
    sql = "SELECT * FROM output_list"
    cur.execute(sql)
    results = cur.fetchall()
    print(results)
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
    """
           web_status
    """
    cur.execute('create table web_status (id integer PRIMARY KEY AUTO_INCREMENT,ip text ,status text,port text)')
    conn.commit()

if __name__ == '__main__':
    main()