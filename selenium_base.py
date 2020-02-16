import enum
from selenium import webdriver
from abc import ABC, abstractmethod


class SeleniumBase(ABC):
    def __init__(self, baseURL):
        super().__init__()
        self.baseURL = baseURL

    class _Browser(enum.Enum):
        """
        Contains the value for the type of browser that may run, firefox or chrome
        """

        CHROME = "chrome"
        FIREFOX = "firefox"

    def _get_driver(self, browser, driver_path):
        """
        Gets the appropriate driver so that Selenium may run based on the browser and driver path specified

        Args:
            brower (string): Tells selenium which webdriver to initialise.
                Either "chrome" or "firefox"
            driver_path (string): Contains the file path to the appropriate selenium driver needed.
                File path should end with the "/DRIVER_NAME.exe"
        """
        # Gets the webdriver and connects to the page of interest

        if browser == self._Browser.CHROME.value:
            driver = webdriver.Chrome(driver_path)
        if browser == self._Browser.FIREFOX.value:
            driver = webdriver.Firefox(driver_path)
        driver.get(self.baseURL)
        return driver

    @abstractmethod
    def _get_court_loc_name(self, driver):
        """
        Gets the name of the court location that is being checked for badminton court availability

        Args:
            driver (WebDriver): Contains either firefox or chrome webdriver.
                driver should be set to the badminton booking page of the court location that name is to be retrieved for.

        
        Returns:
            string: The name of the court location in which the badminton court is being checked for
        """
        raise NotImplementedError

    @abstractmethod
    def _get_timing_for_court_loc(self, driver):
        """
        Finds the name, timing structure, and available court of the court location

        Args:
            driver (WebDriver): Contains either firefox or chrome webdriver.
                driver should be set to the badminton booking page of the court location that is of interest.

        Returns:
            string: Contains the name of the court location
            list<string>: Containing the timings whihc are available at the court location
        """
        raise NotImplementedError


class SeleniumDateHelper:
    def _get_right_date(self, driver, day):
        """
        Searches through the list of available dates and attempts to click the day specified if possible

        Args:
            driver (WebDriver): Contains either firefox or chrome webdriver.
                Needed for use in interacting with the webpages
            day (int): specifies the day of the month that is to be checked for badminton court availability
        
        Return:
            Bool: True for a successful click on the specified date, False otherwise
        """
        raise NotImplementedError

    def _click_date(self, driver, day):
        """
        Clicks the appropriate date on the one_pa badminton website

        Args:
            driver (WebDriver): Contains either firefox or chrome webdriver.
                Needed for use in interacting with the webpages
            day (int): specifies the day of the month that is to be checked for badminton court availability
        
        Return:
            Bool: True for a successful click on the specified date, False otherwise
        """
        return NotImplementedError
