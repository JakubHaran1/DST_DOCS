from calendar_dst import Calendar_dst
import pandas as pd
from datetime import *
import os
from typing import Tuple, List, Union, Dict
from enum import Enum

class DST_app:
    """
    Klasa DST_app reprezentuje aplikację do obsługi restauracji.

    Attributes:
        open_hours (str): Określa godziny otwarcia restauracji w formacie "HH:MM-HH:MM".
        open_days (list): Lista dni tygodnia, w których restauracja jest otwarta, z możliwością określenia, że w niektóre dni jest zamknięta.
        location (str): Adres restauracji.
        tables (dict): Słownik zawierający informacje o dostępnych stolikach w restauracji, gdzie kluczami są różne typy stolików, a wartościami są kolejne słowniki zawierające numery stolików oraz listy godzin, w których są one dostępne.
    """
    
    open_hours = "13:00-23:00"
    open_days = ["Sunday", "close","Tuesday", "Wednesday","close", "Friday", "Saturday"]
    location = "ul.Twój stary nietoperz 666, Łódz - 21-37"
   
    tables = {
        "2": { 
            "1": ["13:00", "15:00", "17:00", "19:00", "21:00", "23:00"],
            "2": ["13:00", "15:00", "17:00", "19:00", "21:00", "23:00"],
            "3": ["13:00", "15:00", "17:00", "19:00", "21:00", "23:00"],
            "4": ["13:00", "15:00", "17:00", "19:00", "21:00", "23:00"],
            "5": ["13:00", "15:00", "17:00", "19:00", "21:00", "23:00"]
        },   
        "4": {
            "6": ["13:00", "15:00", "17:00", "19:00", "21:00", "23:00"],
            "7": ["13:00", "15:00", "17:00", "19:00", "21:00", "23:00"]
            },
        "6": {
            "8": ["13:00", "15:00", "17:00", "19:00", "21:00", "23:00"],
            "9": ["13:00", "15:00", "17:00", "19:00", "21:00", "23:00"]
            },
        "10": {
            "10": ["13:00", "15:00", "17:00", "19:00", "21:00", "23:00"],
            "11": ["13:00", "15:00", "17:00", "19:00", "21:00", "23:00"]
            },
    }

    def __init__(self) -> None:
        """
        Konstruktor klasy, inicjalizuje obiekt klasy DST_app.
        """
        self.order_tables = self.get_saved_tables("order_tables.txt")
        self.basket: List[int] = [0]
        self.full_days: List[str] = []    
        self.available_dates = self.get_available_dates(self.tables)
        
        # 0 - addres, 1 - order_date, 3 - date_now, 4 - hour_now, 5 - table, 6 - order_hour
        values_start = self.start()
        ordered = self.order_food()
        self.make_recipe(values_start, ordered)
        self.save_tables()

    def get_date(self) -> List[Union[str,float]]:
        """
        Pobiera aktualną datę i czas.

        Returns:
            List[str, float]: Aktualna data i czas w postaci listy.
        """
        date_obj = datetime.today()
        day_v = date_obj.weekday()
        [date_v,time_str] = str(date_obj).split(" ")
        # konwersja godzin usera - time
        hours,minutes = time_str.split(":")[0:2]
        time_v = float(f"{hours}.{minutes}")

        return [date_v,day_v,time_v]

    def get_available_dates(self,tables:Dict[str, dict[str, List[str]]])  -> int:
        """
        Oblicza liczbę dostępnych godzin w restauracji na podstawie dostępnych stolików.

        Args:
            tables (dict): Słownik zawierający informacje o dostępnych stolikach w restauracji.

        Returns:
            int: Liczba dostępnych godzin w restauracji.
        """
        available = 0
        for key, val in tables.items():
            for key1,val1 in val.items():
                available += len(val1)
        return available

    def check_day(self,day) -> Tuple[bool,str]:
        """
        Sprawdza, czy dany dzień jest dniem otwartym w restauracji.

        Args:
            day (str): Dzień tygodnia.

        Returns:
            Tuple[bool, str]: Krotka zawierająca informację logiczną True, jeśli restauracja jest otwarta w danym dniu, w przeciwnym razie False oraz komunikat informujący o statusie.
        """
        if day.lower() in self.open_days:
            if day.lower() == "close":
                return False, "This day is closed!"
            return True, "This day is open!"
        else:
            return False, "This day is closed!"

    def check_time(self,time_v:float) -> Tuple[bool,str]:
        """
        Sprawdza, czy dana godzina jest godziną otwarcia restauracji.

        Args:
            time_v (float): Godzina.

        Returns:
            Tuple[bool, str]: Krotka zawierająca informację logiczną True, jeśli restauracja jest otwarta o danej godzinie, w przeciwnym razie False oraz komunikat informujący o statusie.
        """
        open_h,close_h = map(float,self.open_hours.split("-"))
        if open_h <= time_v <= close_h:
            return True, "We are open!"
        else:
            return False, "We are closed!"

    def check_table(self,table:str, table_hour:List[str], time_v:float, date_v:str, day_v:int) -> Tuple[bool,str]:
        """
        Sprawdza dostępność wybranego stolika o danej godzinie.

        Args:
            table (str): Numer stolika.
            table_hour (List[str]): Lista godzin dostępności stolika.
            time_v (float): Godzina.
            date_v (str): Data.
            day_v (int): Numer dnia tygodnia.

        Returns:
            Tuple[bool, str]: Krotka zawierająca informację logiczną True, jeśli stolik jest dostępny o danej godzinie, w przeciwnym razie False oraz komunikat informujący o statusie.
        """
        if table_hour == []:
            return False, "This table is not available today!"
        if date_v in self.full_days:
            return False, "This date is full!"
        if self.check_day(day_v)[0] and self.check_time(time_v)[0]:
            if time_v < float(table_hour[-1]) and time_v >= float(table_hour[0]):
                if date_v in self.order_tables.keys() and table in self.order_tables[date_v].keys():
                    for hour in self.order_tables[date_v][table]:
                        if abs(time_v - float(hour)) < 2:
                            return False, "This table is already ordered at this hour!"
                    return True, "Table is available."
                return True, "Table is available."
        return False, "Table is not available at this hour!"

    def get_saved_tables(self,filename:str) -> Dict[str,dict[str, List[str]]]:
        """
        Pobiera dane o zarezerwowanych stolikach z pliku tekstowego.

        Args:
            filename (str): Nazwa pliku tekstowego.

        Returns:
            Dict[str,dict[str, List[str]]]: Słownik zawierający zarezerwowane stoliki wraz z datami i godzinami rezerwacji.
        """
        if os.path.isfile(filename):
            with open(filename,"r") as file:
                lines = file.readlines()
            data = {}
            for line in lines:
                order_data = line.strip().split(",")
                if order_data[0] in data.keys():
                    data[order_data[0]][order_data[1]] = order_data[2:]
                else:
                    data[order_data[0]] = {order_data[1]:order_data[2:]}
            return data
        return {}

    def save_tables(self) -> None:
        """
        Zapisuje dane o zarezerwowanych stolikach do pliku tekstowego.
        """
        with open("order_tables.txt","w") as file:
            for key,val in self.order_tables.items():
                for key1,val1 in val.items():
                    file.write(f"{key},{key1},{','.join(val1)}\n")

    def start(self) -> List[Union[str,float]]:
        """
        Rozpoczyna proces rezerwacji stolika w restauracji.

        Returns:
            List[Union[str,float]]: Lista zawierająca dane niezbędne do złożenia zamówienia.
        """
        print("Welcome to our restaurant!")
        addr = self.location
        print(f"Here's our address: {addr}")
        [date_v,day_v,time_v] = self.get_date()
        print(f"Today is {date_v} and it's {day_v} day of the week.")
        print(f"It's {time_v} now.")
        return [addr,date_v,day_v,time_v]

    def order_food(self) -> Tuple[str,str]:
        """
        Pozwala na złożenie zamówienia w restauracji.

        Returns:
            Tuple[str,str]: Krotka zawierająca numer stolika oraz godzinę zamówienia.
        """
        print("\nPlease, make an order!")
        table = input("Choose a table number (2,4,6,10): ")
        while table not in self.tables.keys():
            print("Table not available!")
            table = input("Choose a table number (2,4,6,10): ")
        print(f"Available hours for table {table}: {self.tables[table]}")
        table_hour = self.tables[table]
        time_order = input("Choose an hour for the order (13.0-23.0): ")
        while not time_order.replace(".","",1).isdigit() or float(time_order) < 13.0 or float(time_order) > 23.0:
            print("Wrong format!")
            time_order = input("Choose an hour for the order (13.0-23.0): ")
        [addr,date_v,day_v,time_v] = self.get_date()
        check_t,info_t = self.check_table(table,table_hour[str(table)],float(time_order),date_v,day_v)
        if check_t:
            print(info_t)
            return table,time_order
        else:
            print(info_t)
            return self.order_food()

    def make_recipe(self,values_start:List[Union[str,float]],ordered:Tuple[str,str]) -> None:
        """
        Tworzy paragon z zamówienia.

        Args:
            values_start (List[Union[str,float]]): Lista zawierająca dane niezbędne do złożenia zamówienia.
            ordered (Tuple[str,str]): Krotka zawierająca numer stolika oraz godzinę zamówienia.
        """
        addr,date_v,day_v,time_v = values_start
        table, time_order = ordered
        print("\nParagon:")
        print(f"Address: {addr}")
        print(f"Order date: {date_v}")
        print(f"Day of the week: {day_v}")
        print(f"Hour now: {time_v}")
        print(f"Table number: {table}")
        print(f"Order hour: {time_order}\n")
        print("Thank you for your order!")
        
if __name__ == "__main__":
    app = DST_app()


