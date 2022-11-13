class Observer:
    def update():
        pass

class Subject:
    def __init__(self) -> None:
        self.subscribers = set()
        