from scheduler import Scheduler

def my_func():
    print('hello world')

def main():
    s = Scheduler()
    s.schedule_task(my_func, 1)
    return

main()