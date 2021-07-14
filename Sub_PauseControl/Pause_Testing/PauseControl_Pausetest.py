import time

from fsuipc import FSUIPC

# This python is used to Read the Pause Control signal only (for test)
while True:
    with FSUIPC() as fsuipc:

        Pause = input("P = Pause, U = Unpause:\n")
        if Pause == "P":
            try:
                fsuipc.write([(0x262, "H", 1)])
                print("Pause!!!")
            except Exception as e:
                print(e)

        elif Pause == "U":
            try:
                fsuipc.write([(0x262, "H", 0)])
                print("UnPause!!!")
            except Exception as e:
                print(e)

        else:
            print("Invalid input")

        # payload = {
        #     'Name': socket.gethostname(),
        # }
