import traceback

# def func():
#     try:
#         i = 123
#         for i in range(10):
#             pass
#         int('asdfasdf')
#     except Exception as e:
#         print(traceback.format_exc())
#
# func()


# 100任务
import time
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor

def task(i):
    time.sleep(1)
    print(i)

p = ThreadPoolExecutor(10)
for row in range(100):
    p.submit(task,row)















