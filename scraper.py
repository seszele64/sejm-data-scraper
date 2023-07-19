
# bs4 -> remote
from bs4 import BeautifulSoup

# regex
import re

# datetime -> convert dates
import datetime

# requests -> get html
import requests

# import mp as mp

# -------------------------- get all active MPs ids -------------------------- #


def get_all_active_mp_ids(
        term: int = 9,
):
    """
    Get all active MPs ids from the main page.

    Returns:
    - list: A list containing all active MPs ids.
    """

    url = f'https://sejm.gov.pl/Sejm{term}.nsf/poslowie.xsp?type=A'

    # create soup object
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')

    # main site, div id="contentBody"
    main_site = soup.find('div', {'id': 'contentBody'})

    # get hrefs from uls, class 'deputies'
    deputies = main_site.find_all('ul', {'class': 'deputies'})

    # iterate over <li> and get hrefs
    hrefs = []

    # find all <li> in <ul> with class 'deputies'
    for deputy in deputies:
        # find all <li> in <ul> with class 'deputies'
        for li in deputy.find_all('li'):
            # get href from <a> in <li>
            href = li.find('a').get('href')
            # append href to hrefs list
            hrefs.append(href)

    # extract id from hrefs
    ids = []

    for href in hrefs:
        id = href.split('=')[1].split('&')[0]
        ids.append(id)

    return ids

# ------------------------------------- < ------------------------------------ #


ids = get_all_active_mp_ids()


class Scraper:
    def __init__(self, html, retries=3):
        """
        Initialize the Scraper instance.

        Parameters:
        - html (str): The HTML content to be scraped.
        - data: The specific data required for the scraper.
        """

        # retries
        self._retries = retries

        self._soup = BeautifulSoup(html, 'html.parser')
        self._party_info = self.get_political_info()
        self._personal_info = self.get_personal_info()

        self.expiration_date = None
        self.expiration_reason = None
        self.expiration_document = None

    # ---------------------------- party info section ---------------------------- #

    def get_political_info(self) -> tuple:
        """
        Get all party information from the data.

        Returns:
        - tuple: A tuple containing the party information.
        """
        political_info_data = self._soup.find(
            'div', {'class': 'partia'}).find('ul', {'class': 'data'})

        political_info = PoliticalInfo(political_info_data)

        return political_info.get_all_data()

    # ------------------------------- personal info ------------------------------ #

    def get_personal_info(self):
        """
        Get the personal information.

        Returns:
        - tuple: A tuple containing the personal information.
        """

        personal_info = PersonalInfo(self._soup)

        return personal_info.get_all_data()

    # getter -> get email

    def decode_email(self, encoded_email):
        """_summary_
        Decode the email address from html source code.

        Args:
            encoded_email (str): example: '#K r z y s z t o f   D O T   B o s a k   A T   s e j m   D O T   p l '

        Returns:
            decoded_email (str): example: 'Krzysztof.Bosak@sejm.pl'
        """
        decoded_email = encoded_email.replace(
            ' D O T ', '.').replace(' A T ', '@').replace('#', '')
        decoded_email = decoded_email.replace(' ', '')
        return decoded_email

    # get email
    def get_email_address(self):

        if self._soup.find('a', {'id': 'view:_id1:_id2:facetMain:_id190:_id280'}) is None:
            return None

        # xpath '//*[@id="view:_id1:_id2:facetMain:_id190:_id280"]'
        encoded_email_address = self._soup.find(
            'a', {'id': 'view:_id1:_id2:facetMain:_id190:_id280'}).get('href')

        # decode email
        decoded_email_address = self.decode_email(encoded_email_address)

        return decoded_email_address


class Info:
    def __init__(self, data):
        self._data = data

    def find_data(self, tag, attributes=None, string=None):
        """
        Find data within the stored data using specified tag, attributes, and string.

        Parameters:
        - tag (str): The HTML tag to search for.
        - attributes (dict): A dictionary of attributes to match for the tag (default is None).
        - string (str or regex): The string or regular expression to match within the tag (default is None).

        Returns:
        - BeautifulSoup Tag or None: The matching tag or None if not found.
        """
        element = self._data.find(tag, attrs=attributes, string=string)
        return element or None

    def get_all_data(self):
        return (self._data,)

    def __str__(self):
        return f'{self.__class__.__name__}: {self._data}'


