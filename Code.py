import speech_recognition as sr
import RPi.GPIO as GPIO
import time

# GPIO pin configuration for the light
LIGHT_GPIO_PIN = 18  # Adjust based on your wiring

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(LIGHT_GPIO_PIN, GPIO.OUT)

def turn_light_on():
    """Turn the light ON by setting the GPIO pin high."""
    GPIO.output(LIGHT_GPIO_PIN, GPIO.HIGH)
    print("Light ON")

def turn_light_off():
    """Turn the light OFF by setting the GPIO pin low."""
    GPIO.output(LIGHT_GPIO_PIN, GPIO.LOW)
    print("Light OFF")

def listen_for_command():
    """Listen to user's voice commands and return recognized text."""
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    try:
        with microphone as source:
            print("Adjusting for background noise... Please wait.")
            recognizer.adjust_for_ambient_noise(source)  # Reduce background noise
            print("Listening for command...")
            audio_data = recognizer.listen(source)  # Capture the audio

            # Use Google Speech Recognition to convert audio to text
            command_text = recognizer.recognize_google(audio_data).lower()
            print(f"Command received: {command_text}")
            return command_text
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
    except sr.RequestError:
        print("Could not request results from the speech recognition service.")
    
    return ""  # Return empty string if recognition fails

def handle_command(command):
    """Process the recognized command and control the light."""
    if "light on" in command:
        turn_light_on()
    elif "light off" in command:
        turn_light_off()
    else:
        print("Invalid command. Please say 'light on' or 'light off'.")

if _name_ == "_main_":
    try:
        while True:
            # Continuously listen for commands and process them
            voice_command = listen_for_command()
            if voice_command:
                handle_command(voice_command)
            time.sleep(1)  # Add a short delay to avoid rapid looping
    except KeyboardInterrupt:
        print("Program terminated by user.")
    finally:
        GPIO.cleanup()  # Reset GPIO settings before exiting
