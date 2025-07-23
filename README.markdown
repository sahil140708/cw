# Career Will Telegram Bot

A Telegram bot to extract and upload course batch information to Telegram groups or channels. Built with Python and deployable on Render.

## Features
- **/start**: Displays a welcome message.
- **/list**: Lists all available course batches from `career_will_batches.json`.
- **/upload**: Uploads batch details to a specified Telegram group or channel.

## Prerequisites
- Python 3.7+
- Telegram account
- Render account (for deployment)
- Git installed

## Setup Instructions

### 1. Create a Telegram Bot
1. Open Telegram and search for `@BotFather`.
2. Send `/start`, then `/newbot`.
3. Follow prompts to name your bot (e.g., "CareerWillBot") and set a username (e.g., `@CareerWillBot`).
4. Copy the API token provided (e.g., `123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZ`).

### 2. Local Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/career-will-bot.git
   cd career-will-bot
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set the bot token as an environment variable:
   - On Linux/Mac:
     ```bash
     export TELEGRAM_BOT_TOKEN="your-bot-token-here"
     ```
   - On Windows (Command Prompt):
     ```cmd
     set TELEGRAM_BOT_TOKEN=your-bot-token-here
     ```
4. Update `career_will_batches.json` with your course batch data.
5. Run the bot locally:
   ```bash
   python telegram_bot.py
   ```

### 3. Deploy to Render
1. Create a Render account at [render.com](https://render.com).
2. Create a new **Web Service** in the Render dashboard.
3. Connect your GitHub repository:
   - Fork or push this repository to your GitHub account.
   - In Render, select "New Web Service" and connect to your GitHub repo.
4. Configure the service:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: Automatically set by `Procfile` (`python telegram_bot.py`)
   - **Environment Variables**:
     - Key: `TELEGRAM_BOT_TOKEN`, Value: Your bot token
     - Key: `PYTHON_VERSION`, Value: `3.8` (or your preferred version)
   - **Instance Type**: Free or paid, depending on your needs.
5. Deploy the service. Render will provide a URL (e.g., `https://your-app-name.onrender.com`).
6. Verify webhook setup:
   - After deployment, the bot automatically sets a webhook using the Render URL.
   - Check webhook status by sending `/start` to the bot in Telegram.

### 4. Add Bot to Group/Channel
- Add the bot as an admin to the target group or channel:
  - In Telegram, go to group/channel settings and add `@YourBotUsername`.
  - Grant admin permissions for posting messages.
- Get the Chat ID:
  - Use a bot like `@GetIDsBot` or check bot logs for the Chat ID.
  - Example: Group IDs start with `-` (e.g., `-123456789`), channel IDs start with `@` (e.g., `@YourChannel`).

## Usage
- **/list**: View all batches.
- **/upload**: Enter a Chat ID to upload batch details to a group/channel.
- Example output:
  ```
  Course: Python Programming
  Batch ID: PYT-2025-01
  Start Date: 2025-08-01
  Details: Beginner-friendly course, 12 weeks, online
  ```

## Customization
- Update `career_will_batches.json` with your course data.
- Modify `telegram_bot.py` to fetch data from a database or API instead of JSON.
- Add more commands (e.g., filter batches by course) by extending the bot handlers.

## Notes
- **Security**: Keep your bot token secure. Use environment variables, not hard-coded values.
- **Render Free Tier**: May have limitations (e.g., instance sleep after inactivity). Consider a paid plan for 24/7 uptime.
- **Error Handling**: Ensure the bot is an admin in the target group/channel for `/upload` to work.

## License
MIT License