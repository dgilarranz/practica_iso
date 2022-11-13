class Observer:
    def update():
        pass

class Subject:
    def __init__(self):
        self.subscribers = set()

    def subscribe(self, observer: Observer):
        if not isinstance(observer, Observer):
            raise SubscriberIsNotObserverException
        self.subscribers.add(observer)
    
    def unsubscribe(self, observer: Observer):
        self.subscribers.remove(observer)
    
    def notify(self):
        for sub in self.subscribers:
            sub.update()

class SubscriberIsNotObserverException(Exception):
    pass