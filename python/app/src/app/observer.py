class Observer:
    def update():
        pass

class Subject:
    def __init__(self):
        self.subscribers = set()

    def subscribe(self, observer: Observer):
        self.subscribers.add(observer)
        