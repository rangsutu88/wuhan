import psycopg2
import os

# city = input("查询的城市：")
city='第二阶段'
os.chdir(os.path.dirname(os.getcwd()))

os.chdir(city)
current_doculist = os.listdir()

print(os.getcwd())
print(os.listdir())

