from scraper import ids
import pandas as pd

# class for Member of Parliament site


class MP_Site:

    # index list of all MPs, scraped from website
    MP_INDEX_LIST = ids

    def __init__(self, mp_index):
        self.mp_index = mp_index  # Use the setter to format the value

    # properties -> getters
    @property
    def mp_index(self):
        return self._mp_index

    @property
    def mp_info_site(self):
        return f'https://sejm.gov.pl/Sejm9.nsf/posel.xsp?id={self._mp_index}'

    @property
    # speech number is the number of the speech in the MP's speech list
    def mp_speech_site(self):
        return f'https://sejm.gov.pl/Sejm9.nsf/wypowiedzi.xsp?id={self._mp_index}&type=P&symbol=WYPOWIEDZI_POSLA'

    @property
    def mp_voting_site(self):
        return f'https://sejm.gov.pl/Sejm9.nsf/agent.xsp?symbol=POSELGL&NrKadencji=9&Nrl={self._mp_index}'

    # setter for mp_index -> from 001 to 460, has to be a string
    @mp_index.setter
    def mp_index(self, mp_index):
        if isinstance(mp_index, int):
            # fill mp_index with zeros to make it a three-digit number
            self._mp_index = str(mp_index).zfill(3)

            if mp_index in self.MP_INDEX_LIST:
                self._mp_index = mp_index
            else:
                raise ValueError(
                    "Invalid mp_index value. It should be an integer in id range.")

        if isinstance(mp_index, str):
            if len(mp_index) == 3 and mp_index in self.MP_INDEX_LIST:
                self._mp_index = mp_index
            else:
                raise ValueError(
                    "Invalid mp_index value. It should be a three-digit number in ids range.")
        else:
            raise ValueError(
                "Invalid mp_index value. It should be a string of length 3 or an integer.")


# class for each Member of Parliament


class MP:

    # constructor -> what is needed to create an object of this class
    def __init__(self, index, name, surname, link, constituency, elected_date, party_list, no_of_votes, oath_date, parliamentary_experience, club, birth_date, education, school, profession, email):

        # example infos

        # Imię:Andrzej
        # Nazwisko:Adamczyk
        # Link:https://sejm.gov.pl/Sejm9.nsf/posel.xsp?id=001
        # Wybrany dnia:13-10-2019
        # Lista:Prawo i Sprawiedliwość
        # Okręg wyborczy:13  Kraków
        # Liczba głosów:29686
        # Ślubowanie:12-11-2019
        # Staż parlamentarny:poseł V kadencji, poseł VI kadencji, poseł VII kadencji, poseł VIII kadencji
        # Klub/koło:Klub Parlamentarny Prawo i Sprawiedliwość
        # Data i miejsce urodzenia:04-01-1959, Krzeszowice
        # Wykształcenie:wyższe
        # Ukończona szkoła:Społeczna Akademia Nauk w Łodzi, Wydział Zarządzania, Rachunkowośc i finanse w zarządzaniu - licencjat (2014)
        # Zawód:parlamentarzysta
        # E-mail:

        self._index = index
        self._name = name
        self._surname = surname
        self._link = link

        self._elected_date = elected_date
        self._party_list = party_list
        self._constituency = constituency
        self._no_of_votes = no_of_votes
        self._oath_date = oath_date
        self._parliamentary_experience = parliamentary_experience
        self._club = club

        self._birth_date = birth_date
        self._education = education
        self._school = school
        self._profession = profession

        self._email = email

    # properties -> getters

    @property
    def index(self):
        return self._index

    @property
    def elected_date(self):
        return self._elected_date

    @property
    def party_list(self):
        return self._party_list

    @property
    def constituency(self):
        return self._constituency

    @property
    def no_of_votes(self):
        return self._no_of_votes

    @property
    def oath_date(self):
        return self._oath_date

    @property
    def parliamentary_experience(self):
        return self._parliamentary_experience

    @property
    def club(self):
        return self._club

    @property
    def birth_date(self):
        return self._birth_date

    @property
    def education(self):
        return self._education

    @property
    def school(self):
        return self._school

    @property
    def profession(self):
        return self._profession

    @property
    def email(self):
        return self._email

    @property
    def get_data(self):
        return (
            self._index,
            self._name,
            self._surname,
            self._link,
            self._party_list,
            self._constituency,
            self._elected_date,
            self._no_of_votes,
            self._oath_date,
            self._parliamentary_experience,
            self._club,
            self._birth_date,
            self._education,
            self._school,
            self._profession,
            self._email)

    # return as dataframe
    @property
    def to_df(self):
        return pd.DataFrame([self.get_data], columns=['id', 'name', 'surname', 'link', 'party_list', 'constituency', 'elected_date', 'no_of_votes', 'oath_date', 'parliamentary_experience', 'club', 'birth_date', 'education', 'school', 'profession', 'email'])

    # methods
    def __str__(self):
        return f'''
        Id: {self._index}
        Member of Parliament: {self._name} {self._surname}
        Link: {self._link}
        Party list: {self._party_list}
        Constituency: {self._constituency}
        Elected date: {self._elected_date}
        No of votes: {self._no_of_votes}
        Oath date: {self._oath_date}
        Parliamentary experience: {self._parliamentary_experience}
        Club: {self._club}
        Birth date: {self._birth_date}
        Education: {self._education}
        School: {self._school}
        Profession: {self._profession}
        Email: {self._email}
        '''
