import time
import serial
from tofupilot.v2 import TofuPilot

class MCUController:
    """Instrument plug for managing UART communication with the MCU."""
    def __init__(self, port="COM3", baudrate=115200, timeout=1.0):
        self.ser = serial.Serial(port, baudrate, timeout=timeout)
        time.sleep(0.5)  # Allow connection to settle
    def send_and_get_response(self, command: str) -> str:
        self.ser.reset_input_buffer()
        self.ser.write(command.encode('ascii'))
        time.sleep(0.2)  # Give MCU time to process and reply
        raw_data = self.ser.read_all()
        response = raw_data.decode('ascii', errors='ignore')
        return response.strip()
    def close(self):
        if self.ser.is_open:
            self.ser.close()
if __name__ == "__main__":
    controller = MCUController()
    try:
        print("Sending LEDON...")
        resp_on = controller.send_and_get_response("LEDON\n")
        print(f"MCU Response: {resp_on}")
        
        print("Sending LEDOFF...")
        resp_off = controller.send_and_get_response("LEDOFF\n")
        print(f"MCU Response: {resp_off}")
    finally:
        controller.close()