import os
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

# Specify the log directory
log_dir = 'logs'

# Ensure the log directory exists, creating it if necessary
os.makedirs(log_dir, exist_ok=True)

# Define the log file name pattern with a timestamp
log_file_pattern = os.path.join(log_dir, "my_log_%Y-%m-%d.log")

# Create a TimedRotatingFileHandler that rotates daily
handler = TimedRotatingFileHandler(
    filename=datetime.now().strftime(log_file_pattern),  # Initial log file name
    when="midnight",  # Rotate at midnight (daily)
    interval=1,  # Create a new log file every day
    backupCount=30,  # Keep up to 7 days' worth of log files (adjust as needed)
)
handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s'))

# Configure the root logger with the handler
logging.basicConfig(
    level=logging.INFO,  # Set the desired log level
    handlers=[handler],
)

# Your logging statements
logger = logging.getLogger(__name__)