import pandas as pd
import random
import string
import logging
import numpy as np
import matplotlib.pyplot as plt

def generate_log_entry():
    """Generate a log entry with a timestamp, log level, action, and message."""

    timestamp= pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    log_level = random.choice(['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])
    action = random.choice(['Login', 'Logout', 'Data_request', 'Download', 'File_upload', 'Error'])
    user = ''.join(random.choices(string.ascii_uppercase+ string.digits , k=8))
    return f"{timestamp} - {log_level} - {action} - User: {user}"

# Function to write log entries to a file
def write_logs_to_file(log_filename, num_entries=100):
    """Write log entries to a file."""
    try:
        with open(log_filename, 'w') as file:
            for _ in range(num_entries):
                log = generate_log_entry()
                file.write(log + '\n')
        print(f"Log entries written to {log_filename}")

    except Exception as e:
        logging.error(f"Error in write_logs_to_file: {e}")
        print("An error occurred to write filename")

# Function to read the log file and process it.
def load_and_process_logs(log_filename= "generated_logs.txt"):
    """
    Loads and processes the logs from the given file,cleaning and parsing the timestamps.
    """
    try:
            df = pd.read_csv(log_filename, sep=' - ', header=None, names=['Timestamp', 'Log_Level', 'Action', 'User'],engine='python') 
    
            # Clean and trim spaces around the timestamp
            df['Timestamp'] = df['Timestamp'].str.strip()
            # Convert the timestamp to datetime format
            df['Timestamp'] = pd.to_datetime(df['Timestamp'],errors='coerce' )
    
            # Drop rows with invalid timestamps
            df=df.dropna(subset=['Timestamp'])
    
            if df.empty:
                print("No valid log entries found.")
            else:
                print("Log entries loaded and processed successfully.")
                print(df.head())
        
            # Set the timestamp column as the index for time based operations
            df.set_index('Timestamp', inplace=True)
            return df
        
    except Exception as e:
            logging.error(f"Error in load_and_process_logs: {e}")
            print("An error occurred to load and process logs")
            return None
    
# Function to perform basic statistical analysis using pandas and numpy
def analyse_data(df):
    """
      Perform basic statistical analysis such as counting log levels and actions,and computing basic statistics
    """
   
    if df is None or df.empty:
        print("No data to analyze.")
        return None

    # count the occurance of each log level
    log_level_counts= df['Log_Level'].value_counts()
    actions_counts= df['Action'].value_counts()
    log_counts = len(df)
    unique_users = df['User'].nunique()
    logs_per_day = df.resample('D').size()

    # Averages of action per day
    avg_actions_per_day =    logs_per_day.mean()
    max_logs_per_day = logs_per_day.max()

    #Display summer statistics
    print("\nLog Level Counts:\n", log_level_counts)
    print("\nAction Counts:\n", actions_counts)
    print("\nTotal log entries:\n,log_counts",log_counts)
    print("\nUnique users:\n",unique_users)
    print("\nAverage actions per day:\n", avg_actions_per_day)
    print("\nmaximum logs per day:\n", max_logs_per_day)
    print(type(log_level_counts))
    print(type(actions_counts))
    print(type(log_counts))
    print(type(unique_users))
    
    #create a dictionary to store statistical ananlysis results
    stats ={
         "log_level_counts=log_level_counts": log_level_counts,
         "action_counts": actions_counts,
         "log_counts":log_counts,
         "unique_users": unique_users,
         "avg_actions_per_day": avg_actions_per_day,
         "max_logs_per_day": max_logs_per_day
    }

    return stats
# Function to visualize trends over time using matplotlib
def visualize_trends(df):
    """
    Visualize trends over time using matplotlib
    """
    try:
         logs_per_day = df.resample('D').size()
         
         #plotting log frequency over matlplotlib
         plt.figure(figsize=(10,5))
         plt.plot(logs_per_day.index,logs_per_day.values, marker='o', linestyle='-',color='blue')
         plt.title('Log Frequency Over Time')
         plt.xlabel('Date')
         plt.ylabel('Number of Logs')
         plt.xticks(rotation=45)
         plt.grid()
         
         # Show the plot
         plt.tight_layout()
         plt.show()
         print("Trend visualization complete.")
    except Exception as e:
        logging.error(f"Error in visualize_trends: {e}")
        print("An error occurred to visualize trends")

# Step1: Random log file generating
log_filename = "generated_logs.txt"
write_logs_to_file(log_filename,200)

#Step2: Load and process the logs from the file
df_logs= load_and_process_logs(log_filename)

#Step3: Perform basic statistical analysis
stats = analyse_data(df_logs)

#step4: Visualize trends over time
visualize_trends(df_logs)

         