import logging
import os

from modules.simplify_studio.api.cli.cli import run

log_dir = os.path.join("logs", "simplify_studio", "cli")
os.makedirs(log_dir, exist_ok=True)

# Set up logging
logging.basicConfig(
    filename=os.path.join(log_dir, "app.log"),  # Log to a file named 'app.log'
    filemode="a",  # Append to the log file
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,  # Set the logging level to DEBUG
)

if __name__ == "__main__":
    run()
