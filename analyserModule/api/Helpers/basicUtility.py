def getMonthYearFromDate(date):
    """
    When given the date in string format the function returns month and year as tuple. Month is the first value of the 
    tuple and Year is the second value of the tuple.
    """
    dateList = date.split('-')
    month = int(dateList[1])
    year = int(dateList[0])
    return (month, year)


NumDays = {
    "1": 31,
    "2": 28,
    "3": 31,
    "4": 30,
    "5": 31,
    "6": 30,
    "7": 31,
    "8": 31,
    "9": 30,
    "10": 31,
    "11": 30,
    "12": 31,
}


def getStartDateFromMonthYear(month, year):
    """
    """
    if (month < 10):
        dateStr = f"{year}-0{month}-01"
    else:
        dateStr = f"{year}-{month}-01"
    return dateStr


def getEndDateFromMonthYear(month, year):
    day = NumDays[month]
    if (month % 4 == 0):
        day = day+1
    if (month < 10):
        dateStr = f"{year}-0{month}-{day}"
    else:
        dateStr = f"{year}-{month}-{day}"
    return dateStr
