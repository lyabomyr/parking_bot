import os

class Config:
    service_account_file = 'booking-parking-place-918d6fcf7e75.json'
    sheet_key='1AaOa3WcdB0qIDVNzeOqxJpSHM9gwYghqhcPnWVlElig'
    main_sheet_id = 0
    avail_parking_lots_sheet_id =1
    commands = ["reserve","list_reserved_parking_lots","remove_reserve"]
    list_park_places = ['1-27', '1-28', '1-29', '1-30', '1-34']
    PARKING_BOT_TOKEN = os.environ.get('PARKING_BOT_TOKEN')
    STATUS_BOT_TOKEN = os.environ.get('STATUS_BOT_TOKEN')



