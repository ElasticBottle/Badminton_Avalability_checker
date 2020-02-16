import datetime
import time
from one_pa import OnePa
from active_sg import ActiveSG
from timing_matcher import TimingMatcher


def get_data_from_active_sg(date, time_from, time_till):
    active_sg = ActiveSG()
    available_timings = active_sg.get_available_timings(date)
    # TODO: Match the timing data from all of the courts to the timing data that we are interested in
    # TODO: return the list of data that matches in some reasonable format
    return 0


def get_data_from_pa(date, time_from, time_till):
    one_pa = OnePa()
    available_timings = one_pa.get_available_timings(19)
    # TODO: Match the timing data from all of the courts to the timing data that we are interested in
    matched_times = TimingMatcher()
    matched_times.match_timings(available_timings, time_from, time_till)
    # TODO: return the list of data that matches in some reasonable format
    return 0


def main():
    # date = datetime.datetime(2020, 2, 14)
    start = time.time()
    date = 19
    time_from = datetime.time(15, 00, 00)
    time_till = datetime.time(17, 00, 00)
    pa_slots = get_data_from_pa(date, time_from, time_till)
    active_sg_slots = get_data_from_active_sg(date, time_from, time_till)
    print(active_sg_slots, "\n\n", pa_slots)
    end = time.time()
    print("time taken", end - start)


if __name__ == "__main__":
    main()
