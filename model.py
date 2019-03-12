#conding:utf-8

import pymysql
import config

rsDb = config.rs_db
recordDb = pymysql.connect(rsDb['host'], rsDb['user'], rsDb['passwd'], rsDb['database'])

cursor = recordDb.cursor()

'''
	获取定时任务列表
'''
def getJobs():
	sql = '''
		SELECT id, 报表名称, 报表需求方, 需求描述, 周期, 执行时间, crontabTime, 脚本路径, 收件人, delete_flag, create_time FROM report_form_record
	'''

	cursor.execute(sql)

	data = cursor.fetchall()
	res = []
	num = 1
	for i in data:
		res.append({
			"num":num,
			"id":i[0],
			"name":i[1],
			"demander":i[2],
			"desc":i[3],
			"cycle":i[4],
			"jobTime":i[5],
                        "crontabTime":i[6],
			"shPath":i[7],
			"receivers":i[8],
			"createTime":i[10].strftime('%Y-%m-%d'),
			"deleteFlag":int(i[9])
			})
		num += 1

	return res


'''
	根据任务ID获取任务详情
'''
def getJobById(id):
	sql = '''
		SELECT * FROM report_form_record WHERE id = %s
	'''%(id)

	cursor.execute(sql)

	data = cursor.fetchall()
	resData = data[0]
	res = {
		"id" : resData[0],
		"name" : resData[1],
		"demander" : resData[2],
		"desc" : resData[3],
		"cycle" : resData[4],
		"jobTime" : resData[5],
                "crontabTime": resData[6],
		"shPath" : resData[7],
		"receivers" : resData[8],
		"createTime" : resData[10].strftime('%Y-%m-%d')
	}

	return res

'''
	编辑任务记录
	@param id 需要修改的ID
	@param updateData 修改的内容
'''
def updateJob(id, updateData):
	sql = '''
		UPDATE report_form_record SET 报表名称 = '%s', 报表需求方='%s', 需求描述='%s', 周期='%s', 执行时间='%s', 脚本路径='%s', 收件人='%s', crontabTime='%s' 
		WHERE id = %s 
	'''%(updateData['name'], updateData['demander'], updateData['desc'], 
		updateData['cycle'], updateData['jobTime'], updateData['shPath'], updateData['receivers'], updateData['crontabTime'], id)

	cursor.execute(sql)

	try:
		recordDb.commit()
	except:
		return False

	return True


'''
	增加任务记录
	@param insertData
'''
def addJob(insertData):
	sql = '''
		INSERT INTO report_form_record (报表名称, 报表需求方, 需求描述, 周期, 执行时间, crontabTime, 脚本路径, 收件人, create_time)
		VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', now())
	'''%(insertData['name'], insertData['demander'], insertData['desc'], insertData['cycle'], insertData['jobTime'], insertData['crontabTime'], insertData['shPath'],
		insertData['receivers'])

	cursor.execute(sql)

	try:
		recordDb.commit()
	except:
		return False
	return True

'''
	根据任务ID获取crontabTime
	@param id
'''
def getCrontabTimeById(id):
	sql = '''
		select 报表名称, crontabTime, delete_flag, 脚本路径 from report_form_record where id = %s
	'''%(id)

	cursor.execute(sql)

	data = cursor.fetchall()

	resData = [data[0][0], data[0][1], data[0][2], data[0][3]]

	return resData

'''
	修改任务状态
'''
def change(id, type):
        if type == 'stop':
            flag = 1
        elif type == 'restart':
            flag = 0

        sql = "update report_form_record set delete_flag = %d where id = %s"%(flag, id)
        cursor.execute(sql)
        
        try:
            recordDb.commit()
        except:
            return False
        return True
