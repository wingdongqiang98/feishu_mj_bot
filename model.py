# coding:utf-8
import datetime
import os

from peewee import CharField, TextField, BooleanField, DateTimeField, IntegerField, Model
from playhouse.db_url import connect
DATABASE = f'mysql://{os.getenv("MYSQL_USER")}:{os.getenv("MYSQL_PASSWORD")}@db/{os.getenv("MYSQL_DATABASE")}'
database = connect(DATABASE)


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
