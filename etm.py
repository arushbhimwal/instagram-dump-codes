import pandas as pd
from datetime import datetime

# Function to load delegate data from an Excel file
def load_delegates(file_path):
    try:
        delegates = pd.read_excel(file_path)
        print("Delegates loaded successfully!")
        return delegates
    except Exception as e:
        print(f"Error loading delegates: {e}")
        return None

# Function to manage event details
def manage_event(fixed_host, delegates, year):
    # Co-host for the given year is selected from the list of delegates
    co_host = delegates.iloc[year % len(delegates), 0]  # Rotating co-host based on the year

    event_details = {
        "Year": year,
        "Fixed Host": fixed_host,
        "Co-host": co_host,
        "Event Date": datetime(year, 10, 19)  # Assuming the event is on 19th October every year
    }

    print(f"Event details for {year}:")
    print(f"Fixed Host: {fixed_host}")
    print(f"Co-host: {co_host}")
    print(f"Event Date: {event_details['Event Date'].strftime('%Y-%m-%d')}")

    return event_details

# Example usage
if __name__ == "__main__":
    # File path for the Excel file containing delegates
    file_path = "27th ETM Program Schedule.xlsx"  # Update this to your actual file path

    # Load the delegate data
    delegates = load_delegates(file_path)

    if delegates is not None:
        # Define the fixed host
        fixed_host = "CHT"  # Replace with your fixed host's name

        # Specify the year for which you want to manage the event
        current_year = datetime.now().year

        # Manage the event for the current year
        event_details = manage_event(fixed_host, delegates, current_year)
