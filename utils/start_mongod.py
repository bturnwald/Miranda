import subprocess

def start_mongod():
	mgpath = 'C:\\Program Files\\MongoDB\\Server\\3.2\\bin\\mongod.exe'
	dbpath = 'C:\\Users\\Brad\\Github\\haberdas\\Miranda\\data'
	subprocess.Popen([mgpath, '--dbpath', dbpath])

x = start_mongod()

