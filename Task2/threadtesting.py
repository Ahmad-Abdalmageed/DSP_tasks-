import threading
import os


# def print_cube(num):
#     """
#     function to print cube of given num
#     """
#     print("Cube: {}".format(num * num * num))
#
#
# def print_square(num):
#     """
#     function to print square of given num
#     """
#     print("Square: {}".format(num * num))
#
#
# if __name__ == "__main__":
#     # creating thread
#     t1 = threading.Thread(target=print_square, args=(10,))
#     t2 = threading.Thread(target=print_cube, args=(10,))
#
#     # starting thread 1
#     t1.start()
#     # starting thread 2
#     t2.start()
#
#     # wait until thread 1 is completely executed
#     t1.join()
#     # wait until thread 2 is completely executed
#     t2.join()
#
#     # both threads completely executed
#     print("Done!")
import time

exitFlag = 0

class myThread (threading.Thread):
   def __init__(self, threadID, name, counter, runnable):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
      self.runnable = runnable

   def run(self):
      print ("Starting " + self.name)
      self.runnable(self.name, 5, self.counter)
      # print_time(self.name, 5, self.counter)
      print ("Exiting " + self.name)





def print_time(threadName, counter, delay):
   while counter:
      if exitFlag:
         threadName.exit()
      time.sleep(delay)
      print ("%s: %s" % (threadName, time.ctime(time.time())))
      counter -= 1

# Create new threads
# t1 = threading.Thread(target=print_time, args=("Thread-1", 1,1), daemon=True)

thread1 = myThread(1, "Thread-1", 1, print_time)
thread2 = myThread(2, "Thread-2", 2, print_time)

# Start new Threads
thread1.start()
thread2.start()
print ("Exiting Main Thread")
# global variable x
# x = 0
#
#
# def increment():
#     """
#     function to increment global variable x
#     """
#     global x
#     x += 1
#
#
# def thread_task():
#     """
#     task for thread
#     calls increment function 100000 times.
#     """
#     for _ in range(100000):
#         increment()
#
#
# def main_task():
#     global x
#     # setting global variable x as 0
#     x = 0
#
#     # creating threads
#     t1 = threading.Thread(target=thread_task)
#     t2 = threading.Thread(target=thread_task)
#
#     # start threads
#     t1.start()
#     t2.start()
#
#     # wait until threads finish their job
#     t1.join()
#     t2.join()
#
#
# if __name__ == "__main__":
#     for i in range(10):
#         main_task()
#         print("Iteration {0}: x = {1}".format(i, x))
