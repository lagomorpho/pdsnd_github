import time
import pandas as pd
import numpy as np
import datetime as dt

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

CITIES = ['', 'chicago', 'new york city', 'washington']
MONTHS = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
DAY_OF_WEEK = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (int) city - chosen from a list of available cities
        (int) month - chosen from a list of available months with an option for all months
        (int) day - chosen from a list of days of the week with an option for all days
    """

    print('Hello! Let\'s explore some US bikeshare data!')

    # print multiple choice options for cities
    print('Choose a city to explore:')
    for i, city in enumerate(CITY_DATA.keys(), 1):
        print ('{}) {}'.format(i, city.title()))

    # get user input for city choice
    city = 0
    while not (city >= 1 and city <= len(CITY_DATA.keys())):
        try:
            city = int(input('Choose: '))
        except ValueError:
            print("Please enter a number")

    # get user input for whether they want to filter by time
    choice_time = input('\nWould you like to filter by time? Type "yes" to add time filters: ').lower()
    if choice_time != 'yes':
        month = 0
        day = 7
    else:
        # get user input for month (all, january, february, ... , june)
        print('\nChoose a month to explore:')
        for i, month in enumerate(MONTHS):
            print ('{}) {}'.format(i, month.title()))

        month = -1
        while not (month >= 0 and month < len(MONTHS)):
            try:
                month = int(input('Choose: '))
            except ValueError:
                print("Please enter a number")

        # get user input for day of week (all, monday, tuesday, ... sunday)
        print('\nChoose a day of the week to explore:')
        for i, day in enumerate(DAY_OF_WEEK):
            print ('{}) {}'.format(i, day.title()))

        day = -1
        while not (day >= 0 and day < len(DAY_OF_WEEK)):
            try:
                day = int(input('Choose: '))
            except ValueError:
                print("Please enter a number")

    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (int) city - index of the city in the CITIES array
        (int) month - integer representation of the month
        (int) day - integer represenation of the day of the week
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(CITY_DATA[CITIES[city]])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.dayofweek

    # get the subset of data where the month matches the one chosen
    if month != 0:
        df = df[df['Month'] == month]
    
    # get the subset of data where the day of the week matches the one chosen
    if day != 7:
        df = df[df['Day of Week'] == day]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    count = len(df.index)

    # generates month-based stats if month is not filtered
    month_value_counts = dict(df['Month'].value_counts())
    if len(month_value_counts.keys()) > 1:
        # display the most common month
        most_common_month = MONTHS[df['Month'].mode()[0]].title()
        print('Most common month: {}'.format(most_common_month))

        # generates a bar graph of frequencies of months
        print('Chart of the frequencies of months:')
        for month in range(1, 7):
            if month not in month_value_counts:
                break

            percent = 100*month_value_counts[month]//count
            print("{0:12}: {1:2}".format(MONTHS[month].title(),'█'*percent))

    # generates day-based stats if day is not filtered
    day_value_counts = dict(df['Day of Week'].value_counts())
    if len(day_value_counts.keys()) > 1:
        # display the most common day of week
        most_common_dayofweek = DAY_OF_WEEK[df['Day of Week'].mode()[0]].title()
        print('\nMost common day of the week: {}'.format(most_common_dayofweek))

        # generates a bar graph of frequencies of days of the week
        print('Chart of the frequencies of days of week:')
        for day in range(0, 7):
            if day not in day_value_counts:
                break

            percent = 100*day_value_counts[day]//count
            print("{0:12}: {1:2}".format(DAY_OF_WEEK[day].title(),'█'*percent))

    # display the most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    most_common_hour = ', '.join(map(str, map(int, list(df['Hour'].mode()))))    
    print('\nMost common starting hour: {}'.format(most_common_hour))

    # generates a bar graph of frequencies of start hours
    print('Chart of the frequencies of start hours:')
    hour_value_counts = dict(df['Hour'].value_counts())
    for hour in range(0, 24):
        percent = 100*hour_value_counts[hour]//count
        print("{0:2}:00 {1:2}".format(hour,'█'*percent))

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = ', '.join(list(df['Start Station'].mode()))
    print('Most commonly used start station: {}'.format(most_common_start_station))
    
    # display most commonly used end station
    most_common_end_station = ', '.join(list(df['End Station'].mode()))
    print('Most commonly used end station: {}'.format(most_common_end_station))
    
    # display most frequent combination of start station and end station trip
    df['Station Combination'] = df['Start Station'] + ' to ' +  df['End Station']
    most_common_station_combo = ', '.join(list(df['Station Combination'].mode()))
    print('Most frequently used station combination: {}'.format(most_common_station_combo))

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df['Trip Duration'].sum()
    total_duration_h = get_human_readable_time(total_duration)
    print('Total travel duration: {}'.format(total_duration_h))

    # display mean travel time
    mean_duration = df['Trip Duration'].mean()
    mean_duration_h = get_human_readable_time(mean_duration)
    print('Average travel duration: {}'.format(mean_duration_h))

    # display longest trip
    max_duration = df['Trip Duration'].max()
    max_duration_h = get_human_readable_time(max_duration)
    print('Longest trip duration: {}'.format(max_duration_h))

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types value_counts
    print('User Type Counts:')
    for key, value in dict(df['User Type'].value_counts()).items():
            print('{0:12}: {1:8}'.format(key, value))

    # Display counts of gender if that column is present
    if 'Gender' in df.columns:
        print('\nGender Data:')
        gc = dict(df['Gender'].value_counts())

        print('\tRides:')
        for key, value in gc.items():
            print('\t{0:7}: {1:8}'.format(key, value))

        # get average duration by gender
        print('\n\tAverage Duration:')
        for gender in gc.keys():
            gender_df = df[df['Gender'] == gender]
            gender_duration_avg = get_human_readable_time(gender_df['Trip Duration'].mean())
            print('\t{0:7}: {1:8}'.format(gender, gender_duration_avg))


    # Display earliest, most recent, and most common year of birth min/max/mode
    # if that column is present
    if 'Birth Year' in df.columns:
        current_year = dt.datetime.today().year
        df['Age'] = current_year - df['Birth Year']

        print('\nAge Data:')
        print('\tEarliest Birth Year: \t{}'.format(int(df['Birth Year'].min())))
        print('\tMost Recent Birth Year: {}'.format(int(df['Birth Year'].max())))

        most_common_year = ', '.join(map(str, map(int, list(df['Birth Year'].mode()))))
        print('\tMost Common Birth Year: {}'.format(most_common_year))

        print('\tOldest Rider: \t\t{}'.format(int(df['Age'].max())))
        print('\tYoungest Rider: \t{}'.format(int(df['Age'].min())))
        print('\tAvergae Rider Age: \t{}'.format(round(df['Age'].mean())))


        
    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)



def get_human_readable_time(seconds):
    """
    Generates a human readable string of time. Converts seconds into a string describing a length of time including days, hours, minutes, and seconds. Minutes and seconds are always included. Days and hours are prepended if the duration included them.

    Args:
        (int) seconds - the number of seconds to convert
    Returns:
        timestring - A verbose human readable string describing a length of time
    """
    start_time = time.time()
    timestring = ''
    remainder = seconds

    days = int(remainder // (60*60*24))
    remainder -= days*60*60*24

    hours = int(remainder // (60*60))
    remainder -= hours*60*60

    minutes = int(remainder // 60)
    remainder -= minutes*60

    secs = round(remainder, 2)
    
    timestring = "{} minutes and {} seconds".format(minutes, secs)
    if hours > 0:
        timestring = "{} hours, ".format(hours) + timestring
    if days > 0:
        timestring = "{} days, ".format(days) + timestring

    return timestring


def get_human_readable_choice(city, month, day):
    """
    Generates a string describing the data that will be explored depending on the arguments
    """
    current_data_string = "You have selected to view data from " + CITIES[city].title()
    if month != 0:
        current_data_string += " in " + MONTHS[month].title()

    if day != 7:
        current_data_string += " on a " + DAY_OF_WEEK[day].title()

    return current_data_string


def step_through_data(df):
    """
    Steps through raw data of a Pandas Dataframe. The rows of data are converted to a dict and then printed to the screen five rows at a time. This continues until "no" is entered as input

    Args:
        df - Pandas DataFrame containing city data
    """
    step_continue = 'yes'
    index = 0
    while step_continue != 'no':
        for i, row in df[index:index+5].iterrows():
            print(dict(row))

        step_continue = input('\nContinue viewing raw data? Type "no" to exit: \n').lower()
        index += 5


def generate_stats(city, month, day):
    """
    Generates statistics for the chosen city, month, and day

    Args:
        (int) city - index of the city in the CITIES array
        (int) month - integer representation of the month
        (int) day - integer represenation of the day of the week
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    print('-'*40)
    df = load_data(city, month, day)

    print(get_human_readable_choice(city, month, day))

    time_stats(df)
    station_stats(df)
    trip_duration_stats(df)
    user_stats(df)

    return df


def unit_test():
    """
    Runs through all potential choices for city, month, and day and generates stats
    """
    for city in range(1, 4):
        for month in range(0, 7):
            for day in range(0, 8):
                generate_stats(city, month, day)


def debug():
    generate_stats(3,0,7)


def main():
    """
    Manages input flow, prompting user for how they will view their data
    Gives the option to view raw data
    Gives the option to restart the data exploration
    """    
    while True:
        city, month, day = get_filters()

        df = generate_stats(city, month, day)

        # step through data
        step_through = input('\nWould you like to step through raw data? Type "yes" to step through: \n')
        if step_through.lower() == 'yes':
            step_through_data(df)

        # restart
        restart = input('\nWould you like to restart? Type "yes" to restart.\n')
        if restart.lower() != 'yes':
            break


if __name__ == '__main__':
	main()
