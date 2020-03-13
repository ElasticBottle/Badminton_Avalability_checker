import datetime
import time
import pandas as pd
from one_pa import OnePa
from active_sg import ActiveSG
from timing_matcher import TimingMatcher
import concurrent.futures as cf


def get_data_from_active_sg(month, day):
    active_sg = ActiveSG()
    available_timings = active_sg.get_available_timings(day)
    matched_times = TimingMatcher()
    timing_df = matched_times.group_by_timings_active_sg(month, day, available_timings)
    return ("active_sg.csv", timing_df)


def get_data_from_pa(month, day):
    one_pa = OnePa()
    available_timings = one_pa.get_available_timings(day)
    matched_times = TimingMatcher()
    timing_df = matched_times.group_by_timings_on_pa(month, day, available_timings)
    return ("one_pa.csv", timing_df)


def save_to_csv(df_to_save, filename):
    df_to_save.to_csv(filename, header=False)


def get_valid_month():
    month = int(input("What month do you want to search in? (should be a number) "))
    while month < 1 or month > 12:
        month = int(
            input(
                "Invalid input \n\nWhat month do you want to search in? (should be a number) "
            )
        )
    return month


def get_valid_day():
    day = int(input("What day of the month? (should be a number) "))
    while day < 1 or day > 31:
        day = int(
            input("Invalid input \n\nWhat day of the month? (should be a number) ")
        )
    return day


def get_confirmed_response(to_ask):
    while True:
        words = input(to_ask)
        confirmed = input("Are you sure? y/n ")
        if (
            confirmed == "y"
            or confirmed == "Y"
            or confirmed == "yes"
            or confirmed == "Yes"
        ):
            break
    return words


def get_yes_no_response(to_ask):
    confirmed = input(to_ask + " y/n ")
    return (
        confirmed == "y" or confirmed == "Y" or confirmed == "yes" or confirmed == "Yes"
    )


def get_user_info():
    print("Hello and welcome to Badminton Availability Check (BAC) Alpha release")
    user = get_confirmed_response(
        "what is your active sg username? (Relax, only you can see this) "
    )
    pass_ = get_confirmed_response(
        "What is your active sg password? (Relax, only you can see this) "
    )

    chrome_driver = get_confirmed_response(
        "Where did you download chromedriver too? (e.g. C:/downloads/chromedriver.exe) It should start with 'C:' and end with 'chromedriver.exe' "
    )
    return user, pass_, chrome_driver


def first_time_setup():
    with open("top_secret.txt", "r+") as f:
        line = f.readline()
        if line == "NO":
            user, password, chrome_driver = get_user_info()
            print(
                "Writing user details to top_secret.txt. \nIf you made a mistake, just go into the file and replace all the content with 'NO'\n"
            )
            f.seek(0)
            f.write("YES\n" + user + "\n" + password + "\n" + chrome_driver)


def main():
    # date = datetime.datetime(2020, 2, 14)
    first_time_setup()
    start = time.time()
    month = get_valid_month()
    day = get_valid_day()
    search_active_sg = get_yes_no_response(
        "Do you want to search active SG badminton courts?"
    )
    search_pa = get_yes_no_response("Do you want to search one PA badminton courts?")
    with cf.ThreadPoolExecutor() as executor:
        results = []
        if search_active_sg:
            results.append(executor.submit(get_data_from_active_sg, month, day))
        if search_pa:
            results.append(executor.submit(get_data_from_pa, month, day))

        for csv in cf.as_completed(results):
            print("Done searching")
            save_to_csv(
                csv.result()[1],
                str(day)
                + "_"
                + str(month)
                + "_"
                + str(datetime.date.today().year)
                + csv.result()[0],
            )

    # if search_active_sg:
    #     active_sg_slots = get_data_from_active_sg(month, day)
    #     save_to_csv(
    #         active_sg_slots,
    #         str(day)
    #         + "_"
    #         + str(month)
    #         + "_"
    #         + str(datetime.date.today().year)
    #         + "_active_sg.csv",
    #     )
    # if search_pa:
    #     pa_slots = get_data_from_pa(month, day)
    #     save_to_csv(
    #         pa_slots,
    #         str(day)
    #         + "_"
    #         + str(month)
    #         + "_"
    #         + str(datetime.date.today().year)
    #         + "_one_pa.csv",
    #     )

    end = time.time()
    print("time taken", end - start, "seconds")


if __name__ == "__main__":
    main()
