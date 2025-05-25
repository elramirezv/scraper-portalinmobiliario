# Portal Inmobiliario Scraper

A Python-based web scraper that monitors Portal Inmobiliario for new apartment listings and sends notifications through Telegram when new properties are found.

## Features

- Monitors multiple Portal Inmobiliario URLs with different search criteria
- Sends notifications via Telegram when new apartments are found
- Keeps track of already seen listings using a JSON cache file
- Runs in Docker for easy deployment
- Checks for new listings every 2 hours
- Supports multiple chat IDs for different notification channels
- Automatic deployment script with error handling and logging
- Robust error handling and logging system

## Prerequisites

- Docker and Docker Compose installed on your system
- A Telegram bot token and chat ID
- Python 3.12 or higher (for local development)

## Setup

1. Clone this repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create a `.env` file in the root directory with your credentials:
```
TELEGRAM_BOT_TOKEN=your_bot_token_here
SERVER_IP=your_server_ip
```

3. (Optional) Modify the URLs in `main.py` to match your search criteria. The default configuration searches for:
   - 3+ bedroom apartments in Providencia between 0-11000 UF
   - 3+ bedroom apartments in Las Condes between 0-11000 UF
   - Apartments in Ñuñoa for rent between 0-700,000 CLP

## Running the Application

1. Build and start the container:
```bash
docker compose up -d
```

2. Check the logs:
```bash
docker compose logs -f
```

## Deployment

The project includes a deployment script (`deploy.sh`) that can automatically deploy to a remote server. The script includes:
- Automatic Docker and Docker Compose installation if not present
- Backup creation
- Error handling and logging
- Automatic cleanup of unused resources

To use it:

1. Make sure your `.env` file includes the server configuration:
```
SERVER_IP="your_server_ip"
```

2. Make the script executable:
```bash
chmod +x deploy.sh
```

3. Run the deployment:
```bash
./deploy.sh
```

## Project Structure

- `main.py`: Main application file that orchestrates the scraping and notification process
- `services/`
  - `scraper.py`: Web scraping functionality using BeautifulSoup4
  - `telegram.py`: Telegram notification service
  - `logger.py`: Logging configuration
- `already_seen.json`: Cache file for processed listings
- `docker-compose.yml`: Docker Compose configuration
- `Dockerfile`: Docker image configuration using Python 3.12
- `deploy.sh`: Deployment script with error handling
- `requirements.txt`: Python dependencies

## Dependencies

- requests: For making HTTP requests
- beautifulsoup4: For parsing HTML
- python-dotenv: For environment variable management
- python-crontab: For scheduling tasks

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License

Copyright (c) 2025 Alejandro Ramírez

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
