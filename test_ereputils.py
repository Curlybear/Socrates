from ereputils import ErepUtils as Utils


def test_is_number_text():
    assert not Utils.is_number("Test")


def test_is_number_text_number():
    assert Utils.is_number("5.6")


def test_is_number_number():
    assert Utils.is_number(15.5)