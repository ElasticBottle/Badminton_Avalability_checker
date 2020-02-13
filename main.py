import datetime


def get_data_from_active_sg(date, time):
    return 0


def get_data_from_pa(date, time):
    return 0


def main():
    date = datetime.datetime(2020, 2, 14)
    time = datetime.time(15, 00, 00)
    active_sg_slots = get_data_from_active_sg(date, time)
    pa_slots = get_data_from_pa(date, time)
    print(active_sg_slots, "/n/n", pa_slots)


if __name__ == "__main__":
    main()
