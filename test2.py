from time import sleep
from threading import Thread


class Eblan:

    def __init__(self) -> None:
        self.a = [1, 2, 3, 4, 5]

    def start_polling(self):
        print("starting to poll")
        sleep(10)

    def do_it(self):
        print("Doing it", self.a)

    def __del__(self):
        self.do_it()


eb = Eblan()
# eb.start_polling()
thr = Thread(target=eb.start_polling).start()
for i in range(10):
    print(i)
