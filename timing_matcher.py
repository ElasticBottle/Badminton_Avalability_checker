import enum
import datetime
import pandas as pd


class Match(enum.Enum):
    FULL = enum.auto()
    PARTIAL = enum.auto()
    NO_MATCH = enum.auto()


class TimingMatcher:
    def __get_court_match(self, court_name, court_timing, time_from, time_till):
        # TODO: match the timing of the court with the specified timing
        return Match.NO_MATCH

    def match_timings(self, available_timings, time_from, time_till):
        court_matches = {Match.FULL: [], Match.PARTIAL: []}
        for court_name, court_timing in available_timings.items():
            court_match = self.__get_court_match(
                court_name, court_timing, time_from, time_till
            )

            # Adds in partial and full match for selected timings
            if court_match != Match.NO_MATCH:
                court_match_list = court_matches.get(court_match)
                court_match_list.append(court_name)
                court_matches.update({court_match, court_match_list})
        return court_matches

    def group_by_timings_active_sg(self, month, day, available_timings):

        timing_dict = dict()
        for court_name, court_timings in available_timings.items():
            for timing in court_timings:
                current_courts_at_this_timing = timing_dict.get(timing, [])
                current_courts_at_this_timing.append(court_name)
                timing_dict.update({timing: current_courts_at_this_timing})
        timing_df = pd.DataFrame.from_dict(timing_dict, orient="index")
        timing_df.index = pd.to_datetime(timing_df.index)
        timing_df.index = timing_df.index.map(
            lambda t: t.replace(year=datetime.date.today().year, month=month, day=day)
        )
        timing_df = timing_df.sort_index()
        print(timing_df)
        return timing_df

    def _split_timing_into_hourly(self, timings, month, day):
        year = datetime.date.today().year

        start = pd.to_datetime(timings[0]).replace(year=year, month=month, day=day)
        end = pd.to_datetime(timings[1]).replace(year=year, month=month, day=day)
        diff = end - start
        num_hours = divmod(diff.seconds, 3600)[0]

        if num_hours == 1:
            return [start]
        return [
            start,
            (start + datetime.timedelta(hours=1)).replace(
                year=year, month=month, day=day
            ),
        ]

    def group_by_timings_on_pa(self, month, day, available_timings):
        timing_dict = dict()
        for court_name, court_timing in available_timings.items():
            for timing in court_timing:
                timing = timing.split(" - ")
                timing = self._split_timing_into_hourly(timing, month, day)
                for time in timing:
                    current_courts_at_this_timing = timing_dict.get(time, [])
                    current_courts_at_this_timing.append(court_name)
                    timing_dict.update({time: current_courts_at_this_timing})

        timing_df = pd.DataFrame.from_dict(timing_dict, orient="index")
        timing_df = timing_df.sort_index()
        print(timing_df)
        return timing_df
