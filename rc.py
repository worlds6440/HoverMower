import serial
import time
from approxeng.input.selectbinder import ControllerResource
from struct import *
import ctypes

HOVER_SERIAL_BAUD = 115200
START_FRAME = 0xABCD
TIME_SEND = 0.1  # 100ms
SPEED_MAX_TEST = 300


def Send(serial_port, uSteer, uSpeed):
    """ Create command structure ans send via uart serial
        Note: The Steer and Speed are int16_t """
    start_frame = 43981
    checksum = ctypes.c_uint16(start_frame ^ uSteer ^ uSpeed)

    # Create byte string combining all the segments
    # byte_string = start_frame.to_bytes(2, 'little', signed=False) +\
    #     uSteer.to_bytes(2, 'little', signed=True) +\
    #     uSpeed.to_bytes(2, 'little', signed=True) +\
    #     checksum.to_bytes(2, 'little', signed=False)

    # message = ((start_frame, False), (uSteer, True), (uSpeed, True), (checksum, False))
    # byte_string = b''.join([_[0].to_bytes(2, 'little', signed=_[1]) for _ in message])

    byte_string = pack('<HhhH', start_frame, uSteer, uSpeed, checksum.value)

    # Write to Serial
    print(f"uSteer[{uSteer}], uSpeed[{uSpeed}]\n")
    port.write(byte_string)


def map_value(nFrom, nTo, nFrom2, nTo2, nValue):
    """ Map a value from one range to another. """
    if nValue <= nFrom2:
        return nFrom
    elif nValue >= nTo2:
        return nTo
    return float(nTo - nFrom) * (float(nValue - nFrom2) / float(nTo2 - nFrom2)) + nFrom


# Create a serial port over UART
port = serial.Serial("/dev/ttyS0", baudrate=HOVER_SERIAL_BAUD, timeout=1.0)
while True:

    try:
        with ControllerResource() as joystick:
            print('Found a joystick and connected')
            while joystick.connected:
                # Do stuff with your joystick here!

                # Get a corrected value for the left stick x-axis
                ly, rx = joystick['ly','rx']

                speed = int(map_value(-300, 300, -1.0, 1.0, ly))
                steering = int(map_value(-300, 300, -1.0, 1.0, rx))

                # Send the values to the hoverboard
                Send(port, steering, speed)
                time.sleep(TIME_SEND)

        # Joystick disconnected...
        print('Connection to joystick lost')
        Send(port, 0, 0)  # Stop motors
    except IOError:
        # No joystick found, wait for a bit before trying again
        print('Unable to find any joysticks')
        sleep(1.0)
