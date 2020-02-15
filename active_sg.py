# def active_sg():
#     LOGIN_URL = "https://members.myactivesg.com/auth/signin"

#     REQUEST_URL = "https://members.myactivesg.com/facilities/view/activity/18/venue/292?time_from=1581609600"

#     payload = {"email": "s9909427c", "password": "however200"}

#     with requests.Session() as session:
#         post = session.post(LOGIN_URL, data=payload)
#         print(post, "\n\n")
#         results = soup.find(id="formTimeslots")
#         print(results.prettify())
#         r = session.get(REQUEST_URL)
#         soup = BeautifulSoup(r.content, "html.parser")


from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium_base import SeleniumBase

from user_info import UserInfo

STARTING_URL = "https://members.myactivesg.com/auth?redirect=%2Fprofile"
NUMBER_OF_BADMINTON_LOC = 295
PAUSE = 5


class ActiveSG(SeleniumBase):
    def __init__(self):
        super().__init__(STARTING_URL)

    def _login(self, driver, user, password):
        """
        Logs into the website to perform scraping

         Args:
            driver (WebDriver): Contains either firefox or chrome webdriver.
                Needed for use in interacting with the webpage that we want to log into
        """
        email_field = driver.find_element_by_xpath("//*[@id='email']")
        email_field.send_keys(user)
        password_field = driver.find_element_by_xpath("//*[@id = 'password']")
        password_field.send_keys(password)
        submit = driver.find_element_by_xpath("//*[@id = 'btn-submit-login']")
        submit.click()

    def _navigate_to_badminton_booking(self, driver):
        """
        Navigates the driver to the badminton booking page for active sg
        """
        driver.get(
            "https://members.myactivesg.com/facilities/view/activity/18/venue/968?"
        )

    def _get_right_date(self, driver, day):
        # Getting the elements in the date picker and clicking selected date
        elements = driver.find_elements_by_xpath(
            ".//*[@id='ui-datepicker-div']/table/tbody/tr/td/a"
        )

        clicked = False
        for date in elements:
            if (
                date.is_enabled()
                and date.is_displayed()
                and str(date.get_attribute("innerText")) == str(day)
            ):
                date.click()
                clicked = True
        return clicked

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
        # Click to open drop-down
        driver.find_element_by_xpath("//*[@class='datepicker hasDatepicker']").click()

        clicked = self._get_right_date(driver, day)

        if not clicked:
            next_page_btns = driver.find_elements_by_xpath(
                "//*[@id='ui-datepicker-div']/div/a"
            )
            for btn in next_page_btns:
                if (
                    btn.get_attribute("class") == "ui-datepicker-prev ui-corner-all"
                    or btn.get_attribute("class") == "ui-datepicker-next ui-corner-all"
                ):
                    btn.click()
                    return self._get_right_date(driver, day)
        return clicked

    def _get_court_loc_name(self, driver):
        """
        Gets the name of the court location that is being checked for badminton court availability

        Args:
            driver (WebDriver): Contains either firefox or chrome webdriver.
                driver should be set to the badminton booking page of the court location that name is to be retrieved for.

        
        Returns:
            string: The name of the court location in which the badminton court is being checked for
        """
        court_name = driver.find_element_by_xpath(
            "//*[@id='facbookpage']/div/div/div/div/p"
        ).get_attribute("innerText")
        print(court_name)
        return court_name

    def _get_timing_structure_at_court_loc(self, driver):
        """
        Retrieves the timing structure at a particular court location

        Args:
            driver (WebDriver): Contains either firefox or chrome webdriver.
                driver should be set to the badminton booking page of the court location that timing is to be retrieved for.
        
        Returns:
            list<string>: A collection of the timings
        """
        return []

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
        return []

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
        return super()._get_timing_for_court_loc(driver)

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

        self._login(driver, UserInfo.active_sg_user, UserInfo.active_sg_pass)
        self._navigate_to_badminton_booking(driver)
        self._click_date(driver, day)
        print("reached new date")

        all_courts_available_timing = dict()
        driver.implicitly_wait(PAUSE)
        for i in range(NUMBER_OF_BADMINTON_LOC):
            self._get_timing_for_court_loc(driver)
            self._go_to_court_loc(driver, i + 1)
        self._get_timing_for_court_loc(driver)
