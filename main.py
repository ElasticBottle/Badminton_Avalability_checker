import datetime
import time
import pandas as pd
from one_pa import OnePa
from active_sg import ActiveSG
from timing_matcher import TimingMatcher
import concurrent.futures as cf


def get_data_from_active_sg(month, day):
    """
    Retrieves a dictionary of available timing from active sg badminton courts and converts it to a nice dataframe

    Args:
        month (int): Correspond to the month to search in. Only affects the value in dataframe, doesn't affect the month being searched
        dat (int): Corresponds to the day of the month to search in

    Returns:
        tuple(string, Dataframe): String contains the identifier for the Dataframe
            Dataframe contains the details of available courts, indexed by time
    """
    active_sg = ActiveSG()
    available_timings = active_sg.get_available_timings(day)
    matched_times = TimingMatcher()
    timing_df = matched_times.group_by_timings_active_sg(month, day, available_timings)
    return ("active_sg.csv", timing_df)


def get_data_from_pa(month, day):
    """
    Retrieves a dictionary of available timing from one pa badminton courts and converts it to a nice dataframe

    Args:
        month (int): Correspond to the month to search in. Only affects the value in dataframe, doesn't affect the month being searched
        dat (int): Corresponds to the day of the month to search in

    Returns:
        tuple(string, Dataframe): String contains the identifier for the Dataframe
            Dataframe contains the details of available courts, indexed by time
    """
    one_pa = OnePa()
    available_timings = one_pa.get_available_timings(day)
    matched_times = TimingMatcher()
    timing_df = matched_times.group_by_timings_on_pa(month, day, available_timings)
    return ("one_pa.csv", timing_df)


def save_to_csv(df_to_save, filename):
    df_to_save.to_csv(filename, header=False)


def get_num_in_range(min_num, max_num, to_ask, error_msg):
    num = int(input(to_ask))
    while num < min_num or num > max_num:
        num = int(input(error_msg))
    return num


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
    month = get_num_in_range(
        1,
        12,
        "What month do you want to search in? (should be a number) ",
        "Invalid input \n\nWhat month do you want to search in? (should be a number) ",
    )
    day = get_num_in_range(
        1,
        31,
        "What day of the month? (should be a number) ",
        "Invalid input \n\nWhat day of the month? (should be a number) ",
    )
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
