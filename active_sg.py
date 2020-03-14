import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium_base import SeleniumBase
from user_info import UserInfo
from selenium.webdriver.common.action_chains import ActionChains

STARTING_URL = "https://members.myactivesg.com/auth?redirect=%2Fprofile"
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
        # driver.find_element_by_xpath("//*[@id = 'btn-submit-login']").click()

    def _navigate_to_badminton_booking(self, driver):
        """
        Navigates the driver to the badminton booking page for active sg
        """
        driver.get("https://members.myactivesg.com/facilities")

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

    def _set_date(self, driver, day):
        """
        Clicks the appropriate date on the actve sg badminton website

        Args:
            driver (WebDriver): Contains either firefox or chrome webdriver.
                Needed for use in interacting with the webpages
            day (int): specifies the day of the month that is to be checked for badminton court availability
        
        Return:
            Bool: True for a successful click on the specified date, False otherwise
        """
        # Click on date picker
        driver.find_element_by_xpath('//*[@id="date_filter"]').click()

        # Get list of dates
        dates = driver.find_elements_by_xpath(
            '//*[@id="ui-datepicker-div"]/table/tbody/tr/td/a'
        )

        current_date = 0
        for date in dates:
            if (
                date.get_attribute("class")
                == "ui-state-default ui-state-highlight ui-state-active ui-state-hover"
            ):
                current_date = date.get_attribute("innerText")
                if int(current_date) > day:
                    # Go to next month
                    driver.find_element_by_xpath(
                        '//*[@id="ui-datepicker-div"]/div/a[@class = "ui-datepicker-next ui-corner-all"]'
                    ).click()

                return self._get_right_date(driver, day)

    def _set_activity(self, driver):
        """
        Sets the value of the activity dropdown to "Badminton"

        Args:
            driver (WebDriver): Either the Firefox or Chrome WebDriver
                Should be set to othe book facility page in Active SG
        """
        activity_box = WebDriverWait(driver, PAUSE).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="activity_filter_chosen"]')
            )
        )
        driver.execute_script("arguments[0].scrollIntoView();", activity_box)
        activity_box.click()
        option_to_select = driver.find_element_by_xpath(
            '//*[@id="activity_filter_chosen"]/div/ul/li[2]'
        )
        actions = ActionChains(driver)
        actions.move_to_element(option_to_select)
        actions.click()
        actions.perform()

    def _set_date_and_activity(self, driver, day):
        """
        Sets the day that is to be checked for

        Args:
            driver (WebDriver): Either the Firefox or Chrome WebDriver
                Should be set to othe book facility page in Active SG
            day (int): contains the day of the month that is to be searched
        """
        self._set_activity(driver)
        clicked = self._set_date(driver, day)
        if not clicked:
            print("Date is too far into the future to be booked!")
            driver.quit()
        driver.find_element_by_xpath('//*[@id="search"]').click()

    def _get_court_loc_name(self, driver):
        """
        Gets the name of the court location that is being checked for badminton court availability

        Args:
            driver (WebDriver): Contains either firefox or chrome webdriver.
                driver should be set to the badminton booking page of the court location that name is to be retrieved for.

        
        Returns:
            string: The name of the court location in which the badminton court is being checked for
        """
        court_name = (
            WebDriverWait(driver, PAUSE)
            .until(
                EC.presence_of_element_located(
                    (By.XPATH, "//*[@id='facbookpage']/div/div/div/div/p")
                )
            )
            .get_attribute("innerText")
        )
        return court_name

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
        availability = set()
        timeslots = driver.find_element_by_xpath('//*[@id="formTimeslots"]')
        timeslots = timeslots.find_elements_by_xpath(".//div/div/div/div")
        for time in timeslots:
            available = time.find_element_by_xpath(".//input").get_attribute("name")
            if available == "timeslots[]":
                timing = time.find_element_by_xpath(".//label").get_attribute(
                    "innerText"
                )
                availability.add(timing)
        return availability

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
        court_name = self._get_court_loc_name(driver)
        available_timings = self._get_available_courts_at_court_loc(driver)
        print(court_name, ":\n", available_timings)
        return court_name, available_timings

    def _check_for_next_page(self, driver):
        """
        Checks for next available page containing badminton courts.
        driver is navigated to the next page if one exist, does nothing to driver otherwise

        Args:
            driver (WebDrive): Contains either firefox or chrome webdriver.
                driver should be set to the badminton booking page.
        
        Returns:
            Bool: True if next page has been navigated too, False otherwise.
        """
        next_buttons = driver.find_elements_by_xpath(
            '//*[@id="main"]/div[3]/div/article/div/section/div/ul/li[6]/a'
        )
        next_button = None
        if next_buttons:
            for button in next_buttons:
                if button.get_attribute("innerText") == "Next →":
                    next_button = button
            print(next_button.get_attribute("innerText"))
            driver.execute_script("arguments[0].scrollIntoView();", next_button)
            next_button.click()
            return True
        return False

    def get_available_timings(self, day):
        """
        Retrieves all the available badminton court with its associated timing

        Args:
            day (int): contains the day in which courts are to be searched for

        Returns:
            dictionary<string, list<string>>: Key represent the court names
                Value contains the list of strings representing the available timings of the court
        """
        driver = self._get_driver(
            "chrome",
            "C:/Users/winst/Documents/MEGA/Programs!/chromedriver_win32/chromedriver.exe",
        )

        self._login(driver, UserInfo.get_username(), UserInfo.get_password())
        time.sleep(2)
        self._navigate_to_badminton_booking(driver)
        all_available_timing = dict()
        self._set_date_and_activity(driver, day)

        have_courts = True
        while have_courts:
            available_courts = WebDriverWait(driver, PAUSE).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, './/*[@id = "main"]/div/div/article/div/section/ul/li')
                )
            )

            for i in range(len(available_courts)):
                court = WebDriverWait(driver, PAUSE).until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            './/*[@id = "main"]/div/div/article/div/section/ul/li['
                            + str(i + 1)
                            + "]",
                        )
                    )
                )
                driver.execute_script("arguments[0].scrollIntoView();", court)
                court.click()

                court_name, available_timings = self._get_timing_for_court_loc(driver)
                all_available_timing.update({court_name: available_timings})
                driver.back()
                time.sleep(2)
            have_courts = self._check_for_next_page(driver)

        driver.quit()

        return all_available_timing
