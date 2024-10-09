import speech_recognition as sr
import RPi.GPIO as GPIO
import time

# Setup GPIO for LED control
GPIO.setmode(GPIO.BCM)  # Use Broadcom pin numbering
GPIO.setwarnings(False)  # Disable warnings
LED_PIN = 18  # GPIO pin where LED is connected
GPIO.setup(LED_PIN, GPIO.OUT)  # Set pin as output
GPIO.output(LED_PIN, GPIO.LOW)  # Ensure LED starts off

# Function to switch light ON
def light_on():
    GPIO.output(LED_PIN, GPIO.HIGH)  # Turn LED on
    print("Light ON")

# Function to switch light OFF
def light_off():
    GPIO.output(LED_PIN, GPIO.LOW)  # Turn LED off
    print("Light OFF")

# Setup Speech Recognizer
recognizer = sr.Recognizer()  # Initialize recognizer

def listen_for_command():
    with sr.Microphone() as source:
        print("Listening for command...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust mic sensitivity for background noise
        audio = recognizer.listen(source)  # Listen for command

    try:
        # Recognize speech using Google Web Speech API
        command = recognizer.recognize_google(audio).lower()  # Convert speech to text
        print(f"You said: {command}")

        # Check command and control light accordingly
        if "light on" in command:
            light_on()
        elif "light off" in command:
            light_off()
        else:
            print("Command not recognized, please say 'light on' or 'light off'.")

    except sr.UnknownValueError:
        # Handle case when speech is not understood
        print("Could not understand the command.")
    except sr.RequestError as e:
        # Handle errors in requesting results from Google API
        print(f"Could not request results from Google Speech Recognition service; {e}")

try:
    while True:
        listen_for_command()  # Continuously listen for commands
        time.sleep(1)  # Small delay between listening cycles

except KeyboardInterrupt:
    # Gracefully exit on user interruption
    print("Exiting program")
finally:
    GPIO.cleanup()  # Reset GPIO state on exit
