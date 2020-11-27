host = "127.0.0.1"
prot = "3306"
username = "root"
password = "010207"
database = "books"
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(username,password,host,prot,database)
SQLALCHEMY_TRACK_MODIFICATIONS = True
