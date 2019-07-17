import pymysql

def fetch_one_sql(conn, sql, data=None):
    cursor = conn.cursor()
    cursor.execute(sql, data)
    result = cursor.fetchall()
    cursor.close()
    return result

def oprt_mysql(conn,sql,data=None):
    cursor = conn.cursor()
    cursor.execute(sql, data)
    conn.commit()
    cursor.close()

if __name__ == "__main__":
    conn = pymysql.connect(host='localhost', port=3306,
                    user='root', password='123456',
                    db='xy_test', charset='utf8')
    # sql = "select * from register_account"
    # date = fetch_one_sql(conn,sql)
    # for i in date:
    #     email = i[1]
    #     pwd = i[2]
    #     print(email,pwd)

    email = "snlanl18@gmail.com"
    user_agent = "Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36"
    sql = "update register_account set user_agent=%s where email=%s;"
    oprt_mysql(conn,sql,(user_agent,email))