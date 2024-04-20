import logging

from pbcgui.utility import StructuredMessage


def test_structured_message():
    msg = StructuredMessage(**{"key": "value"})
    logging.debug(msg)
    logging.debug(dir(msg))

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(message)s')
    test_structured_message()
    logging.info("Structured message test passed")