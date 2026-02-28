import datetime
now = datetime.datetime.now()
def fivedaysubstract():
    x = now
    x = x.replace(day=x.day - 5)
    print(x)


def threedays():
    yesterday = now - datetime.timedelta(days=1)
    tommorow = now + datetime.timedelta(days=1)
    print(f"yesterday: {yesterday}")
    print(f"today: {now}")
    print(f"tommorow: {tommorow}")

def microseconds():
    print(f"microseconds: {now.microsecond}")

def difference(x, y):
    difference = (x - y).total_seconds()*1000000
    print(f"difference: {difference} seconds")
difference(datetime.datetime(2024, 6, 1), datetime.datetime(2024, 5, 25))