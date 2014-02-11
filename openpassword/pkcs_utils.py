from math import fmod


def byte_pad(input_bytes, length=8):
    if length > 256:
        raise ValueError("Maximum padding length is 256")

    # Modulo input bytes length with padding length to see how many bytes to pad with
    bytes_to_pad = length - int(fmod(len(input_bytes), length))

    if bytes_to_pad == length:
        bytes_to_pad = 0

    # Pad input bytes with a sequence of bytes containing the number of padded bytes
    input_bytes += bytes([bytes_to_pad] * bytes_to_pad)

    return input_bytes


def strip_byte_padding(input_bytes, length=8):
    if fmod(len(input_bytes), length) != 0:
        raise ValueError("Input byte length is not divisible by %s " % length)

    # Get the last {length} bytes of the input bytes, reversed
    if len(input_bytes) == length:
        byte_block = bytes(input_bytes[::-1])
    else:
        byte_block = bytes(input_bytes[:length:-1])

    # If input bytes is padded, the padding is equal to byte value of the number
    # of bytes padded. So we can read the padding value from the last byte..
    padding_byte = byte_block[0:1]

    for i in range(1, ord(padding_byte.decode())):
        if byte_block[i:i+1] != padding_byte:
            return input_bytes

    return input_bytes[0:-ord(padding_byte.decode())]
