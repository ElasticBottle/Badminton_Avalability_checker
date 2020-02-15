import enum

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

NUMBER_OF_CC_WITH_BADMINTON_COURT = 75
PAUSE = 5


class Browser(enum.Enum):
    CHROME = "chrome"
    FIREFOX = "firefox"


class OnePaTiming:
    def __get_driver(self, browser, driver_path):
        if browser == Browser.CHROME.value:
            return webdriver.Chrome(driver_path)
        if browser == Browser.FIREFOX.value:
            return webdriver.Firefox(driver_path)

    def __click_date(self, driver, day):
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
                break

    def __get_cc_name(self, driver):
        return driver.find_element_by_xpath(
            ".//*[@class = 'facilitiesHeader']/a"
        ).get_attribute("innerText")

    def __get_timing_structure_at_cc(self, driver):
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
        # Finding available courst for the day
        courts = driver.find_elements_by_xpath(".//*[@id='facTable1']/div/span")
        available_courts = list()
        for court in courts:
            if court.get_attribute("class") == "slots normal":
                available_courts.append(
                    court.find_element_by_xpath(".//div/input").get_attribute("id")[-1]
                )
        return available_courts

    def __get_timing_for_cc(self, driver):
        cc_name = self.__get_cc_name(driver)
        cc_timings = self.__get_timing_structure_at_cc(driver)
        cc_available_slots = self.__get_available_courts_at_cc(driver)
        cc_available_timings = [cc_timings[int(i)] for i in cc_available_slots]
        print("Available timings at", cc_name, ":\n", cc_available_timings)
        # Todo: get the timing that the available courts correspond too
        # Todo: go through all the courts that the cc has to offer
        # Todo: store the results for the timings in each CC somewhere
        # Todo: return the result for the timings in each CC

    def __go_to_next_cc(self, driver, cc_to_check):
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

        driver = self.__get_driver(
            "chrome",
            "C:/Users/winst/Documents/MEGA/Programs!/chromedriver_win32/chromedriver.exe",
        )

        # Connecting to the page
        driver.get("https://www.onepa.sg/facilities/4020CCMCPA-BM")

        self.__click_date(driver, day)

        print("reached new date")
        driver.implicitly_wait(PAUSE)
        for i in range(NUMBER_OF_CC_WITH_BADMINTON_COURT):
            self.__get_timing_for_cc(driver)
            self.__go_to_next_cc(driver, i + 1)
            driver.implicitly_wait(5)
        self.__get_timing_for_cc(driver)
