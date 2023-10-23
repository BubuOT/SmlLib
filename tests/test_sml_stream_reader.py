import binascii

import pytest

from smllib.reader import CrcError, SmlStreamReader


def test_strip_start():
    r = SmlStreamReader()
    r.add(b'asdfasdfasdf\x1B\x1B\x1B\x1B\x01\x01\x01\x01')
    assert r.get_frame() is None
    assert r.bytes == b'\x1B\x1B\x1B\x1B\x01\x01\x01\x01'


def test_skip_escape():
    r = SmlStreamReader()
    msg = b'\x1B\x1B\x1B\x1B\x01\x01\x01\x01\x1B\x1B\x1B\x1B\x1B\x1B\x1B\x1B\x1A\x00\x00\x00'
    r.add(msg)
    assert r.get_frame() is None
    assert r.bytes == msg


def test_exception():
    r = SmlStreamReader()
    msg = b'\x1B\x1B\x1B\x1B\x01\x01\x01\x01\x1B\x1B\x1B\x1B\x1A\x00\x00\x00'
    r.add(msg)
    with pytest.raises(CrcError) as e:
        r.get_frame()
    assert repr(e.value) == '<CrcError msg: 0000 calc: c6e5>'


def test_msg_long_list():
    msg2 = binascii.a2b_hex(
        '1b1b1b1b01010101'
        '76040000016200620072650000010176010107000002dba23c0b0a01484c5902000424a0010163945b00'
        # This frame contains a long list (f104)
        '76040000026200620072650000070177010b0a01484c5902000424a00101f10477070100603201010101010104484c590177070100600100ff010101010b0a01484c5902000424a00177070100010800ff65001c81046502dba23d621e52ff6502aea1320177070100020800ff65001c81046502dba23d621e52ff62000177070100100700ff0101621b52005300890177070100200700ff0101622352ff6309280177070100340700ff0101622352ff6309290177070100480700ff0101622352ff63092201770701001f0700ff0101622152fe62290177070100330700ff0101622152fe624e0177070100470700ff0101622152fe622e0177070100510701ff01016208520062f00177070100510702ff01016208520062780177070100510704ff010162085200630110017707010051070fff010162085200630138017707010051071aff01016208520063011101770701000e0700ff0101622c52ff6301f40177070100000200000101010109312e30322e3030370177070100605a02010101010105413031410177070100600500ff0101010165001c810401010163fc1e00'  # noqa: E501
        '760400000362006200726500000201710163e82300'
        '00001b1b1b1b1a0222ed'
    )

    r = SmlStreamReader()
    r.add(msg2)
    frame = r.get_frame()
    for msg in frame.parse_frame():
        msg.format_msg()
