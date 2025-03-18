import csv
from datetime import datetime
import pytz
from uuid import uuid4

# Function to parse date strings into datetime objects
def parse_date(date_str):
    for fmt in ('%d/%m/%Y %H:%M:%S', '%d/%m/%Y %H:%M:%S'):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            pass
    raise ValueError(f"time data '{date_str}' does not match any known format")

# Function to format datetime to ICS format
def format_ics_datetime(dt):
    return dt.strftime("%Y%m%dT%H%M%S")

# Function to convert CSV data to ICS format
def csv_to_ics(ics_filename):
    timezone = pytz.timezone("Europe/Rome")
    
    # Start building the ICS content
    ics_content = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//CSV to ICS Converter//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH"
    ]
    
    # Open and read the CSV file
    with open("./aprile.csv", newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        
        # Iterate over each row in the CSV file
        for row in reader:
            # Create a unique ID for the event
            event_uid = str(uuid4())
            
            # Set event name based on the 'test' field
            if row['test'] == 'TEST':
                event_name = f"{row['test']} - {row['Modulo']}"
            else:
                event_name = row['Modulo']
            
            # Parse and format start and end times
            start_dt = timezone.localize(parse_date(row['Data inizio']))
            end_dt = timezone.localize(parse_date(row['Data fine']))
            
            start_str = format_ics_datetime(start_dt)
            end_str = format_ics_datetime(end_dt)
            
            # Add timezone information
            start_str += "Z" if start_dt.tzinfo is None else ""
            end_str += "Z" if end_dt.tzinfo is None else ""
            
            # Create the event
            ics_content.extend([
                "BEGIN:VEVENT",
                f"UID:{event_uid}",
                f"SUMMARY:{event_name}",
                f"DESCRIPTION:{row['aula']}",
                f"DTSTART:{start_str}",
                f"DTEND:{end_str}",
                f"GEO:43.88075;11.100805",  # Same geo coordinates as original
                "END:VEVENT"
            ])
    
    # Complete the ICS file
    ics_content.append("END:VCALENDAR")
    
    # Write the calendar to an ICS file
    with open(ics_filename, 'w', encoding='utf-8', newline='\r\n') as icsfile:
        icsfile.write('\r\n'.join(ics_content))

# Example usage
if __name__ == "__main__":
    csv_to_ics('events.ics')
    print("ICS file successfully created!")
