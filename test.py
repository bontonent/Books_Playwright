import multiprocessing
import time
import random


def time_sleep(element):
    if element == "Error":
        time.sleep(1)
        i = i
        print("Error")

    time_sec = random.randint(0,3)
    time.sleep(time_sec)

i = 0;p = []

p.append(multiprocessing.Process(target = time_sleep, args = (None,)))
p.append(multiprocessing.Process(target = time_sleep, args = ("Error",)))
p.append(multiprocessing.Process(target = time_sleep, args = (None,)))

for process in p:
    process.start()
for process in p:
    process.join()
print("End process")