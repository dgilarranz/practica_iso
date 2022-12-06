from app.gui.money_frame import MoneyFrame
import toga
from functools import reduce

def test_money_frame_is_toga_window():
    assert isinstance(MoneyFrame(), toga.Window)

def test_create_box_creates_box_with_supplied_string_as_label():
    mf = MoneyFrame()
    text = "Prueba"
    box = mf.create_box(text)
    label = list(
        filter(
            lambda c: isinstance(c, toga.Label),
            box.children
        )
    )[0]
    assert label.text == text

def test_create_box_creates_box_with_another_string_as_label():
    mf = MoneyFrame()
    text = "String diferente"
    box = mf.create_box(text)
    label = list(
        filter(
            lambda c: isinstance(c, toga.Label),
            box.children
        )
    )[0]
    assert label.text == text

def test_create_box_also_creates_an_input():
    mf = MoneyFrame()
    box = mf.create_box("Prueba")
    text_input = list(
        filter(
            lambda c: isinstance(c, toga.TextInput),
            box.children
        )
    )[0]
    assert text_input is not None

def test_create_box_only_has_two_children():
    mf = MoneyFrame()
    box = mf.create_box("Prueba")
    assert len(box.children) == 2

def test_init_adds_to_content_from_address_box():
    mf = MoneyFrame()
    box = reduce(
        lambda box, current: current if current.children[0].text == "From Address:" else box,
        mf.content.children
    )
    assert box is not None
