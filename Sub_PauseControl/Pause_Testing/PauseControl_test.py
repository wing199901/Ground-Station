import time

from fsuipc import FSUIPC

# This python is used to Read the Pause Control signal only (for test)

with FSUIPC() as fsuipc:
    prepared = fsuipc.prepare_data([
        (0x264, "H"),  # Pause indicator (0=Not paused, 1=Paused)
    ], True)

    while True:
        PauseControl = prepared.read()
        print(f"PauseControl: {PauseControl}")
        time.sleep(500)

        # payload = {
        #     'Name': socket.gethostname(),
        # }
