import struct

def build_rrq(filename, mode):
    opcode = 1
    return build_request_packet(filename, mode, opcode)


def build_wrq(filename, mode):
    opcode = 2
    return build_request_packet(filename, mode, opcode)


def build_request_packet(filename, mode, opcode):
    packet = bytearray()

    packet.append(0)
    packet.append(opcode)

    filename = bytearray(filename.encode('utf-8'))
    packet += filename

    packet.append(0)

    form = bytearray(mode.encode('utf-8'))
    packet += form

    packet.append(0)

    return packet


def build_ack(byte1, byte2):
    ack = bytearray()
    ack.append(0)
    ack.append(4)
    ack.append(byte1)
    ack.append(byte2)
    return ack


def build_data(block, data):
    opcode = 3
    block = int.from_bytes(block, "big")
    data_length = str(len(data))
    format_string = '!HH' + data_length + 's'
    data = bytes(data, 'utf-8')
    packet = struct.pack(format_string, opcode, block, data)
    return packet


def build_error(error_code, error_msg):
    packet = bytearray()
    opcode = 5

    packet.append(0)
    packet.append(opcode)

    packet.append(0)
    packet.append(error_code)

    error_msg = bytearray(error_msg.encode('utf-8'))
    packet += error_msg

    packet.append(0)

    return packet
