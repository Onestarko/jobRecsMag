# jobRecsMag

*crontab定时工具*

##### 工具界面

![image-20190308170909493](https://i.loli.net/2019/03/08/5c82343b6f2e0.png)

##### 配置的定时任务可查看

![image-20190308171046473](https://i.loli.net/2019/03/08/5c8234b796c35.png)

### 一、安装需要的包

```
pip install -r requiesments.txt
```



二、配置文件



### 二、初始化数据库

```shell
python createTB.py db migrate
```

```shell
python createTB.py db upgrades
```



三、启动服务

```
python app.py
```

