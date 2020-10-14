from datetime import date


class Year:
    def __init__(self, name, start_calendar_year):
        self.name = name
        self.start_date = date(month=6, day=1, year=start_calendar_year)
        self.end_date = date(month=5, day=31, year=start_calendar_year + 1)

    def __repr__(self):
        return '<Year {}>'.format(self.name)

    def __contains__(self, date):
        return date >= self.start_date and date <= self.end_date


class Years:

    _all_years = [Year(name, start_year)
                  for name, start_year
                  in [('1G', 2013),
                      ('2G', 2014),
                      ('3G', 2015),
                      ('4G', 2016),
                      ('5G', 2017),
                      ('6G', 2018),
                      ('3B', 2019),
                      ('4B', 2020), ]]

    @staticmethod
    def year_names():
        return [y.name for y in Years._all_years][::-1]

    @staticmethod
    def get(date):
        for year in Years._all_years:
            if date in year:
                return year.name
        else:
            return 'Unnamed Year ({})'.format(date.year)
