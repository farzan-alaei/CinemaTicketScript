#! /usr/bin/python3

import json, os
from custom_exceptions import FilmError, NoCapacityError
import logging
import os

LOG_FILE = "./log/movie.log"
JSON_FILE = "./database/films.json"

if not os.path.exists(LOG_FILE):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

LOG_FILE = "./log/movie.log"
JSON_FILE = "./database/films.json"

if not os.path.exists(LOG_FILE):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

logger = logging.getLogger(__name__)
file_h = logging.FileHandler(LOG_FILE)

file_f = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(massage)s")
file_h.setFormatter(file_f)
file_h.setLevel(logging.INFO)
logger.addHandler(file_h)


class Film:
    """
    This class is for modeling film.
    """

    films = {}

    def __init__(self, name: str, genre: str, age_rating: str, tickets: dict = {}):
        self.name = name
        self.genre = genre
        self.age_rating = age_rating
        self.tickets = tickets

        Film.films.update({self.name: self.__dict__})
        Film.save_films_to_json("./database/films.json", Film.films)

    @classmethod
    def load_films_from_json(cls, JSON_FILE):
        """
        This class method is for loading our films and\
                tickets data in the dictionary\
                from a json file called database/films.json
        """
        with open(JSON_FILE, mode="r", encoding="utf-8") as file:
            return json.load(file)

    @classmethod
    def save_films_to_json(cls, JSON_FILE, dictionary):
        """
        This class method is for saving our films and\
                tickets data in the dictionary\
                into a json file called database/films.json
        """
        with open(JSON_FILE, mode="w+", encoding="utf-8") as file:
            json.dump(dictionary, file, indent=4)

    @staticmethod
    def add_film(name: str, genre: str, age_rating: str):
        """
        This class method is for adding a film and its ticket.
        """
        Film.films = Film.load_films_from_json("./database/films.json")
        Film(name, genre, age_rating)

    @classmethod
    def get_object(cls, name):
        """
        This class method is for getting the film name\
                and creating a object from that information\
                for us.
        """
        for i, j in Film.films.items():
            if i == name:
                return cls(j["name"], j["genre"], j["age_rating"])

    def delete_film_obj(self):
        del self

    @classmethod
    def remove_film(cls, name: str):
        """
        This class method is for removing\
                a film fro our database.
        """
        if name not in Film.films:
            raise FilmError("Film Not Found! ")
        del Film.films[name]
        cls.save_films_to_json("./database/films.json", Film.films)


class Ticket(Film):
    """
    This class is for modeling Ticket
    """

    ticket_dict = {}

    def __init__(self, name, scene_date, showtime, capacity, price: int):
        self.name = name
        self.scene_date = scene_date
        self.showtime = showtime
        self.available_seats = capacity
        self.price = price

        Ticket.ticket_dict.update(
            {f"{self.scene_date} _ {self.showtime}": self.__dict__}
        )
        Film.films = Film.load_films_from_json("./database/films.json")

        Ticket.ticket_dict.update(Film.films[name]["tickets"])
        Film.films[name]["tickets"] = Ticket.ticket_dict

        Film.save_films_to_json("./database/films.json", Film.films)
        Ticket.ticket_dict.clear()

    @staticmethod
    def add_ticket(name, scene_date, showtime, capacity, price):
        """
        This method is for adding a ticket from a defined film
        """
        t_obj = Ticket(name, scene_date, showtime, capacity, price)
        t_obj.delete_film_obj()

    @classmethod
    def sell_ticket(cls, film_name, ticket_key, quantity):
        """
        This method is for seeling ticket\
                taking us count and substraction this\
                count from our total quantity of that\
                ticket
        """
        if quantity <= Film.films[film_name]["tickets"][ticket_key]["available_seats"]:
            Film.films[film_name]["tickets"][ticket_key]["available_seats"] -= quantity
            Film.save_films_to_json("./database/films.json", Film.films)
            print(f"{quantity} ticket(s) sold successfully.")
        else:
            raise NoCapacityError("Insufficient ticket! ")

    def delete_ticket_obj(self):
        del self
