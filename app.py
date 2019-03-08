#coding:utf-8

from flask import Flask, render_template, url_for, request, redirect
from flask_bootstrap import Bootstrap
import model
import json
from crontab import CronTab
import config

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def list():
	jobs = model.getJobs()
	return render_template("list.html", jobs=jobs)

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
	if request.method == 'GET':
            job = model.getJobById(id)
            return render_template("edit.html", job=job)
	elif request.method == "POST":
		updateData = {
			"name":request.form['name'],
			"demander":request.form['demander'],
			"desc":request.form['desc'],
			"cycle":request.form['cycle'],
                        "crontabTime":request.form['crontabTime'],
			"jobTime":request.form['jobTime'],
			"shPath":request.form['shPath'],
			"receivers":request.form['receivers']
		}

		#检查crontab是否需要修改
		resData = model.getCrontabTimeById(id)
		
		if resData[1] == request.form['crontabTime'] or int(resData[2]) == 1:
			pass
		else:
			jobName = resData[0]
			cronUser = CronTab(user = True)
			editJob = cronUser.find_comment(jobName)
			cronUser.remove(editJob)
			addJob = cronUser.new(command = config.cronPath+'/'+request.form['shPath'])
			addJob.setall(request.form['crontabTime'])
			addJob.set_comment(request.form['name'])
			cronUser.write()

		res = model.updateJob(id, updateData)
		if res == True:
			return redirect('/')
		else:
			return "修改出错"

@app.route("/add", methods=["GET", "POST"])
def add():
	if request.method == "GET":
		return render_template("add.html")
	elif request.method == "POST":
		insertData = {
			"name":request.form['name'],
			"demander":request.form['demander'],
			"desc":request.form['desc'],
			"cycle":request.form['cycle'],
			"jobTime":request.form['jobTime'],
                        "crontabTime":request.form['crontabTime'],
			"shPath":request.form['shPath'],
			"receivers":request.form['receivers']
		}

		res = model.addJob(insertData)
		#添加crontab任务
		cronUser = CronTab(user=True)
		cod = config.cronPath + '/'+request.form['shPath']
		job = cronUser.new(command=cod)
		job.setall(request.form['crontabTime'])
		job.set_comment(request.form['name'])
		cronUser.write()

		if res == True:
			return redirect('/')
		else:
			return "添加出错"

@app.route("/stop/<id>", methods=["GET", "POST"])
def stop(id):
	#将delete_flag 设置为1
	model.change(id, 'stop')

	#将crontab失效
	resData = model.getCrontabTimeById(id)
	jobName = resData[0]
	cronUser = CronTab(user = True)
	editJob = cronUser.find_comment(jobName)
	cronUser.remove(editJob)
	cronUser.write()
	return redirect('/')

@app.route("/restart/<id>", methods=["GET", "POST"])
def restart(id):
	#将delete_flag 设置为1
	model.change(id, 'restart')

	#新增crontab
	resData = model.getCrontabTimeById(id)
	jobName = resData[0]
	
	cronUser = CronTab(user = True)
	addJob = cronUser.new(command = config.cronPath+'/'+resData[3])
	addJob.setall(resData[1])
	addJob.set_comment(jobName)
	cronUser.write()
	return redirect('/')


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000, debug=True)
