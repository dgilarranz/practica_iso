class Observer:
    def update():
        pass

class Subject:
    def __init__(self):
        self.subscribers = set()

    def subscribe(self, observer: Observer):
        if isinstance(observer, int):
            raise SubscriberIsNotObserverException
        self.subscribers.add(observer)

class SubscriberIsNotObserverException(Exception):
    pass