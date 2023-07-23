import os


class Config:
    db_host = os.getenv('DB_HOST', 'mysql')  # localhost
    db_port = 3306
    db_user = os.getenv('DB_USER', "root")
    db_password = os.getenv('DB_PASSWORD', 'test1234')
    service_account_file = 'booking-parking-place-918d6fcf7e75.json'
    sheet_key = '1AaOa3WcdB0qIDVNzeOqxJpSHM9gwYghqhcPnWVlElig'
    main_sheet_id = 0
    avail_parking_lots_sheet_id = 1
    user_data_sheet_id = 2
    commands = ["reserve", "list_reserved_parking_lots", "remove_reserve"]
    PARKING_BOT_TOKEN = os.environ.get('PARKING_BOT_TOKEN')  # '5944821419:AAESYXzxMM942idnIrITlZvkoEBNzQMAKmQ'
    STATUS_BOT_TOKEN = os.environ.get('STATUS_BOT_TOKEN')  # '5934102533:AAFnDv8G8Of-gyB9YKSPYwGK_-3hb57whwM'
    # chat_id='-565980061' #test
    chat_id = '-1001550996439'  # production


class ColumnName:
    user_id = 'user_id'
    user_name = 'user_name'
    surname = 'surname'
    parking_lots = 'parking_lots'
    reservation_time = 'reservation_time'
    all_parking_places = 'all_parking_places'
    database_name = 'pybot'
    update_date = 'update_date'
    google_flag = 'google_flag'
    table_list_slots = 'avalots'
    table_list_reserve = 'booking'
    table_timestamp_action = 'last_update_date'
    table_flag = 'flags'
    table_user_data = 'user_data'


class Querry:
    create_database = f"CREATE  DATABASE IF NOT EXISTS {ColumnName.database_name} DEFAULT CHARSET=utf8;"
    create_booking_table = f"CREATE TABLE IF NOT EXISTS {ColumnName.database_name}.{ColumnName.table_list_reserve} ({ColumnName.user_id} VARCHAR(255), {ColumnName.user_name} VARCHAR(255), {ColumnName.surname} VARCHAR(255), {ColumnName.parking_lots} VARCHAR(255), {ColumnName.reservation_time} VARCHAR(255)) DEFAULT CHARSET=utf8;"
    create_avalots_table = f"CREATE TABLE IF NOT EXISTS {ColumnName.database_name}.{ColumnName.table_list_slots}  ({ColumnName.all_parking_places} VARCHAR(255)) DEFAULT CHARSET=utf8;"
    create_last_update_table = f"CREATE TABLE IF NOT EXISTS {ColumnName.database_name}.{ColumnName.table_timestamp_action} ({ColumnName.update_date} VARCHAR(255)) DEFAULT CHARSET=utf8;"
    creaet_create_flag_table = f"CREATE TABLE IF NOT EXISTS {ColumnName.database_name}.{ColumnName.table_flag} ({ColumnName.google_flag} VARCHAR(255)) DEFAULT CHARSET=utf8;"
    create_user_data_table = f"CREATE TABLE IF NOT EXISTS {ColumnName.database_name}.{ColumnName.table_user_data} ({ColumnName.user_id} VARCHAR(255), {ColumnName.user_name} VARCHAR(255))  DEFAULT CHARSET=utf8;"

    truncate_avalots = f"TRUNCATE {ColumnName.database_name}.{ColumnName.table_list_slots};"
    truncate_booking = f"TRUNCATE {ColumnName.database_name}.{ColumnName.table_list_reserve};"
    truncte_google_flag = f"TRUNCATE {ColumnName.database_name}.{ColumnName.table_flag};"
    truncte_user_data = f"TRUNCATE {ColumnName.database_name}.{ColumnName.table_user_data};"

    select_reserved_list = f"select * from {ColumnName.database_name}.{ColumnName.table_list_reserve};"
    select_all_parking_lot = f"select * from {ColumnName.database_name}.{ColumnName.table_list_slots};"
    select_google_flag = f"select * from {ColumnName.database_name}.{ColumnName.table_flag};"

    select_all_user_data = f"select  {ColumnName.user_id},{ColumnName.user_name} from {ColumnName.database_name}.{ColumnName.table_user_data}"

    def select_user_data_table(self, user_id):
        return f"select {ColumnName.user_name} from {ColumnName.database_name}.{ColumnName.table_user_data} where {ColumnName.user_id} = \'{user_id}\'"

    insert_google_flag = f"INSERT INTO {ColumnName.database_name}.{ColumnName.table_flag} ({ColumnName.google_flag}) VALUES (\'Yes\')"

    def insert_avalots(self, park_lot):
        return f"INSERT INTO {ColumnName.database_name}.{ColumnName.table_list_slots} ({ColumnName.all_parking_places}) VALUES (\'{park_lot}\');"

    def insert_reserve(self, user_id, name, surname, parking_lot, reserve_time):
        return f"INSERT INTO {ColumnName.database_name}.{ColumnName.table_list_reserve} (user_id, user_name, surname , parking_lots , reservation_time) VALUES (\"{user_id}\",\"{name}\",\"{surname}\",\"{parking_lot}\",\"{reserve_time}\");"

    def insert_user_data(self, user_id, name):
        return f"INSERT INTO {ColumnName.database_name}.{ColumnName.table_user_data} ({ColumnName.user_id}, {ColumnName.user_name}) VALUES (\"{user_id}\",\"{name}\")"

    def delete_from_avalots(self, lot):
        return f"DELETE FROM {ColumnName.database_name}.{ColumnName.table_list_slots} WHERE {ColumnName.all_parking_places} like \"{lot}\";"

    def delete_from_user_data(self, user_id):
        return f"DELETE FROM {ColumnName.database_name}.{ColumnName.table_user_data} WHERE {ColumnName.user_id} = \"{user_id}\";"

    def delete_from_reserve(self, user_id):
        return f"DELETE FROM {ColumnName.database_name}.{ColumnName.table_list_reserve} WHERE {ColumnName.user_id} = \"{user_id}\";"
