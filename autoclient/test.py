import traceback

def func():
    try:
        i = 123
        for i in range(10):
            pass
        int('asdfasdf')
    except Exception as e:
        print(traceback.format_exc())

func()