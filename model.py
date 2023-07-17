# coding:utf-8
import datetime
import os

from peewee import CharField, TextField, BooleanField, DateTimeField, IntegerField, Model,MySQLDatabase
# 从环境变量中读取数据库连接信息
db_host = 'db'  # 使用服务名作为主机名
db_port = 3306  # MySQL 的默认端口
db_name = os.getenv('MYSQL_DATABASE')  # 假设你在 .env 文件中设置了这些环境变量
db_user = os.getenv('MYSQL_USER')
db_password = os.getenv('MYSQL_PASSWORD')

database = MySQLDatabase(
    db_name,
    user=db_user,
    password=db_password,
    host=db_host,
    port=db_port,
)


class BaseModel(Model):
    class Meta:
        database = database

class Task(BaseModel):
    user = CharField(default="", max_length=64, index=True)
    chat_id = CharField(default="", max_length=100, index=True)
    message_id = CharField(default="", max_length=100, index=True)
    chat_type = CharField(default="group", max_length=20, index=True)
    params = TextField(default="{}")
    status = CharField(default="init", index=True, max_length=20)  # init running finish error timeout cancel
    result = TextField(default="")
    desc = TextField(default="")
    enable = BooleanField(default=True)
    timestamp = DateTimeField(default=datetime.datetime.now)
    retry_count = IntegerField(default=0)
    task_type = CharField(default="imagine", index=True, max_length=20)
    image_url = TextField(default="")


def initialize_db():
    database.connect()
    database.create_tables([Task])

def main():
    pass


if __name__ == "__main__":
    main()
