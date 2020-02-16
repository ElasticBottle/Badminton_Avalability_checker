import enum
import time
from multiprocessing import Pool
from selenium_base import SeleniumBase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

NUMBER_OF_CC_WITH_BADMINTON_COURT = 75
PAUSE = 10
STARTING_URL = "https://www.onepa.sg/facilities/4020CCMCPA-BM"


class OnePaTiming(SeleniumBase):
    """
    Allows user to retrieve the list of available timings for all the Community Centers (CC) that offers badminton in Singapore
    """

    def __init__(self):
        super().__init__(STARTING_URL)

    def _login(self, driver):
        pass

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
        driver.find_element_by_xpath("//*[@id='content_0_tbDatePicker']").click()
        clicked = self._get_right_date(driver, day)
        if not clicked:
            driver.find_element_by_xpath(
                "//*[@id='ui-datepicker-div']/div/a[@class = 'ui-datepicker-next ui-corner-all']"
            ).click()
            clicked = self._get_right_date(driver, day)
        return clicked

    def _get_court_loc_name(self, driver):
        """
        Gets the name of the cc that is being checked for badminton court availability

        Args:
            driver (WebDriver): Contains either firefox or chrome webdriver.
                driver should be set to the badminton booking page of the CC that name is to be retrieved for.

        
        Returns:
            string: The name of the CC in which the badminton court is being checked for
        """
        return driver.find_element_by_xpath(
            ".//*[@class = 'facilitiesHeader']/a"
        ).get_attribute("innerText")

    def _get_timing_structure_at_court_loc(self, driver):
        """
        Retrieves the timing structure at a particular CC

        Args:
            driver (WebDriver): Contains either firefox or chrome webdriver.
                driver should be set to the badminton booking page of the CC that timing is to be retrieved for.
        
        Returns:
            list<string>: A collection of the timings, either in 2 hour blocks or in 1 hour blocks 
                Each entry represent a timing block. E.g "9.30 A.M. - 10.30 A.M."
        """
        timings = driver.find_elements_by_xpath(
            ".//*[@id = 'facTable1']/div[@class = 'timeslotsContainer']/div"
        )
        # Removes the title for the time column
        timings.pop(0)

        # Adding the timing to the list
        for i in range(len(timings)):
            timings[i] = timings[i].get_attribute("innerText")
        return timings

    def _get_available_courts_at_court_loc(self, driver):
        """
        Finds the timing index of the available courts at the particular CC

        Args:
            driver (WebDriver): Contains either firefox or chrome webdriver.
                driver should be set to the badminton booking page of the CC that timing is to be retrieved for.
        
        Returns:
            list<string>: A collection of the court timing indexes that is available.
                Timing timing to be retrieved from _get_timing_structure_at_cc() function.
        """
        # Finding available courst for the day
        courts = driver.find_elements_by_xpath(".//*[@id='facTable1']/div/span")
        available_courts = set()
        for court in courts:
            if court.get_attribute("class") == "slots normal":
                available_courts.add(
                    court.find_element_by_xpath(".//div/input").get_attribute("id")[-1]
                )
        return available_courts

    def _get_timing_for_court_loc(self, driver):
        """
        Finds the name, timing structure, and available court of the CC

        Args:
            driver (WebDriver): Contains either firefox or chrome webdriver.
                driver should be set to the badminton booking page of the CC that is of interest.

        Returns:
            string: Contains the name of the CC
            list<string>: Containing the timings whihc are available at the CC
        """
        court_name = self._get_court_loc_name(driver)
        court_timings = self._get_timing_structure_at_court_loc(driver)
        court_available_slots = self._get_available_courts_at_court_loc(driver)
        court_available_timings = [court_timings[int(i)] for i in court_available_slots]
        print("Available timings at", court_name, ":\n", court_available_timings)
        return court_name, court_available_timings

    def _go_to_court_loc(self, driver, court_loc_to_check):
        """
        Changes the badminton booking page for a particular CC that @param driver is at to the badminton booking page for another CC

        Args:
            driver (WebDriver): Contains either firefox or chrome webdriver.
                driver should be set to the badminton booking page of any CC
            cc_to_check (int): The index of the particular CC that you want to navigate too.
                cc_to_check should be between 0 - 75 
        """
        cc_selector = driver.find_element_by_xpath(
            ".//*[@id='select2-content_0_ddlFacilityLocation-container']"
        )
        cc_selector.click()
        cc_selector = driver.find_elements_by_xpath(
            "//*[@id='content_0_ddlFacilityLocation']/option"
        )
        driver.implicitly_wait(PAUSE)
        cc_selector[court_loc_to_check].click()

    def get_available_timings(self, day):
        """
        Checks all CC with badminton courts for their available timings

        Args:
            day(int): day of the month that you would like to retrieve badminton timings for.

        Returns:
            dictionary: Contains all the names of CC with badminton courts mapped to their list of available timings.
        """
        start = time.time()
        driver = self._get_driver(
            "chrome",
            "C:/Users/winst/Documents/MEGA/Programs!/chromedriver_win32/chromedriver.exe",
        )

        self._click_date(driver, day)
        print("reached new date")

        all_available_timing = dict()

        # ? Add multi threading to launch multiple web browsers at once and speed up search
        for i in range(NUMBER_OF_CC_WITH_BADMINTON_COURT):
            court_name, court_timing = self._get_timing_for_court_loc(driver)
            all_available_timing[court_name] = court_timing
            self._go_to_court_loc(driver, i + 1)
        court_name, court_timing = self._get_timing_for_court_loc(driver)
        all_available_timing[court_name] = court_timing

        end = time.time()
        print("time taken", end - start)
        return all_available_timing
