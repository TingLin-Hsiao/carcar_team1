import logging
from typing import Optional
import time
import threading

from BT import Bluetooth
from score import ScoreboardServer, ScoreboardFake

log = logging.getLogger(__name__)

# hint: You may design additional functions to execute the input command,
# which will be helpful when debugging :)


class BTInterface:
    def __init__(self, port: Optional[str] = None):
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
    
    def start(self):
        input("Press enter to start.")
        self.bt.serial_write_string("s")

    def get_UID(self):
        """Read and return the UID from Arduino (if available)."""
        uid = self.bt.serial_read_byte()
        uid = str(uid)
        uid=uid.upper()
        uid = uid.replace("0X","")
        
        # if uid != "0" and uid != "596573":
        if len(uid) == 8:
            print(f"Received UID: {uid}")
            return uid
        return None
    
    def listen_for_uid(self):
        """Continuously listen for UID messages from Arduino."""
        while self.listening:
            uid = self.get_UID()
            if uid:
                log.info(uid)
            time.sleep(0.5)  # Avoid excessive CPU usage

    def get_Node(self):
        arrive = self.bt.serial_read_byte()
        arrive = str(arrive)
        arrive = arrive.upper()
        arrive = arrive.replace("0X","")
        # print(arrive)
        if arrive == "FC":
            print("Arrived Node")
            return arrive
        return None

    def send_action(self, dirc):
        valid_commands = {"F", "B", "L", "R", "S"}  # Define allowed commands
        for i in dirc:
            if i in valid_commands:
                self.bt.serial_write_string(i)
                log.info(f"Sent action: {i}")
                # print(f'commmand: {i}\n')
                
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
