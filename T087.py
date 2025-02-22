from machine import Pin, UART
import time

# Twilio credentials (REPLACE WITH SECURE STORAGE)
TWILIO_PHONE = "+18575784600"
RECIPIENT_PHONE = "+918056850946"

# SIM800L UART setup
gsm = UART(1, baudrate=9600, tx=17, rx=16)

# IR Receiver setup (Connected to ESP32 Pin 15)
ir_receiver = Pin(15, Pin.IN)

# Function to send SMS via Twilio API through SIM800L
def send_sms(message):
    print("Sending SMS...")
    gsm.write('AT+CMGF=1\r\n')  # Set SMS text mode
    time.sleep(1)
    gsm.write(f'AT+CMGS="{RECIPIENT_PHONE}"\r\n')
    time.sleep(1)
    gsm.write(message + "\x1A")  # Send SMS message
    time.sleep(3)
    print("SMS Sent!")

# Main loop to check IR data
while True:
    if ir_receiver.value() == 1:  # If IR signal detected
        print("IR Data Received!")

        # Simulating received values (decode IR data in real application)
        heart_rate = 65
        oxygen_level = 78
        altitude = 50
        object_detected = True

        # Condition checks for alerts
        if heart_rate < 70 or oxygen_level < 80:
            message = f"⚠️ ALERT: Low Heart Rate: {heart_rate} bpm, Oxygen Level: {oxygen_level}%"
            send_sms(message)
        
        if altitude < 100:
            message = f"⚠️ ALERT: Low Altitude Detected: {altitude}m"
            send_sms(message)

        if object_detected:
            message = f"⚠️ ALERT: Object Detected!"
            send_sms(message)

    time.sleep(2)




import machine
import time

# Define GPIO pins
TRIG = machine.Pin(2, machine.Pin.OUT)  # Trigger pin
ECHO = machine.Pin(4, machine.Pin.IN)   # Echo pin

def get_distance():
    """Measure distance using the HC-SR04 ultrasonic sensor"""
    
    # Ensure trigger is LOW
    TRIG.value(0)
    time.sleep_us(2)

    # Send 10µs pulse to trigger
    TRIG.value(1)
    time.sleep_us(10)
    TRIG.value(0)

    # Measure the duration of the echo pulse
    pulse_duration = machine.time_pulse_us(ECHO, 1, 30000)  # Max 30ms timeout
    
    if pulse_duration < 0:
        return None  # Return None if the reading is invalid

    # Convert time (microseconds) to distance (cm)
    distance = (pulse_duration * 0.0343) / 2
    return distance

# Main loop
while True:
    distance = get_distance()
    
    if distance is not None:
        print(f"Distance: {distance:.2f} cm")
    else:
        print("Error: No valid reading")
    
    time.sleep(1)  # Wait 1 second before the next measurement

