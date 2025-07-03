# OSINT Telegram Bot – IP/Domain Intelligence
## Screenshot
![Bot Screenshot](screenshot.png)
## Overview

This Telegram bot performs OSINT (Open Source Intelligence) analysis on IP addresses and domain names.  
It accepts input via text messages, images (OCR), or QR codes, and returns a detailed intelligence report.

## Features

- Supports:
  - Plain text input (IP address or domain name)
  - Images containing IP/domain using OCR
  - QR codes containing IP or domain
- Automatically resolves domain names to IP addresses
- Input validation using regular expressions
- Intelligence checks include:
  - WHOIS data lookup
  - IP geolocation (country, city, ISP)
  - Port scanning (top 15 TCP/UDP ports using Nmap)
  - Blacklist status (e.g., VirusTotal integration)
- Generates an HTML report and returns it to the user
- Rejects unsupported content types (documents, audio, stickers, etc.)
- Includes error handling for API failures, invalid input, and more

## Supported Input

**Accepted:**
- Text: valid IPv4 addresses and domain names 
- Images with visible IP/domain (via OCR)
- QR codes containing valid IP/domain

**Rejected:**
- Any file type that is not an image
- Invalid or empty text input
- Images or QR codes that do not contain valid data

## Technologies Used

- Python
- python-telegram-bot (v20+)
- pytesseract (OCR)
- pyzbar (QR code decoding)
- socket, whois, requests
- Nmap (port scanning)
- python-dotenv (.env management)
- Docker (containerization)

## Requirements

To run this project, you need:
	•	Docker and Docker Compose installed on your machine
(Install Docker, Install Compose)
	•	Telegram bot token from BotFather
	•	API keys for:
	•	VirusTotal
	•	AbuseIPDB
## Setup and Execution

### Clone the Repository

```bash
git clone https://github.com/your-username/osint-telegram-bot.git
cd osint-telegram-bot
```

### Create a `.env` file in the project root

```env
TELEGRAM_TOKEN=your_telegram_bot_token
VT_API_KEY=your_virustotal_api_key
ABUSEIPDB_API_KEY=your_abuseipdb_api_key
```

### Run using Docker Compose

```bash
docker-compose up --build
```

## Report Output

Each analysis generates an `.html` report including:

- WHOIS registration information
- Geolocation (country, city, ISP)
- Open TCP/UDP ports (top 15)
- Malicious or blacklist status (if available)

The report is sent back to the user through Telegram.

## Security and Best Practices

- API keys are stored securely in a `.env` file
- Errors are clearly handled and logged
- Temporary files (images, reports) are removed after processing

## Bot Commands

- `/start` – Welcome message and usage instructions
- `/help` – List of supported inputs and functionality

## APIs and Tools Used

- WHOIS Lookup
- IP Geolocation API
- Nmap
- pytesseract (OCR)
- pyzbar (QR decoder)
- python-telegram-bot

## License

This project is provided for educational and research purposes only.
