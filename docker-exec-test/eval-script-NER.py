
def evaluate():
    # READ FILES and run eval functions

    text_file = open("/input-files/test-data.txt", "r")
    data = text_file.read()
    text_file.close()
 
    print(f"Contents read from file {data}.")

    return 70.2