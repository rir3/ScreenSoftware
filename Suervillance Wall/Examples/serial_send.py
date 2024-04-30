import serial

def send_message(ser):
    while True:
        message = input("Enter message to send (or 'exit' to quit): ").strip()
        if message.lower() == 'exit':
            break
        ser.write(message.encode())
        print("Message sent.")

if __name__ == "__main__":
    port_name = input("Enter the serial port name (e.g., COM1, /dev/ttyUSB0): ").strip()
    baud_rate = int(input("Enter the baud rate: ").strip())

    try:
        # Establish serial connection
        ser = serial.Serial(port_name, baud_rate)
        print(f"Serial connection established on port {port_name} with baud rate {baud_rate}.")

        # Start sending messages
        send_message(ser)

    except serial.SerialException as e:
        print(f"Failed to open serial port: {e}")

    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Serial port closed.")