class ClubInfo(Info):
    def __init__(self, data):
        super().__init__(data)
        self.set_name_and_link()

    @property
    def name(self):
        """
        Get the club name.

        Returns:
        - str: The club name.
        """
        return self._name

    @property
    def link(self):
        """
        Get the club link.

        Returns:
        - str: The club link.
        """
        return self._link

    def set_name_and_link(self):
        """
        Set the club name and link based on the stored data.

        This method uses the instance variable self._data instead of a parameter.
        """
        link_elem = self._data.find('a')
        if link_elem:
            self._name = link_elem.text
            self._link = link_elem.get('href')
        else:
            self._name = None
            self._link = None

    def __str__(self):
        return f'''
        Club name: {self._name}
        Club link: {self._link}
        '''


class PoliticalInfo(Info):
    def __init__(self, political_data):
        super().__init__(political_data)
        self._data = political_data
        self.set_elected_date()
        self.set_party_list()
        self.set_constituency()
        self.set_no_of_votes()
        self.set_oath_date()
        self.set_club()
        self.set_parliamentary_experience()

    def set_elected_date(self):
        self._elected_date = self._data.find('p', {'class': 'right'}).text

    def set_party_list(self):
        self._party_list = self._data.find(
            'p', {'id': 'lblLista'}).find_next_sibling('p').text

    def set_constituency(self):
        self._constituency = self._data.find('p', {'id': 'okreg'}).text

    def set_no_of_votes(self):
        self._no_of_votes = self._data.find(
            'p', {'id': 'lblGlosy'}).find_next_sibling('p').text

    def set_oath_date(self):
        oath_date = self._data.find('p', string=re.compile(
            'Ślubowanie:')).find_next_sibling('p').text
        self._oath_date = datetime.datetime.strptime(
            oath_date, '%d-%m-%Y').strftime('%Y-%m-%d')

    def set_club(self):
        self._club = ClubInfo(self._data)

    def set_parliamentary_experience(self):
        self._parliamentary_experience = self._data.find(
            'p', {'id': 'lblStaz'}).find_next_sibling('p').text

    # properties

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
    def club(self):
        return self._club

    @property
    def parliamentary_experience(self):
        return self._parliamentary_experience

    @property
    def club_name(self):
        return self._club.name if self._club else None

    @property
    def club_link(self):
        return self._club.link if self._club else None

    # methods

    def get_all_data(self):
        return (
            self.elected_date,
            self.party_list,
            self.constituency,
            self.no_of_votes,
            self.oath_date,
            self.club_name,
            self.parliamentary_experience
        )

    def __str__(self):
        return f'''
        Elected date: {self.elected_date}
        Party list: {self.party_list}
        Constituency: {self.constituency}
        Number of votes: {self.no_of_votes}
        Oath date: {self.oath_date}
        Club name: {self.club_name}
        Club link: {self.club_link}
        Parliamentary experience: {self.parliamentary_experience}
        '''


class PersonalInfo(Info):
    def __init__(self, data):
        self._data = data
        self.set_name_surname()
        self._personal_data = data.find('div', {'class': 'cv'})
        super().__init__(self._personal_data)
        self.set_birth_date_and_place()
        self.set_education()
        self.set_school()
        self.set_profession()

    def set_name_surname(self):
        name = self._data.find('h1').text
        self._name, self._surname = name.rsplit(' ', 1)

    def set_birth_date_and_place(self):
        birth_date_place = self.find_data('p', {'id': 'urodzony'})
        if birth_date_place:
            birth_date_place = birth_date_place.text
            parts = birth_date_place.split(',')
            self._birth_date = datetime.datetime.strptime(
                parts[0].strip(), '%d-%m-%Y').strftime('%Y-%m-%d')
            self._birth_place = parts[1].strip() if len(parts) > 1 else None

    def set_education(self):
        education_elem = self._data.find('p', {'id': 'lblWyksztalcenie'})
        self._education = education_elem.find_next_sibling(
            'p').text if education_elem else None

    def set_school(self):
        school_elem = self._data.find('p', {'id': 'lblSzkola'})
        self._school = school_elem.find_next_sibling(
            'p').text if school_elem else None

    def set_profession(self):
        profession_elem = self._data.find('p', {'id': 'lblZawod'})
        self._profession = profession_elem.find_next_sibling(
            'p').text if profession_elem else None

    def get_all_data(self):
        return self._name, self._surname, self._birth_date, self._birth_place, self._education, self._school, self._profession

    def __str__(self):
        return f'''
        Name: {self._name}
        Surname: {self._surname}
        Birth date: {self._birth_date}
        Birth place: {self._birth_place}
        Education: {self._education}
        School: {self._school}
        Profession: {self._profession}
        '''
