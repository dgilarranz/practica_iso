from app.gui.money_frame import MoneyFrame
import toga
from functools import reduce
from unittest.mock import patch

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

    from_box = None
    for box in mf.content.children:
        if box.children[0].text == "From Address:":
            from_box = box
            break

    assert from_box is not None

def test_init_adds_to_content_private_key_box():
    mf = MoneyFrame()
    
    key_box = None
    for box in mf.content.children:
        if box.children[0].text == "Private Key:":
            key_box = box
            break

    assert key_box is not None

def test_init_adds_to_content_token_address_box():
    mf = MoneyFrame()
    
    token_box = None
    for box in mf.content.children:
        if box.children[0].text == "Token Address:":
            token_box = box
            break

    assert token_box is not None


def test_init_adds_to_content_eth_ammount_box():
    mf = MoneyFrame()
    
    eth_box = None
    for box in mf.content.children:
        if box.children[0].text == "Eth Ammount:":
            eth_box = box
            break

    assert eth_box is not None

def test_init_adds_to_content_to_address_box():
    mf = MoneyFrame()
    
    to_box = None
    for box in mf.content.children:
        if box.children[0].text == "To Address:":
            to_box = box
            break

    assert to_box is not None

def test_last_children_is_send_button():
    mf = MoneyFrame()
    last_child = mf.content.children[-1]
    assert isinstance(last_child, toga.Button)

def test_button_text_is_send():
    mf = MoneyFrame()
    send_button = mf.content.children[-1]
    assert send_button.text == "Send"

def test_send_money_calls_contract():
    from_address = "Sender"
    private_key = "Key"
    token_address = "Token"
    eth_ammount = "5"
    to_address = "Receiver"

    mf = MoneyFrame()
    mf.from_box.children[1].value = from_address
    mf.key_box.children[1].value = private_key
    mf.token_box.children[1].value = token_address
    mf.eth_box.children[1].value = eth_ammount
    mf.to_box.children[1].value = to_address

    with patch("app.erc20andEthSender.MoneyContract.__init__") as mock_contract:
        mock_contract.return_value = None
        mf.send_money(None)
        mock_contract.assert_called_once_with(
            from_address,
            private_key,
            token_address,
            int(eth_ammount),
            to_address
        )

def test_send_money_calls_contract_with_different_data():
    from_address = "Another Sender"
    private_key = "Another Key"
    token_address = "Another Token"
    eth_ammount = "7"
    to_address = "Another Receiver"

    mf = MoneyFrame()
    mf.from_box.children[1].value = from_address
    mf.key_box.children[1].value = private_key
    mf.token_box.children[1].value = token_address
    mf.eth_box.children[1].value = eth_ammount
    mf.to_box.children[1].value = to_address

    with patch("app.erc20andEthSender.MoneyContract.__init__") as mock_contract:
        mock_contract.return_value = None
        mf.send_money(None)
        mock_contract.assert_called_once_with(
            from_address,
            private_key,
            token_address,
            float(eth_ammount),
            to_address
        )        