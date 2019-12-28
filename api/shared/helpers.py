import calendar


def get_date_range(year, month, separator):
    first_day_of_month = '01'
    start_date = year + separator + month + separator + first_day_of_month

    last_day_of_month = str(calendar.monthrange(int(year), int(month))[1])
    end_date = year + separator + month + separator + last_day_of_month

    return start_date, end_date
