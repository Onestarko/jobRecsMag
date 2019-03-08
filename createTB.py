#coding:utf-8

'''
初始化数据库
'''
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Shell, Manager
import config

app = Flask(__name__)
manager = Manager(app)

dbConf = config.rs_db
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://%s:%s@%s/%s'%(dbConf['user'], dbConf['passwd'], dbConf['host'], dbConf['database'])
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

class Report_form_record(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    报表名称 = db.Column(db.String(64))
    报表需求方 = db.Column(db.String(64))
    需求描述 = db.Column(db.String(64))
    周期 = db.Column(db.String(64))
    执行时间 = db.Column(db.String(30))
    crontabTime = db.Column(db.String(255))
    脚本路径 = db.Column(db.String(80))
    收件人 = db.Column(db.Text())
    delete_flag = db.Column(db.Integer, server_default='0')
    create_time = db.Column(db.DateTime, server_default='0000-00-00 00:00:00')

if __name__ == '__main__':
    manager.run()
