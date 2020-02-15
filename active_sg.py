# def active_sg():
#     LOGIN_URL = "https://members.myactivesg.com/auth/signin"

#     REQUEST_URL = "https://members.myactivesg.com/facilities/view/activity/18/venue/292?time_from=1581609600"

#     payload = {"email": "s9909427c", "password": "however200"}

#     with requests.Session() as session:
#         post = session.post(LOGIN_URL, data=payload)
#         print(post, "\n\n")
#         r = session.get(REQUEST_URL)
#         soup = BeautifulSoup(r.content, "html.parser")
#         results = soup.find(id="formTimeslots")
#         print(results.prettify())
from selenium import webdriver
from selenium_base import SeleniumBase

STARTING_URL = ""


class ActiveSG(SeleniumBase):
    def __init__(self):
        super().__init__(STARTING_URL)

    def _login(self, driver):
        """
        Logs into the website to perform scraping

         Args:
            driver (WebDriver): Contains either firefox or chrome webdriver.
                Needed for use in interacting with the webpage that we want to log into
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
        raise NotImplementedError

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

    def _get_timing_structure_at_court_loc(self, driver):
        """
        Retrieves the timing structure at a particular court location

        Args:
            driver (WebDriver): Contains either firefox or chrome webdriver.
                driver should be set to the badminton booking page of the court location that timing is to be retrieved for.
        
        Returns:
            list<string>: A collection of the timings
        """
        raise NotImplementedError

    def _get_available_courts_at_court_loc(self, driver):
        """
        Finds the timing index of the available courts at the particular court location

        Args:
            driver (WebDriver): Contains either firefox or chrome webdriver.
                driver should be set to the badminton booking page of the court location that timing is to be retrieved for.
        
        Returns:
            list<string>: A collection of the court timing indexes that is available.
                Timing timing to be retrieved from _get_timing_structure_at_court_loc() function.
        """
        raise NotImplementedError

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

    def _go_to_court_loc(self, driver, court_loc_to_check):
        """
        Changes the badminton booking page for a particular court location that @param driver is at to the badminton booking page for another court location

        Args:
            driver (WebDriver): Contains either firefox or chrome webdriver.
                driver should be set to the badminton booking page of any court location
            court_loc_to_check (int): The index of the particular court location that you want to navigate too.
                court_loc_to_check should be between 0 - 75 
        """
        pass

    def get_available_timings(self, day):
        driver = self._get_driver(
            "chrome",
            "C:/Users/winst/Documents/MEGA/Programs!/chromedriver_win32/chromedriver.exe",
        )
