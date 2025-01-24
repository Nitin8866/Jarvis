# Jarvis: A Voice-Activated Personal Assistant

Jarvis is a voice-activated personal assistant that simplifies tasks such as sending emails, playing music, searching Google, and more. Built with Python, it leverages speech recognition and APIs to provide a smooth and interactive user experience.

---

## Features
- **Voice Commands**: Activate and control Jarvis using voice commands like "Hey Jarvis" or "Hi Jarvis."
- **Email Sending**: Send emails via Gmail with subject and message recognition.
- **YouTube Search**: Search and play music or videos on YouTube using the YouTube Data API.
- **Wikipedia Search**: Fetch Wikipedia articles and open them in your browser.
- **Google Search**: Perform quick Google searches directly from your voice commands.
- **Application Launcher**: Open installed applications on your macOS system.
- **Multi-Language Support**: Responds in English (default) and Hindi (for specific queries).

---

## Prerequisites
1. **Python Version**: Ensure you have Python 3.9 or later installed.
2. **Required Python Libraries**:
   - `speechrecognition`
   - `wikipedia-api`
   - `requests`
   - `smtplib`
3. **Operating System**: Works on macOS (required for the `say` command for text-to-speech).
4. **YouTube Data API Key**: Obtain a valid API key from the [Google Cloud Console](https://console.cloud.google.com/).
5. **Gmail Credentials**:
   - Enable "Less Secure Apps" or generate an app-specific password for Gmail.

---

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/jarvis-assistant.git
   cd jarvis-assistant

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**:
   - Create a `.env` file or export the variables directly:
     ```bash
     export YOUTUBE_API_KEY="Your_Youtube_API_Key"
     export EMAIL_USER="Your_Gmail_Email"
     export EMAIL_PASS="Your_Gmail_Password"
     ```

4. **Run the Script**:
   ```bash
   python jarvis.py
   ```

---

## Usage
1. **Activate Jarvis**:
   - Use voice commands like **"Hey Jarvis"** or **"Hi Jarvis"** to start interacting.
   
2. **Give Commands**:
   - **"Play music Despacito"**: Searches YouTube and plays the requested song.
   - **"Send email to Nitin"**: Sends an email after asking for the subject and message.
   - **"Search Google for Python tutorials"**: Opens search results for Python tutorials in your default browser.
   - **"Open Safari"**: Launches Safari or any specified application on macOS.
   - **"Search Wikipedia for Python"**: Opens the relevant Wikipedia page in your browser.

---

## Configuration
1. **Voice Settings**:
   - Change the `VOICE` variable in the script to customize the default voice (e.g., `Rishi` for English or `Lekha` for Hindi).

2. **Timeouts**:
   - Modify the `timeout` value in the `take_command` function to adjust how long Jarvis listens for commands.

---

## Limitations
1. **Operating System**: Currently works only on macOS for voice output (uses the `say` command).
2. **Internet Dependency**: Most features require an active internet connection.
3. **Gmail SMTP**: May require enabling "Less Secure Apps" or using an app-specific password.

---

## Contributing
Contributions are welcome! If you'd like to add new features, improve existing functionality, or fix bugs, please submit a pull request. Make sure to follow the repository's coding guidelines.

---

## License
This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## Future Enhancements
- Add support for Windows and Linux for text-to-speech functionality.
- Integrate natural language processing for better command understanding.
- Expand multi-language support to other languages.
- Add more APIs for enhanced functionality.
```
