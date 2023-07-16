# coding:utf-8
import datetime
import os

from flask import Flask
from peewee import CharField, TextField, BooleanField, DateTimeField, IntegerField
from playhouse.flask_utils import FlaskDB
DATABASE = f'mysql://{os.getenv("MYSQL_USER")}:{os.getenv("MYSQL_PASSWORD")}@db/{os.getenv("MYSQL_DATABASE")}'
db_wrapper = FlaskDB()


class Task(db_wrapper.Model):
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


def create_app():
    print("init")
    app = Flask(__name__)
    app.config['DATABASE'] = DATABASE
    db_wrapper.init_app(app)
    with db_wrapper.database.atomic():
        db_wrapper.database.create_tables([Task])
    return app


def main():
    pass


if __name__ == "__main__":
    main()
