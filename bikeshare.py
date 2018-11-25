import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = 0
    while city != 'chicago' and city != 'washington' and city != 'new york city':
        city = input('Enter city name (Chicago, New York City, or Washington) to explore its data: ').lower()
        if city != 'chicago' and city != 'washington' and city != 'new york city':
            print('Invalid city. Try again!')

    # get user input for month (all, january, february, ... , june)
    month_list = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    month = 0
    while month not in month_list:
        month = input('Which month, from January - June would you like to fliter by? Or choose "all": ').lower()
        if month not in month_list:
            print('Invalid entry. Select a month from January - June or "all".')
    
    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = 0
    while day not in days:
        day = input('Which day of the week would you like to fliter by? Or choose "all": ').lower()
        if day not in days:
            print('Invalid entry. Select a day of the week or "all".')

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour_of_day'] = df['Start Time'].dt.hour

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('Most common month for rentals: {}'.format(popular_month))

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most common day for rentals: {}'.format(popular_day))

    # display the most common start hour
    popular_hour = df['hour_of_day'].mode()[0]
    print('Most common hour for rentals: {}'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    top_ss = df['Start Station'].mode()[0]
    print('Most common start station: {}'.format(top_ss))

    # display most commonly used end station
    top_es = df['End Station'].mode()[0]
    print('Most common end station: {}'.format(top_es))

    # display most frequent combination of start station and end station trip
    top_start_end = (df['Start Station'] + ', ' + df['End Station']).mode()[0]
    print('Most common start/end route: {}'.format(top_start_end))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    # display total travel time
    df['duration'] = df['End Time'].sub(df['Start Time'], axis=0)
    print('Total travel time: {}'.format(df['duration'].sum()))
    # display mean travel time
    print('Mean travel time: {}'.format(df['duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """
    Displays statistics on bikeshare users. Will display output for lack of birth year
    or gender data in dataset.
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('User Types: {}'.format(df['User Type'].value_counts()))
    # Display counts of gender
    while True:
        try:
            print('User Genders: {}'.format(df['Gender'].value_counts()))
            break
        except:
            print('No gender data.')
            break

    # Display earliest, most recent, and most common year of birth
    while True:
        try:
            print('Earliest birth year of users: {}'.format(int(df['Birth Year'].min())))
            print('Most recent birth year of users: {}'.format(int(df['Birth Year'].max())))
            print('Most common birth year of users: {}'.format(int(df['Birth Year'].mode()[0])))
            break
        except:
            print('No birth year data')
            break
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """ 
    Allows user to view raw entries for selected data, 5 lines at a time. User can see additional lines
    by pressing enter. 'No' or 'n' will exit the raw data function.
    """
    
    df = df.drop(['month', 'day_of_week', 'hour_of_day', 'duration'], axis=1)
    df = df.reset_index()
    i=0
    y=0
    z = input('Would you like to see the raw data from this set? yes or no: ').lower()
    print('-'*40)
    if z == 'yes' or z =='y':
        while y < 5:
            print('\n'*2)
            print(df.loc[[i]])
            i+=1
            y+=1
            if y > 4:
                print('-'*40)
                x = input('Press ENTER to see next 5 entries, or type "no" to exit: ').lower()
                print('-'*40)
                if x != 'no' and x != 'n':
                    y = 0
                else:
                    z = 'no'
                    break
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        next_stat = input('Press ENTER to continue to "Most Popular Stations and Trip" data...')
        print('-'*40)
        station_stats(df)
        next_stat = input('Press ENTER to continue to "Trip Duration" data...')
        print('-'*40)
        trip_duration_stats(df)
        next_stat = input('Press ENTER to continue to "User Stats" data...')
        print('-'*40)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        if restart != 'yes' and restart != 'y':
            break


if __name__ == "__main__":
	main()
