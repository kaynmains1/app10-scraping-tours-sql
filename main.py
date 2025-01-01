import requests
import selectorlib
import smtplib, ssl
import os
import time
import sqlite3


URL = "https://programmer100.pythonanywhere.com/tours/"


class Event:
    def scrape(self, url):
        response = requests.get(url)
        source = response.text
        return source

    def extract(self, source):
        extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
        value = extractor.extract(source)["tours"]
        return value


class Email:
    def send(self, message):
        host = "smtp.gmail.com"
        port = 465

        username = "lebronlebron321321@gmail.com"
        password = "utvm jjzi hsuk yxkk"

        receiver = "lebronlebron321321@gmail.com"
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(host, port, context=context) as server:
            server.login(username, password)
            server.sendmail(username, receiver, message)


class Database:

    def __init__(self):
        self.connection = sqlite3.connect("data.db")

    def store(self, extracted):
        row = extracted.split(",")
        row = [item.strip(" ") for item in row]
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO events VALUES (?,?,?)", row)
        self.connection.commit()

    def read(self, extracted):
        row =  extracted.split(",")
        row = [item.strip(" ") for item in row]
        band, city, date = row
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?", (band, city, date))
        rows = cursor.fetchall()
        print(rows)
        return rows


if __name__ == "__main__":
    while True:
        event = Event()
        scraped = event.scrape(URL)
        extracted = event.extract(scraped)
        print(extracted)
        if extracted != "No upcoming tours":
            database = Database()
            row = database.read(extracted)
            if not row:
                database.store(extracted)
                email = Email()
                email.send(message="hey, new temperature was found")
        time.sleep(2)