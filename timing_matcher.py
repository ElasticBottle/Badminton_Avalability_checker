import enum


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

    def group_by_timings(self, available_timings):
        # TODO: group the courts into timing buckets rather than by court name
        pass
