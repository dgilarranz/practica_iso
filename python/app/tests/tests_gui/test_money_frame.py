from app.gui.money_frame import MoneyFrame
import toga

def test_money_frame_is_toga_window():
    assert isinstance(MoneyFrame(), toga.Window)