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
			_calc(self)
		else:
			print('计时未开始，请先start()')
	def _calc(self):
		self.kind=['年','月','天','小时','分钟','秒']
		for index in range(6):
			self.count.append(int(self.end[index])-int(self.begin[index]))
			self.result+=str(self.count[index])+self.kind[index]
	def __str__(self):
		return self.result
	__repr__=__str__
