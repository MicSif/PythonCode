import time
class Clock:
	def __init__(self):
		self.result='未开始计时'
		self.begin=0
		self.end=0
		self.count=[]
	def start(self):
		self.begin=time.perf_counter()
		print('计时开始')
	def stop(self):
		if self.begin:
			self.end=time.perf_counter()
			print('计时结束')
			self._calc()
		else:
			print('计时未开始，请先start()')
	def _calc(self):
		self.kind=['秒','分钟','小时','天','月','年']
		self.date=['60','60','24','31','12','0']
		self.middle=[]
		self.result='计时总共'
		self.count = self.end - self.begin
		self.count=round(self.count,3)
		for index in range(5):
			self.middle.append(self.count%int(self.date[index]))
			self.count//=int(self.date[index])
			self.count=int(self.count)
		for index in range(4,-1,-1):
			if self.middle[index]:
				self.result+=str(self.middle[index])+self.kind[index]
		self.begin=0
		self.end=0
	def __str__(self):
		return self.result
	__repr__=__str__
t=Clock()
a=600000000
t.start()
while a>0:
	a-=1
t.stop()
print(t)

