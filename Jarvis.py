import speech_recognition as sr
import wikipediaapi
import webbrowser
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import subprocess
import requests
import logging

# Set up logging
logging.basicConfig(level=logging.INFO) 

# Your YouTube Data API key (store securely)
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY', 'Your_Youtube_API_Key')

# Voice options (choose one from the list of available voices)
VOICE = 'Rishi'  # Change this to the desired voice

def speak(audio, lang='en'):
    """Uses macOS 'say' command to convert text to speech with natural pauses and specific voice."""
    try:
        # Adding natural pauses with ellipses and commas
        audio = audio.replace('.', '. ...').replace('?', '? ...').replace(',', ', ...')
        
        # Set the voice and language
        if lang == 'hi':
            command = ['say', '-v', 'Lekha', audio]
        else:
            command = ['say', '-v', VOICE, audio]
        
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error in speak function: {e}")
    except Exception as e:
        logging.error(f"Unexpected error in speak function: {e}")

def take_command():
    """Listens for a command and returns it as a string."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        logging.info("Adjusting for ambient noise, please wait...")
        r.adjust_for_ambient_noise(source, duration=1)
        logging.info("Listening...")
        try:
            audio = r.listen(source, timeout=15)
            logging.info("Audio data received")
            query = r.recognize_google(audio, language="en-IN")
            logging.info(f"Recognized query: {query}")
            return query
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            logging.error(f"Request error: {e}")
            speak("Sorry, there was a problem with the speech recognition service.")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            speak("Sorry, something went wrong.")
        return None

def jarvis_activated(command):
    """Checks if the activation phrase is present in the command."""
    activation_phrases = ['hey jarvis', 'jarvis', 'hi jarvis']
    return any(phrase in command.lower() for phrase in activation_phrases)

def handle_command(query):
    """Processes the given command and executes the appropriate action."""
    logging.info(f"Handling command: {query}")
    query = query.lower()

    # Check for playing music
    if 'play music' in query or 'play song' in query:
        search_youtube_and_play(query)
    
    # Check for opening a specific website
    elif 'open' in query and 'website' in query:
        website_name = query.replace('open', '').replace('website', '').strip()
        if website_name:
            webbrowser.open(f"https://www.google.com/search?q={website_name}")
        else:
            speak("Please specify a website to open.")

    # Open a specific application
    elif 'open' in query:
        app_name = query.replace('open', '').strip()
        if app_name:
            open_application(app_name)
        else:
            speak("Please specify an application to open.")

    elif 'wikipedia' in query:
        query = query.replace("wikipedia", '').strip()  # Clean up the query
        if query:  # Ensure there's a valid query
            # Open the Wikipedia page in Google Chrome
            wikipedia_url = f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}"
            logging.info(f"Opening Wikipedia page for: {query}")
            webbrowser.get('chrome').open(wikipedia_url)
        else:
            speak("Please specify a topic to search for on Wikipedia.")

    elif 'who are you' in query:
        speak("I am Jarvis, developed by Priyanshi and Nitin")
    
    elif 'tum kaun ho' in query:
        speak("Mai jarvis hu, mujhe priyanshi aur nitin ne develop kiya hai", lang='hi')
    
    elif 'send email to nitin' in query:
        to_email = "nitinmaharj8866@gmail.com"
        try:
            speak("What should be the subject?")
            subject = take_command()
            if subject:
                speak("What should I say?")
                message = take_command()
                if message:
                    send_email(to_email, subject, message)
                else:
                    speak("I didn't catch the message. Please try again.")
            else:
                speak("I didn't catch the subject. Please try again.")
        except Exception as e:
            logging.error(f"Error sending email to nitin: {e}")
            speak("Sorry, I was not able to send the email.")
    
    elif 'send email' in query:
        try:
            speak("What is the recipient's email address?")
            to_email = take_command()
            if to_email:  # Ensure that an email was recognized
                to_email = to_email.lower().replace(" at ", "@").replace(" ", "")
                speak(f"Did you mean {to_email}? Say yes or no.")
                confirm = take_command()
                if confirm and 'yes' in confirm:
                    speak("What should be the subject?")
                    subject = take_command()
                    if subject:
                        speak("What should I say?")
                        message = take_command()
                        if message:
                            send_email(to_email, subject, message)
                        else:
                            speak("I didn't catch the message. Please try again.")
                    else:
                        speak("I didn't catch the subject. Please try again.")
                else:
                    speak("Let's try again. Please provide the recipient's email address.")
            else:
                speak("I didn't catch that. Please provide the recipient's email address.")
        except Exception as e:
            logging.error(f"Error sending email: {e}")
            speak("Sorry, I was not able to send the email.")
    
    elif 'search google for' in query:
        logging.info(f"Executing Google search for: {query}")
        query = query.replace("search google for", "").strip()
        speak(f"Searching Google for {query}")
        webbrowser.open(f"https://www.google.com/search?q={query}")
    
    elif 'sleep' in query:
        speak("Jarvis signing off")
        return False
    else:
        speak("Sorry, I didn't understand that command.")
    
    return True

def search_youtube_and_play(query):
    """Searches YouTube and plays the first video based on the user's command."""
    # Extract search query by removing command keywords
    search_query = query.lower().replace("play music", "").replace("play song", "").strip()
    if search_query:
        youtube_search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&maxResults=1&q={search_query}&key={YOUTUBE_API_KEY}"
        
        try:
            response = requests.get(youtube_search_url)
            data = response.json()
            logging.info(f"YouTube API response: {data}")  # Log response for debugging
            
            if 'items' in data and len(data['items']) > 0:
                video_id = data['items'][0]['id']['videoId']
                video_title = data['items'][0]['snippet']['title']
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                
                # Speak the video title and open the video
                speak(f"Now playing {search_query}. Enjoy the music!")
                webbrowser.open(video_url)
            else:
                speak("I couldn't find any video for your query.")
        except Exception as e:
            logging.error(f"Error fetching YouTube data: {e}")
            speak("Sorry, there was an error retrieving the video.")
    else:
        speak("Please provide a song name or title.")

