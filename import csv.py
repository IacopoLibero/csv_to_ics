import csv
from ics import Calendar, Event
from datetime import datetime
import pytz

# Function to parse date strings into datetime objects
def parse_date(date_str):
    for fmt in ('%d/%m/%Y %H:%M:%S', '%d/%m/%Y %H:%M:%S'):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            pass
    raise ValueError(f"time data '{date_str}' does not match any known format")

# Function to convert CSV data to ICS format
def csv_to_ics(ics_filename):
    calendar = Calendar()
    timezone = pytz.timezone("Europe/Rome")
    
    # Open and read the CSV file
    with open("/home/ifts/Desktop/csv_to_ics/marzo.csv", newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        
        # Iterate over each row in the CSV file
        for row in reader:
            event = Event()
            
            # Set event name based on the 'test' field
            if(row['test']=='TEST'):
                event.name = row['test'] + " - " + row['Modulo']
            else:
                event.name = row['Modulo']
            
            # Set event start and end times
            event.begin = timezone.localize(parse_date(row['Data inizio']))
            event.end = timezone.localize(parse_date(row['Data fine']))
            
            # Set event description and other properties
            event.description = row['aula']
            event.alarms = []
            event.geo = (43.88075, 11.100805)
            
            # Add event to the calendar
            calendar.events.add(event)
    
    # Write the calendar to an ICS file
    with open(ics_filename, 'w', encoding='utf-8', newline='') as icsfile:
        icsfile.write(calendar.serialize())

# Example usage
csv_to_ics('events.ics')
