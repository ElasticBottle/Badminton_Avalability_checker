import datetime
import requests
from bs4 import BeautifulSoup


def active_sg():
    LOGIN_URL = "https://members.myactivesg.com/auth/signin"

    REQUEST_URL = "https://members.myactivesg.com/facilities/view/activity/18/venue/292?time_from=1581609600"

    payload = {"email": "s9909427c", "password": "however200"}

    with requests.Session() as session:
        post = session.post(LOGIN_URL, data=payload)
        print(post, "\n\n")
        r = session.get(REQUEST_URL)
        soup = BeautifulSoup(r.content, "html.parser")
        results = soup.find(id="formTimeslots")
        print(results.prettify())


def get_data_from_active_sg(date, time_from, time_till):
    # Todo: Get timing data from all of active sg badminton courts
    # Todo: Match the timing data from all of the courts to the timing data that we are interested in
    # Todo: return the list of data that matches in some reasonable format
    return 0


def get_data_from_pa(date, time_from, time_till):
    # Todo: Get timing data from all of pa badminton courts
    # Todo: Match the timing data from all of the courts to the timing data that we are interested in
    # Todo: return the list of data that matches in some reasonable format
    return 0


def main():
    date = datetime.datetime(2020, 2, 14)
    time_from = datetime.time(15, 00, 00)
    time_till = datetime.time(17, 00, 00)
    active_sg_slots = get_data_from_active_sg(date, time_from, time_till)
    pa_slots = get_data_from_pa(date, time_from, time_till)
    print(active_sg_slots, "\n\n", pa_slots)
    active_sg()


if __name__ == "__main__":
    main()
