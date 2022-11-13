from app.observer import Observer, Subject

def test_observer_hash_notify_method():
    assert callable(Observer.update)