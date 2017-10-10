import time
class Clock:
	def __init__(self):
		self.result='未开始计时'
		self.begin=0
		self.end=0
		self.count=[]
	def start(self):
		self.begin=time.localtime()
		print('计时开始')
	def stop(self):
		if self.begin:
			self.end=time.localtime()
			print('计时结束')
			self._calc()
		else:
			print('计时未开始，请先start()')
	def _calc(self):
		self.kind=['年','月','天','小时','分钟','秒']
		self.result='计时总共'
		for index in range(6):
			self.count.append(int(self.end[index])-int(self.begin[index]))
			if self.count[index]:
				self.result+=str(self.count[index])+self.kind[index]
		self.begin=0
		self.end=0
	def __str__(self):
		return self.result
	__repr__=__str__
t=Clock()
a=40000000
t.start()
while a>0:
	a-=1
t.stop()
print(t)
print('hello world')
