from app.observer import Observer, Subject

def test_observer_hash_notify_method():
    assert callable(Observer.update)

def test_subject_hash_observer_list():
    s: Subject = Subject()
    assert type(s.subscribers) is set

def test_subscribe_observer():
    o = Observer()
    s = Subject()
    s.subscribe(o)

    assert o in s.subscribers