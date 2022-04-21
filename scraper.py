import collections
import requests
import json

BASE_URL = "https://api.github.com/users/"


class Scraper:

    def __init__(self, login):
        self.__repos_url = BASE_URL + login + "/repos"
        self.__account_url = BASE_URL + login
        self.__load_repo_list()
        self.__load_bio_info()

    def __load_repo_list(self):
        try:
            repos_request = requests.get(self.__repos_url)
            repos_json = repos_request.json()
            repos_list = []
            unique_lang = dict()
            for repo in repos_json:
                language_request = requests.get(repo["languages_url"])
                language_json = language_request.json()
                for lang in language_json:
                    if lang not in unique_lang:
                        unique_lang[lang] = language_json[lang]
                    else:
                        unique_lang[lang] += language_json[lang]
                repo_data = dict([("name", repo['name']),
                                  ("languages", language_json)])
                repos_list.append(repo_data)
            self.__repos_list__ = dict([("repositories", repos_list)])
            self.__used_lang_list__ = unique_lang
        except requests.exceptions.Timeout:
            self.__used_lang_list__ = None
            self.__repos_list__ = dict([("error_message",
                                         "Timeout exception occured !")])
        except requests.exceptions.TooManyRedirects:
            self.__used_lang_list__ = None
            self.__repos_list__ = dict([("error_message",
                                         "Too many redirection occured !")])
        except (TypeError, ValueError, KeyError,
                requests.exceptions.RequestException):
            self.__used_lang_list__ = None
            self.__repos_list__ = dict([("error_message", "Invalid querry !")])

    def __load_bio_info(self):
        try:
            bio_request = requests.get(self.__account_url)
            bio_json = bio_request.json()
            self.__bio_data__ = dict([("login", bio_json["login"]),
                                      ("name", bio_json["name"]),
                                      ("bio", bio_json["bio"]),
                                      ("unique_langs_used",
                                       self.__used_lang_list__)])
        except requests.exceptions.Timeout:
            self.__bio_data__ = dict([("error_message",
                                       "Timeout exception occured !")])
        except requests.exceptions.TooManyRedirects:
            self.__bio_data__ = dict([("error_message",
                                       "Too many redirection occured !")])
        except (TypeError, ValueError, KeyError,
                requests.exceptions.RequestException):
            self.__bio_data__ = dict([("error_message", "Invalid querry !")])

    def get_repo_info(self):
        return self.__repos_list__

    def get_bio_info(self):
        return self.__bio_data__