def send_email(to_email, subject, message):
    """Sends an email to the specified recipient."""
    from_email = os.getenv('EMAIL_USER', 'nitinmaharaj8866@gmail.com')
    from_password = os.getenv('EMAIL_PASS', 'BE4TMN8866')

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    try:
        logging.info(f"Attempting to send email from {from_email} to {to_email}")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        speak("Email has been sent!")
        logging.info("Email sent successfully.")
    except smtplib.SMTPAuthenticationError:
        speak("Failed to log in to the email server. Please check your credentials.")
        logging.error("SMTP Authentication Error: Check email credentials.")
    except Exception as e:
        logging.error(f"Error sending email: {e}")
        speak("Sorry, I am not able to send the email at the moment.")

def open_application(app_name):
    """Attempts to open the specified application by name. If the application is not found, informs the user."""
    try:
        # Attempt to open the application using macOS `open -a` command
        result = os.system(f'open -a "{app_name}"')
        
        # Check the result of the command; `0` indicates success, while any other value suggests an issue
        if result == 0:
            logging.info(f"Opened application: {app_name}")
        else:
            # If result is not 0, assume the application was not found
            logging.warning(f"Application '{app_name}' not found on the device.")
            speak(f"Sorry, I couldn't find the application {app_name} on this device.")
            
    except Exception as e:
        # Catch any unexpected errors
        logging.error(f"Error opening application: {e}")
        speak(f"An error occurred while trying to open {app_name}.")


# Main loop
if __name__ == "__main__":
    while True:
        command = take_command()
        if command and jarvis_activated(command):
            speak("How can I assist you?")
            while True:
                command = take_command()
                if command:
                    if not handle_command(command):
                        break
        else:
            speak("Please activate me by saying 'Hey Jarvis'.")
