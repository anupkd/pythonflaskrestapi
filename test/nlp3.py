import datefinder
string_with_dates = """
                    entries are due by January 4th, 2017 at 8:00pm
                    created 01/15/2005 by ACME Inc. and associates.
                    stil month format dec 2019 and december 2020 and last month  
                    """
matches = datefinder.find_dates(string_with_dates)
for match in matches:
    print (match)