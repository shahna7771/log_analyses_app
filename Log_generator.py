import random
import time
import string
import logging

#setting up logging for error handling
logging.basicConfig(filename='log_generator_error.log', level=logging.ERROR)

# list the level of logs
log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']

# list of possible actions
actions = ['login', 'logout', 'data_request', 'download', 'file_upload', 'error']

# function to generate a random string for logs
def generate_random_string(length=10):
    """Generate a random string of fixed length."""
    try:
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    except Exception as e:
        logging.error(f"Error in random_string: {e}")
        return "error"

# Function to generate a random log entry
def generate_log_entry():
    """Generate a log entry with a timestamp, log level, action, and message."""
    try:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        log_level = random.choice(log_levels)
        action = random.choice(actions)
        user =  generate_random_string(8)
        log_entry = f"{timestamp} - {log_level} - {action} - User: {user}"
        return log_entry
    except Exception as e:
        logging.error(f"Error in generate_log_entry: {e}")
        return "error"
    
# Function to write log entries to a file
def write_logs_to_file(log_filename, num_entries=100):
    """Write log entries to a file."""
    try:
        with open(log_filename, 'w') as file:
            for _ in range(num_entries):
                log = generate_log_entry()
                if log != "error":
                    file.write(log + '\n')
        print(f"Log entries written to {log_filename}")

    except Exception as e:
        logging.error(f"Error in write_logs_to_file: {e}")
        print("An error occurred to write filename")

# generate and write entries in log file
write_logs_to_file('generated_logs.txt', 200)
    

    