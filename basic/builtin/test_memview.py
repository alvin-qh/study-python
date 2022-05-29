

    data = bytearray(b"abcdef")

    mv = memoryview(data)
    assert mv[0] == 97
    assert mv[1] == 98
    assert mv[0:6] == ""
