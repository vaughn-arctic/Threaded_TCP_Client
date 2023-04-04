def read_out(filename):
    data_file = list()
    with open(filename, "r") as f:
        while True:
            data_chunk = f.read(512)
            if len(data_chunk) < 512:    # End of file / last data transmission
                data_file.append(data_chunk)
                f.close()
                break
            else:
                data_file.append(data_chunk)
    return data_file
