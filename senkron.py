import sys
import os

# Sanal ortamı etkinleştir
activate_this = '/home/ubuntu/myenv/bin/activate_this.py'
exec(open(activate_this).read(), {'__file__': activate_this})

import sqlite3
import time
import schedule
from supabase import create_client, Client
import os
import sys

# SQLite ve Supabase bağlantı bilgileri
SQLITE_DB_PATH = r"db_path"
SUPABASE_URL = "---"
SUPABASE_KEY = "---"

def connect_sqlite():
    try:
        return sqlite3.connect(SQLITE_DB_PATH)
    except sqlite3.Error as e:
        print(f"SQLite bağlantı hatası: {e}")
        return None

def connect_supabase():
    try:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"Supabase bağlantı hatası: {e}")
        return None

def fetch_sqlite_data(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    data = {}
    for table in tables:
        table_name = table[0]
        if table_name.startswith('sqlite_'):
            continue  # SQLite sistem tablolarını atla
        cursor.execute(f"SELECT * FROM {table_name};")
        columns = [description[0] for description in cursor.description]
        rows = cursor.fetchall()
        data[table_name] = {"columns": columns, "rows": rows}
    
    return data

def upsert_to_supabase(supabase: Client, table_name: str, columns: list, rows: list):
    for row in rows:
        row_dict = dict(zip(columns, row))
        
        try:
            # Upsert işlemi: id sütunu varsa, on_conflict ile güncelleyerek ekleyelim
            if 'id' in row_dict:
                supabase.table(table_name).upsert(row_dict, on_conflict=['id']).execute()
            else:
                # id yoksa, on_conflict olarak tüm sütunları kullan
                supabase.table(table_name).upsert(row_dict, on_conflict=columns).execute()
            print(f"{table_name} tablosuna veri başarıyla eklendi veya güncellendi.")
        except Exception as e:
            print(f"Veri eklenirken hata oluştu: {e}")

def sync_databases():
    print("Senkronizasyon başlatılıyor...")
    sqlite_conn = connect_sqlite()
    if not sqlite_conn:
        print("SQLite bağlantısı kurulamadı. Senkronizasyon iptal ediliyor.")
        return

    supabase = connect_supabase()
    if not supabase:
        print("Supabase bağlantısı kurulamadı. Senkronizasyon iptal ediliyor.")
        sqlite_conn.close()
        return
    
    try:
        data = fetch_sqlite_data(sqlite_conn)
        for table_name, table_data in data.items():
            columns = table_data["columns"]
            rows = table_data["rows"]
            print(f"{table_name} tablosu senkronize ediliyor...")
            upsert_to_supabase(supabase, table_name, columns, rows)
        print("Senkronizasyon tamamlandı.")
    except Exception as e:
        print(f"Senkronizasyon sırasında hata oluştu: {e}")
    finally:
        sqlite_conn.close()

def main():
    schedule.every(2).minutes.do(sync_databases)
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("Program kullanıcı tarafından sonlandırıldı.")
        sys.exit(0)

if __name__ == "__main__":
    main()
