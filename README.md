# Sonos Control Project

A web-based control panel for Sonos speakers on your network.

## Features

- **Speaker Discovery**: Automatically finds Sonos speakers on your network
- **Playback Control**: Play, pause, and stop music
- **Volume Control**: Adjust speaker volume from 0-100%
- **Track Information**: Display currently playing track details
- **Web Interface**: Easy-to-use Streamlit web application

## Requirements

- Python 3.7+
- Sonos speakers on your network
- Network access to Sonos speakers (port 1400)

## Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd sonos-control-project
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

## Usage

1. Open your web browser and navigate to the URL shown by Streamlit (usually http://localhost:8501)
2. The app will automatically discover Sonos speakers on your network
3. Select a speaker from the dropdown menu
4. Use the control buttons to play, pause, or stop music
5. Adjust volume using the slider
6. View current track information

## How It Works

The application uses:
- **SSDP (Simple Service Discovery Protocol)** to find Sonos speakers
- **SOAP/XML** to communicate with Sonos speakers via their UPnP interface
- **Streamlit** for the web interface

## Network Requirements

- Sonos speakers must be on the same network as the computer running this application
- Port 1400 must be accessible on Sonos speakers
- UPnP must be enabled on your network

## Troubleshooting

### No Speakers Found
- Ensure Sonos speakers are powered on and connected to the network
- Check if your firewall is blocking the discovery process
- Verify network connectivity between your computer and Sonos speakers

### Control Commands Not Working
- Check if the speaker is currently playing music
- Ensure the speaker is not in a group with other speakers
- Verify the speaker's IP address hasn't changed

### Volume Control Issues
- Some Sonos models may have different volume ranges
- Check if the speaker is muted

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License.
