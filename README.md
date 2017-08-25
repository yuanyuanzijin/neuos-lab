# NEU OS实验分发平台Web端

## 使用说明

### 环境

#### Python

开发过程中使用Python 2.7，建议配置虚拟环境。

#### 依赖
安装依赖只需在终端运行：

`pip install -r requirements.txt`

如果安装过程中报错，请使用sudo，如依然提示缺少某些基本库，对应安装即可。

### 使用

第一次运行需要一些配置操作。

#### 数据库初始化

删除开发时的db.sqlite3文件，重新建立SQLite数据库

`python manage.py migrate`

使数据库模型生效

`python manage.py makemigrations main`

建立Superuser账号

`python manage.py createsuperuser`

#### 配置文件 neuos/settings.py

最下端的几个变量需要更换成自己的，分别是CAS转向地址，Github OAuth的Client ID和Client Secret。

> CAS_REDIRECT_URL = 'http://your_domain/cas'

> CLIENT_ID = '0e7ffa086913cce028b0'

> CLIENT_SECRET = 'dace5dfc9c3e47685b7bee1500e34725c965226f'`

#### 启动网站

在不使用Apache等服务器的情况下，可使用以下指令启动网站：

`python manage.py runserver 0.0.0.0:port`

#### 教师信息导入

访问http://your_domain/admin，使用之前配置好的SuperUser账号登录。

打开首页的User表，选择添加user，输入老师的教工号，将user_type设为老师即可。


## 开发说明

详见Wiki[开发说明](http://git.yuanyuanzijin.com/ZijinAI/Neuos/wiki/%E5%BC%80%E5%8F%91%E8%AF%B4%E6%98%8E)
