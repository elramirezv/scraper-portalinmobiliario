# Portal Inmobiliario Scraper

A Python-based web scraper that monitors Portal Inmobiliario for new apartment listings and sends notifications through Telegram when new properties are found.

## Features

- Monitors multiple Portal Inmobiliario URLs
- Sends notifications via Telegram when new apartments are found
- Keeps track of already seen listings to avoid duplicate notifications
- Runs in Docker for easy deployment
- Checks for new listings every 2 hours

## Prerequisites

- Docker and Docker Compose installed on your system
- A Telegram bot token and chat ID

## Setup

1. Clone this repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create a `.env` file in the root directory with your Telegram credentials:
```
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

3. (Optional) Modify the URLs in `main.py` to match your search criteria. The default configuration searches for:
   - 3+ bedroom apartments in Providencia between 6000-11000 UF
   - 3+ bedroom apartments in Las Condes between 6000-11000 UF

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

The project includes a deployment script (`deploy.sh`) that can automatically deploy to a remote server. To use it:

1. Update the server configuration in `deploy.sh`:
```bash
SERVER_IP="your_server_ip"
SERVER_USER="your_server_user"
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

- `main.py`: Main application file
- `services/`
  - `scraper.py`: Web scraping functionality
  - `telegram.py`: Telegram notification service
  - `logger.py`: Logging configuration
- `already_seen.json`: Cache file for processed listings
- `docker-compose.yml`: Docker Compose configuration
- `Dockerfile`: Docker image configuration
- `deploy.sh`: Deployment script

## Contributing

Feel free to submit issues and enhancement requests!

## License

[Add your chosen license here]
