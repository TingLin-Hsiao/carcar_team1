import logging
from typing import Optional
import time
import threading

from BT import Bluetooth

log = logging.getLogger(__name__)

# hint: You may design additional functions to execute the input command,
# which will be helpful when debugging :)


class BTInterface:
    def __init__(self, scoreboard, port: Optional[str] = None):
        log.info("Arduino Bluetooth Connect Program.")
        self.bt = Bluetooth()
        if port is None:
            port = input("PC bluetooth port name: ")
        while not self.bt.do_connect(port):
            if port == "quit":
                self.bt.disconnect()
                quit()
            port = input("PC bluetooth port name: ")
        # Start listening for UIDs in a background thread
        self.listening = True
        self.listener_thread = threading.Thread(target=self.listen_for_uid, daemon=True)
        self.listener_thread.start()
        self.scoreboard = scoreboard
        
    def start(self):
        input("Press enter to start.")
        self.bt.serial_write_string("s")

    def get_UID(self):
        """Read and return the UID from Arduino (if available)."""
        uid = self.bt.serial_read_byte()
        if uid:
            print(f"Received UID: {f'{uid}'.upper()}")
            score, time_remaining = self.scoreboard.add_UID(f'{uid}'.upper())
            current_score = self.scoreboard.get_current_score()
            log.info(f"Score from UID: {score}, Time left: {time_remaining}")
            log.info(f"Current score: {current_score}")
        return None
    
    def listen_for_uid(self):
        """Continuously listen for UID messages from Arduino."""
        while self.listening:
            uid = self.get_UID()
            if uid:
                log.info(uid)
            time.sleep(0.5)  # Avoid excessive CPU usage

    def send_action(self, dirc):
        valid_commands = {"F", "B", "L", "R", "S"}  # Define allowed commands
        for i in dirc:
            if i in valid_commands:
                self.bt.serial_write_string(i)
                log.info(f"Sent action: {i}")
                print(f'commmand: {i}\n')
                
            else:
                log.error(f"Invalid action: {dirc}")
        return 

    def end_process(self):
        self.bt.serial_write_string("e")
        self.listening = False
        self.bt.disconnect()


if __name__ == "__main__":
    test = BTInterface()
    test.start()
    test.end_process()
