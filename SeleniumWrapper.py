# Selenium Wrapper-*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException


class SeleniumWrapper:
    """Wrap selenoim"""
    def __init__(self):
        self.browser = webdriver.Firefox()

