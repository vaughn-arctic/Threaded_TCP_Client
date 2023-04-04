import os.path

def read_in(data, filename):
    if len(data) < 1:
        with open(filename, "ba") as file_object:
            file_object.close()
    else:
        with open(filename, "ba") as file_object:
            file_object.write(data)

    file_object.close()
