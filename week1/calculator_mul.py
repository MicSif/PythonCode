#!/usr/bin/env python3
import sys,os.path
from multiprocessing import Process,Queue
queue1=Queue()
queue2=Queue()
class Config:
	def __init__(self,configfile):
		self._config = {}
		self.config_list = []
		for self.eachline in configfile:
			if len(self.eachline.split('='))==2:
				self.config_list = self.eachline.split('=')
				self._config[self.config_list[0].strip()] = self.config_list[1].strip()
			else:
				sys.exit('wrong input of config value')
	def get_config(self,value):
		try:
			return self._config[value]
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
	def dumptofile(self,outputfile):
		with open(outputfile,'a') as output_file:
			output_file.write(str(self.each_one_list[0])+','+str(self.each_one_list[1])+','+str(self.each_one_list[2])+','+str(self.each_one_list[3])+','+str(self.each_one_list[4])+'\n')

def worker(user_data):
	persondata=UserData(user_data)
	queue1.put(persondata)
def cal(config_class):
	person_class=queue1.get()
	person_class.calculator(config)
	queue2.put(person_class)
def output(outputfile):
	per_class=queue2.get()
	per_class.dumptofile(outputfile)
args=sys.argv[1:]
if len(args) == 6:
	index_c = args.index('-c')
	configfile = args[index_c+1]
	index_d = args.index('-d')
	userdatafile = args[index_d+1]
	index_o = args.index('-o')
	outputfile = args[index_o+1]
else:
	sys.exit('Parameter Error')
config_list=[]
userdata_list=[]
if os.path.isfile(configfile):
	with open(configfile) as config_file:
		for each_config_line in config_file:
			config_list.append(each_config_line)
else:
	sys.exit('no exist configfile')

config = Config(config_list)

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

