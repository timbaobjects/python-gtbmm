import os
from gtbmm import GTBMobileMoney
from gtbmm.exceptions import EXCEPTIONS_MAP
import pytest


def test_auth():
    # Test proper authentication
    mm = GTBMobileMoney(os.environ['GTB_ACCOUNT'], os.environ['GTB_PIN'])
    assert mm.auth() is True

    # Test Incorrect Pin
    with pytest.raises(EXCEPTIONS_MAP['29']) as exc:
        mm.auth(os.environ['GTB_ACCOUNT'], '0000')
    assert exc.value.message == 'Incorrect PIN'

    # Test Invalid Account
    with pytest.raises(EXCEPTIONS_MAP['11']) as exc:
        mm.auth('1111', '1111')
    assert exc.value.message == 'Invalid Account'


def test_balance():
    mm = GTBMobileMoney(os.environ['GTB_ACCOUNT'], os.environ['GTB_PIN'])
    response = mm.balance()
    assert response.get('balance') >= 0


def test_history():
    mm = GTBMobileMoney(os.environ['GTB_ACCOUNT'], os.environ['GTB_PIN'])
    history = list(mm.history())
    assert len(history) > 0


def test_send():
    mm = GTBMobileMoney(os.environ['GTB_ACCOUNT'], os.environ['GTB_PIN'])

    # Test sending an invalid amount
    with pytest.raises(EXCEPTIONS_MAP['212']):
        mm._beforeSend(os.environ['GTB_DST_ACCOUNT'], 0)

    # Test sending to an invalid destination account
    with pytest.raises(EXCEPTIONS_MAP['2020']):
        mm._beforeSend('08012345', '10')

    # Test sending to an inactive destination account
    with pytest.raises(EXCEPTIONS_MAP['128']):
        mm._beforeSend('08012345678', '10')

    # Test sending to an incorrect destination account
    with pytest.raises(EXCEPTIONS_MAP['687']):
        mm._beforeSend('08033333333', '10')

    # Test sending less than the minimum amount
    with pytest.raises(EXCEPTIONS_MAP['107']):
        mm._beforeSend(os.environ['GTB_DST_ACCOUNT'], '1')

    # Test sending with insufficient balance
    with pytest.raises(EXCEPTIONS_MAP['16']):
        mm._beforeSend(os.environ['GTB_DST_ACCOUNT'], '999')

    # Test sending with more than maximum allowed
    with pytest.raises(EXCEPTIONS_MAP['106']):
        mm._beforeSend(os.environ['GTB_DST_ACCOUNT'], '100000')

    # Test sending to self
    with pytest.raises(EXCEPTIONS_MAP['295']):
        mm._beforeSend(os.environ['GTB_ACCOUNT'], '50')
