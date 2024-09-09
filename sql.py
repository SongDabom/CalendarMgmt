import pymysql
import pandas as pd
db = pymysql.connect(
    user='root',
    password='01075375470',
    host='192.168.123.105',
    db='helpdesk',
    charset='utf8'
)
cursor = db.cursor(pymysql.cursors.DictCursor)
# create table
# sql = "CREATE TABLE memberID(" \
#       "ID varchar(20) not null," \
#       "password varchar(10) not null," \
#       "name varchar(12) not null," \
#       "cell_phone varchar(15) not null," \
#       "com_phone varchar(15) not null," \
#       "address varchar(40) not null," \
#       "com_name varchar(30) not null," \
#       "dept_name varchar(20) not null," \
#       "position varchar(10) not null," \
#       "created_by varchar(20) not null," \
#       "created_time datetime not null," \
#       "changed_by varchar(20) not null," \
#       "changed_time datetime not null" \
#       ");"

## insert
sql = "INSERT INTO memberID values('BK12352', 'dsx', '김정일', '010-1554-3456','051-433-3453', '부산 사하구', 'BK', '고객만족팀'," \
      "'부장','BK12345', '2022-01-10 15:29', 'BK12345', '2022-01-10 15:29');"

# update
# sql = "UPDATE memberID set address = '부산 강서구' where ID = 'BK12345'"

# delete
# sql = "DELETE FROM memberID where ID = 'BK12346'"

# sql = "SELECT * FROM memberID;"
cursor.execute(sql)
db.commit()

# to array
# result = cursor.fetchall()
#
# result = pd.DataFrame(result)
# print(result.values.tolist())
