import csv
from ics import Calendar, Event
from datetime import datetime
import pytz

def parse_date(date_str):
    for fmt in ('%d/%m/%Y %H.%M.%S', '%d/%m/%Y %H:%M:%S'):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            pass
    raise ValueError(f"time data '{date_str}' does not match any known format")

def csv_to_ics(ics_filename):
    calendar = Calendar()
    timezone = pytz.timezone("Europe/Rome")
    with open("calendario - Sheet1.csv", newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            event = Event()
            if(row['test']=='TEST'):
                event.name =row['test']+ " - " + row['Modulo']
            else:
                event.name = row['Modulo']

            event.begin = timezone.localize(parse_date(row['Data inizio']))
            event.end = timezone.localize(parse_date(row['Data fine']))
            event.description = row['aula']
            event.alarms = []
            event.geo = (43.88075, 11.100805)
            calendar.events.add(event)
    
    with open(ics_filename, 'w', encoding='utf-8', newline='') as icsfile:
        icsfile.write(calendar.serialize())

# Example usage
csv_to_ics('events.ics')
