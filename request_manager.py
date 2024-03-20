"""request manager packages"""
import logging
import requests
from bs4 import BeautifulSoup

# Logging basic configuration
logging.basicConfig(filename="logging's.log")


class Request:
    """Request class to send a request"""
    def __init__(self, url: str) -> None:
        try:
            self.response = requests.get(url=url, timeout=20)
            if self.response.status_code != 200:
                raise requests.exceptions.ConnectionError(
                    'Something went wrong! Please try again later.'
                )
        except requests.exceptions.Timeout as error:
            print('Timeout:', error)
            logging.error('Request timed out')
        except requests.exceptions.ConnectionError as error:
            print('ConnectionError:', error)
            logging.error('Request connection error')
        except requests.exceptions.HTTPError as error:
            print('HTTPError:', error)
            logging.error('HTTP error')
        except AttributeError as error:
            print('AttributeError:', error)
            logging.error('AttributeError')
        else:
            print('Request sent seccussfully')
            logging.info('Request sent seccussfully')

    @property
    def content(self) -> BeautifulSoup:
        """
        This function creates a BeautifulSoup object.
        Use as property
        """
        return BeautifulSoup(self.response.text, 'html.parser')

    @property
    def status_code(self) -> int:
        """
        This function returns request status code.
        Use as property
        """
        try:
            status = self.response.status_code
        except AttributeError as error:
            print('AttributeError:', error)
            logging.error('AttributeError')
            return None
        return status

    @property
    def headers(self) -> dict:
        """
        This function returns website headers.
        Use as property
        """
        return self.response.headers

    def get_one(self, html_tag: str, tag_id_by: str = None, tag_id: str = None):
        """
        This function gets html_tag such as div
        and tag_id_by such as class or id
        and finally tag_id which is different on every website.
        If you do not set tag_id_by or tag_id it will just use html_tag to find data
        """
        try:
            if not tag_id_by or not tag_id:
                data = self.content.find(html_tag)
            else:
                data = self.content.find(
                    html_tag, {tag_id_by: tag_id})
        except ValueError as error:
            print('ValueError:', error)
            logging.error('ValueError')
            return None

        return data

    def get_all(self, html_tag: str, tag_id_by: str = None, tag_id: str = None) -> list:
        """
        This function gets html_tag such as div
        and tag_id_by such as class or id
        and finally tag_id which is different on every website.
        Return a list of all tags that you want.
        If you do not set tag_id_by or tag_id it will just use html_tag to find data.
        """
        try:
            if not tag_id_by or not tag_id:
                datas = self.content.find_all(html_tag)
            else:
                datas = self.content.find_all(
                    html_tag, {tag_id_by: tag_id})
        except ValueError as error:
            print('ValueError:', error)
            logging.error('ValueError')
            return None
        return datas
