from readinfile import read_in

def unpack_DATA(filename, packet):
    opcode = packet[1]
    block = packet[2:4]
    j = 4
    data = bytearray()

    # Stripping the leading path from the filename
    for i in range(len(filename) - 1, 0, -1):
        # print(filename[i], " != ", '/')
        if filename[i] == "/":
            x = i
            filename = filename[x + 1:]
            # print("Stripped filename: ", filename)
            break

    if len(packet) < 5:
        with open(filename, "ba") as file_object:
            file_object.close()
    else:
        while j < len(packet):
            data.append(packet[j])
            j += 1

        with open(filename, "ba") as file_object:
            file_object.write(data)

    file_object.close()

    return opcode, block


def unpack_ACK(packet):
    block = packet[2:4]
    return block


def unpack_ERROR(packet):
    error_code = packet[2:4]
    error_msg = str(packet[4:len(packet)-1])
    return error_code, error_msg


def unpack_RRQ_WRQ(packet):
    # print("Deconstructing request packet")
    opcode = packet[1]
    for i in range(len(packet[2:])):
        if packet[2 + i] == 0:  # Loop to find index of end of filename
            x = i
            break
    filename = packet[2:(x+2)]
    print(filename.decode("utf-8"))
    return filename.decode("utf-8")