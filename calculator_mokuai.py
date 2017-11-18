#!/usr/bin/env python3
import sys,os.path,getopt,configparser,datetime
from multiprocessing import Process,Queue
queue1=Queue()
queue2=Queue()
class Config:
	def __init__(self,config_file,city):
		self.conf = configparser.ConfigParser()
		self.conf.read(config_file)
		self.city=city
		self.section=self.conf.sections()
		if self.city not in self.section:
			sys.exit('wrong city name')
		else:
			pass
	def get_config(self,value):
		try:
			return self.conf.get(self.city,value)
		except:
			sys.exit('no this value')
class UserData:
	def __init__(self,userdatafile):
		self.userdata = []
		if len(userdatafile.split(','))==2:
			self.userdata = userdatafile.split(',')	
		else:
			sys.exit('wrong input of userdata')
	def shebao_rate(self,config_class):
		self.shebao_kind = ['YangLao','YiLiao','ShiYe','GongShang','ShengYu','GongJiJin']
		self.shebao_rates=0
		try:
			for self.each_shebao in self.shebao_kind:
				self.shebao_rates += float(config_class.get_config(self.each_shebao))
			return self.shebao_rates
		except:
			sys.exit('wrong config value')
	def com_salary(self,salary,config_class):
		try:
			if float(salary) < float(config_class.get_config('JiShuL')):
				return float(config_class.get_config('JiShuL'))
			elif float(salary) > float(config_class.get_config('JiShuH')):
				return float(config_class.get_config('JiShuH'))
			else:
				return float(salary)
		except:
			sys.exit('wrong JiShu')
	def calculator(self,config_class):
		try:
			self.each_one_list = []
			self.salary = int(float(self.userdata[1]))
			self.salary_com = self.com_salary(self.salary,config_class)
			self.shebao = float(self.shebao_rate(config_class))*self.salary_com
			self.salary_new = self.salary - 3500 - self.shebao
			if self.salary_new <= 0:
				self.fax = 0
			elif self.salary_new <= 1500:
				self.fax = self.salary_new * 0.03
			elif self.salary_new <= 4500:
				self.fax = self.salary_new * 0.1 - 105
			elif self.salary_new <= 9000:
				self.fax = self.salary_new * 0.2 - 555
			elif self.salary_new <= 35000:
				self.fax = self.salary_new * 0.25 - 1005
			elif self.salary_new <= 55000:
				self.fax = self.salary_new * 0.3 - 2755
			elif self.salary_new <= 80000:
				self.fax = self.salary_new * 0.35 - 5505
			else:
				self.fax = self.salary_new * 0.45 - 13505
			self.salary_final = float(self.salary) - self.shebao - self.fax
			self.each_one_list.append(self.userdata[0])
			self.each_one_list.append(int(self.salary))
			self.each_one_list.append(format(float(self.shebao),'.2f'))
			self.each_one_list.append(format(float(self.fax),'.2f'))
			self.each_one_list.append(format(float(self.salary_final),'.2f'))
		except:
			sys.exit('Parameter wrong')
	def dumptofile(self,outputfile,time):
		with open(outputfile,'a') as output_file:
			output_file.write(str(self.each_one_list[0])+','+str(self.each_one_list[1])+','+str(self.each_one_list[2])+','+str(self.each_one_list[3])+','+str(self.each_one_list[4])+','+str(time)+'\n')

def worker(user_data):
	persondata=UserData(user_data)
	queue1.put(persondata)
def cal(config_class):
	person_class=queue1.get()
	person_class.calculator(config)
	queue2.put(person_class)
def output(outputfile):
	per_class=queue2.get()
	now_time=datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S')
	per_class.dumptofile(outputfile,now_time)
def usage():
	print('Usage: calculator.py -C cityname -c configfile -d userdata -o resultdata')
	sys.exit(1)
try:
	city='DEFAULT'
	opts,args = getopt.getopt(sys.argv[1:],"hC:o:c:d:",["help"]); 
	opt_list=[]
	for opt,arg in opts:
		
		if opt in ('-h','--help'):
			usage()
		elif opt == '-c':
			configfile = arg
		elif opt == '-d':
			userdatafile = arg
		elif opt == '-o':
			outputfile = arg
		elif opt == '-C':
			city = arg
		else:
			sys.exit('wrong option')
		opt_list.append(opt)
	if '-c' not in opt_list or '-d' not in opt_list or '-o' not in opt_list:
		sys.exit('need option')
	else:
		pass
except getopt.GetoptError:
	sys.exit('this option need value')

if os.path.isfile(configfile):
	try:
		city = city.upper()
	except:
		sys.exit('wrong city name')
	config = Config(configfile,city)
else:
	sys.exit('no exist configfile')

userdata_list=[]

if os.path.isfile(userdatafile):
	with open(userdatafile) as userdata_file:
		for each_user_line in userdata_file:
			p1 = Process(target=worker,args=(each_user_line,))
			p1.start()
			p2 = Process(target=cal,args=(config,))
			p2.start()
			p3= Process(target=output,args=(outputfile,))
			p3.start()
else:
	sys,exit('no exist userdatafile')

