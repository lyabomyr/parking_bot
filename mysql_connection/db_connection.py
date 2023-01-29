import mysql.connector
import pandas as pd
from parking_bot.google_sheet import GoogleSheetClient
from config import Config, Querry,ColumnName


def connect():
    conn = mysql.connector.connect(
        host= Config.db_host,
        port= Config.db_port,
        user= Config.db_user,
        password= Config.db_password
        )
    return conn

def mysql_execute( query):
    conn = connect()
    mycursor = conn.cursor( )
    mycursor.execute(query)
    print(mycursor.rowcount, "record effected")
    conn.commit()
    mycursor.close()
    conn.close()
    return mycursor 

def get_query_to_pandas(query):
    conn = connect()
    mycursor = conn.cursor()
    mycursor.execute(query)
    rows = mycursor.fetchall()
    df = pd.DataFrame.from_records(rows, columns=[x[0] for x in mycursor.description])
    mycursor.close()
    conn.close()
    return df

def mysql_init():
    print('start')
    conn = connect()
    mycursor = conn.cursor()
    print('executing preparation...')
    mysql_execute('SET NAMES \'utf8\'')
    mysql_execute("Drop  table if exists pybot.booking")
    mycursor.execute(Querry.create_database)
    print(Querry.create_database)
    mycursor.execute(Querry.create_booking_table)
    print(Querry.create_booking_table)
    mycursor.execute(Querry.create_avalots_table)
    print(Querry.create_avalots_table)
    mycursor.execute(Querry.create_last_update_table)
    print(Querry.create_last_update_table)
    mycursor.execute(Querry.truncate_avalots)
    print(Querry.truncate_avalots)
    mycursor.execute(Querry.creaet_create_flag_table)
    print(Querry.creaet_create_flag_table)
    mycursor.execute(Querry.create_user_data_table)
    print(Querry.create_user_data_table)
    all_parking_lots = GoogleSheetClient().get_sheet(Config.sheet_key,Config.avail_parking_lots_sheet_id)
    print('insert avalots')
    for park_lots in all_parking_lots[ColumnName.all_parking_places].values.tolist():
        mycursor.execute(Querry().insert_avalots(park_lots))
        conn.commit()
    print(type(get_query_to_pandas(Querry.select_reserved_list)))
    if get_query_to_pandas(Querry.select_reserved_list).empty:
        google_df = GoogleSheetClient().get_sheet(Config.sheet_key,Config.main_sheet_id)
        for index, row in google_df.iterrows():
            mysql_execute(Querry().insert_reserve(row[ColumnName.user_id],row[ColumnName.user_name], row[ColumnName.surname], row[ColumnName.parking_lots], row[ColumnName.reservation_time]))
            print('inserted after error')
    if get_query_to_pandas(Querry.select_all_user_data).empty:
        google_df = GoogleSheetClient().get_sheet(Config.sheet_key,Config.user_data_sheet_id)
        for index, row in google_df.iterrows():
            mysql_execute(Querry().insert_user_data(row[ColumnName.user_id], row[ColumnName.user_name]))
    mycursor.close()
    conn.close()
    return print("complete init start")

mysql_init()
