import STPython

def main():
    # conn =STPython.connect('SYSDBA', 'szoscar55', dsn='127.0.0.1:2003/osrdb')
    conn =STPython.connect('SYSDBA', 'szoscar55', dsn='127.0.0.1:2004/keys')
    cur = conn.cursor()

    """
    usradmin
    """
    cur.execute('create table usradmin (id integer PRIMARY KEY AUTO_INCREMENT,username text,passwd text)')
    conn.commit()
    cur.execute('INSERT INTO usradmin (username,passwd)values (:a,:b)', ('admin', '4c635087df1041bd13681ee3c6eb04d5'))
    conn.commit()
    print('USRADMIN表创建成功')
    print('==='*12)

    """
    input
    """
    cur.execute('create table input_select (dev_ID integer, description text, free integer)')
    conn.commit()
    rows = [(1, '测试输入1', 1), (2, '测试输入2', 1), (3, '测试输入3', 1)]
    sql = "insert into input_select (dev_id,description,free) values (:a,:b,:o)"
    cur.executemany(sql, rows)
    conn.commit()
    print('INPUT_SELECT表创建成功')
    print('===' * 12)

    """
    output
    """
    cur.execute('create table output_list (id integer PRIMARY KEY, name text)')
    conn.commit()
    rows = [(1, '测试输出1'), (2, '测试输出2'), (3, '测试输出3')]
    sql = 'insert into output_list (id,name) values (:a,:b)'
    cur.executemany(sql, rows)
    conn.commit()
    print('OUTPUT_LIST表创建成功')
    print('===' * 12)

    """
    keys
    """
    sql = "create table keys_set (id integer PRIMARY KEY AUTO_INCREMENT,inputID text ,inputName text,ip text,description text,keyName varchar (1000),key1 varchar (200),key2 varchar(200),key3 varchar(200),key4 varchar(200),key5 varchar(200),key6 varchar(200),key7 varchar(200),key8 varchar(200),key9 varchar(200),key10 varchar(200),key11 varchar(200),key12 varchar(200),key1id varchar (200),key2id varchar(200),key3id varchar(200),key4id varchar(200),key5id varchar(200),key6id varchar(200),key7id varchar(200),key8id varchar(200),key9id varchar(200),key10id varchar(200),key11id varchar(200),key12id varchar(200),status text)"
    cur.execute(sql)
    conn.commit()
    print('KEYS_SET表创建成功')
    print('===' * 12)

    """
    template
    """
    sql = "create table template (name text,key1 varchar (200),key2 varchar(200),key3 varchar(200),key4 varchar(200),key5 varchar(200),key6 varchar(200),key7 varchar(200),key8 varchar(200),key9 varchar(200),key10 varchar(200),key11 varchar(200),key12 varchar(200),keyName varchar (1000))"
    cur.execute(sql)
    conn.commit()
    print('TEMPLATE表创建成功')
    print('===' * 12)

    """
    task
    """
    sql = "create table task (name text ,taskmap varchar (1000))"
    cur.execute(sql)
    conn.commit()
    print('TASK表创建成功')
    print('===' * 12)

    """
    web_status
    """
    cur.execute('create table web_status (id integer PRIMARY KEY AUTO_INCREMENT,ip text ,status text,port text)')
    conn.commit()
    print('WEB_STATUS表创建成功')
    print('===' * 12)

if __name__ == '__main__':
    main()