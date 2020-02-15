import enum
import time
from multiprocessing import Pool

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

NUMBER_OF_CC_WITH_BADMINTON_COURT = 75
PAUSE = 5
STARTING_URL = "https://www.onepa.sg/facilities/4020CCMCPA-BM"


class Browser(enum.Enum):
    """
    Contains the value for the type of browser that may run, firefox or chrome
    """

    CHROME = "chrome"
    FIREFOX = "firefox"


class OnePaTiming:
    """
    Allows user to retrieve the list of available timings for all the Community Centers (CC) that offers badminton in Singapore
    """

    def __get_driver(self, browser, driver_path):
        """
        Gets the appropriate driver so that Selenium may run based on the browser and driver path specified

        Args:
            brower (string): Tells selenium which webdriver to initialise.
                Either "chrome" or "firefox"
            driver_path (string): Contains the file path to the appropriate selenium driver needed.
                File path should end with the "/DRIVER_NAME.exe"
        """
        if browser == Browser.CHROME.value:
            return webdriver.Chrome(driver_path)
        if browser == Browser.FIREFOX.value:
            return webdriver.Firefox(driver_path)

    def __click_date(self, driver, day):
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

        # Getting the elements in the date picker and clicking selected date
        elements = driver.find_elements_by_xpath(
            ".//*[@id='ui-datepicker-div']/table/tbody/tr/td/a"
        )
        for dates in elements:
            if (
                dates.is_enabled()
                and dates.is_displayed()
                and str(dates.get_attribute("innerText")) == str(day)
            ):
                dates.click()
                return True
        return False

    def __get_cc_name(self, driver):
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

    def __get_timing_structure_at_cc(self, driver):
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

    def __get_available_courts_at_cc(self, driver):
        """
        Finds the timing index of the available courts at the particular CC

        Args:
            driver (WebDriver): Contains either firefox or chrome webdriver.
                driver should be set to the badminton booking page of the CC that timing is to be retrieved for.
        
        Returns:
            list<string>: A collection of the court timing indexes that is available.
                Timing timing to be retrieved from __get_timing_structure_at_cc() function.
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

    def __get_timing_for_cc(self, driver):
        """
        Finds the name, timing structure, and available court of the CC

        Args:
            driver (WebDriver): Contains either firefox or chrome webdriver.
                driver should be set to the badminton booking page of the CC that is of interest.

        Returns:
            string: Contains the name of the CC
            list<string>: Containing the timings whihc are available at the CC
        """
        cc_name = self.__get_cc_name(driver)
        cc_timings = self.__get_timing_structure_at_cc(driver)
        cc_available_slots = self.__get_available_courts_at_cc(driver)
        cc_available_timings = [cc_timings[int(i)] for i in cc_available_slots]
        print("Available timings at", cc_name, ":\n", cc_available_timings)
        return cc_name, cc_available_timings

    def __go_to_cc(self, driver, cc_to_check):
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
        cc_selector[cc_to_check].click()

    def get_one_pa_timings(self, day):
        """
        Checks all CC with badminton courts for their available timings

        Args:
            day(int): day of the month that you would like to retrieve badminton timings for.

        Returns:
            dictionary: Contains all the names of CC with badminton courts mapped to their list of available timings.
        """
        start = time.time()
        driver = self.__get_driver(
            "chrome",
            "C:/Users/winst/Documents/MEGA/Programs!/chromedriver_win32/chromedriver.exe",
        )

        # Connecting to the page
        driver.get(STARTING_URL)

        self.__click_date(driver, day)
        print("reached new date")

        all_cc_available_timing = dict()
        driver.implicitly_wait(PAUSE)
        for i in range(NUMBER_OF_CC_WITH_BADMINTON_COURT):
            cc_name, cc_timing = self.__get_timing_for_cc(driver)
            all_cc_available_timing[cc_name] = cc_timing
            self.__go_to_cc(driver, i + 1)
            driver.implicitly_wait(5)
        cc_name, cc_timing = self.__get_timing_for_cc(driver)
        all_cc_available_timing[cc_name] = cc_timing

        end = time.time()
        print("time taken", end - start)

        return all_cc_available_timing
