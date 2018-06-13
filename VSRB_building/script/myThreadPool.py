import sys
from Queue import Queue
from threading import Thread
import threading

class Worker(Thread):
	""" Thread executing tasks from a given tasks queue """
	def __init__(self, tasks, rsQueue):
		Thread.__init__(self)
		self.tasks = tasks
		self.rsQueue = rsQueue
		self.daemon = True
		self.start()
	def run(self):
		while True:
			command, func, args, kargs = self.tasks.get()
			if command == 'stop':
				break
			try:
				self.rsQueue.put(func(*args, **kargs))
			except Exception as e:
				print (e)
			finally:
				self.tasks.task_done()
	def dismiss(self):
		command = 'stop'
		self.tasks.put((command, None, None, None))

class ThreadPool:
	""" Pool of threads consuming tasks from a queue """
	def __init__(self, num_threads, size=0):
		self.tasks = Queue(num_threads)
		self.rsQueue = Queue(size) #equals 0 means infinite...
		self.workers = {}
		for i in range(num_threads):
			self.workers[i] = Worker(self.tasks, self.rsQueue)
	def add_task(self, func, *args, **kargs):
		""" Add a task to the queue """
		command = 'process'
		self.tasks.put((command, func, args, kargs))
	def map(self, func, args_list):
		""" Add a list of tasks to the queue """
		for args in args_list:
			self.add_task(func, args)
	def destory(self):
		# first, request all threads to stop...
		for i in self.workers:
			self.workers[i].dismiss()
		# then, wait for each of them to terminate..
		for i in self.workers:
			self.workers[i].join()
		# clean up the workers from now-unused thread objects
		del self.workers

