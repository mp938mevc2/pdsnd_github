import time
from datetime import timedelta
from os import system, name
import pandas as pd
import numpy as np

'''
CITY_DATA is a dictionary that is used to translate the city name, entered in the 
get_filters function to the file name where the raw data is.
'''
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    This function starts by clearing the screen to prepare for the bikeshare prompt
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    system('cls' if name == 'nt' else 'clear')
    print('Hello! Let\'s explore some US bikeshare data!')
    '''
    The input for city, month, and day is requested via three separate while loops that continue 
    looping until a valid entry is made. To account for mismatched capitalization, the input is 
    changed to lower case on entry.
    '''
    while True:
        city = input('We have data for Chicago, New York City, and Washington. Which city\'s data would you like to look at?  ').lower()
        if city == "chicago" or city == 'new york city' or city == 'washington':
            break
        else:
            continue

    while True:
        month = input('\nWhat month would you like to see data for? Enter a month January through June or all):  ').lower()
        if month == 'january' or month == 'february' or month == 'march' or month == 'april' or month == 'may' or month == 'june' or month == 'all':
            break
        else:
            continue

    while True:
        day = input('\nAnd for which day of the week would you like to see? Enter a day name or all:  ').lower()
        if day == 'all' or day == 'monday' or day == 'tuesday' or day == 'wednesday' or day == 'thursday' or day == 'friday' or day == 'saturday' or day == 'sunday':
            break
        else:
            continue

    # A bicycle rider border between the input data and the output data!
    print('\n' + '            o           ' * 4)
    print('           /\\\\          ' * 4)
    print('         _ \\-<          ' * 4)
    print('________(_)/(_)_________' * 4 + '\n')
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
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.day_name()

    # If a specific month is chosen, this removes all other months from the dataframe 
    if month != 'all':
        '''
        Create a list with months in order to use their index (+1) because the output
        of the the month df above is numeric.
        '''
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1
        df = df[df['Month'] == month]

    # If a specific day is chosen, this removes all other days from the dataframe 
    if day != 'all':
        df = df[df['Day of Week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel.
    
    Args:
        (df) df - dataframe with the data modified based on user entry.
    Returns:
        N/A - print output to screen only
    
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    ''' 
    Used mode on the dataframe calling the month column to get the month with the highest
    count of users and used a month list again for the integer to name translation.
    '''
    common_month = df['Month'].mode()[0]-1
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    common_month = months[common_month].title()
    print('The bikeshare\'s busiest month was {}.'.format(common_month))

    ''' 
    Used mode on the dataframe calling the day of week column to get the day of the week 
    with the highest count of users.
    '''

    common_day = df['Day of Week'].mode()[0]
    print('The bikeshare\'s busiest days were {}s.'.format(common_day))
    
    ''' 
    Used mode on the dataframe calling the start time column and used date time module 
    to get the hour with the highest count of users.
    '''

    common_hour = df['Start Time'].dt.hour.mode()[0]
    print('The bikeshare was used most during the {}:00 hour.'.format(common_hour))
    
    print(f'\nThis took {time.time() - start_time:.5f} seconds.')
    print('\n' + '_' * 96 + '\n')

def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.
    
    Args:
        (df) df - dataframe with the data modified based on user entry.
    Returns:
        N/A - print output to screen only
    
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Used mode on the start station column to get the most common starting point
    most_start_station = df['Start Station'].mode()[0]
    print('The station with the most trip originations was ' + most_start_station)

    # Used mode on the end station column to get the most common ending point
    most_end_station = df['End Station'].mode()[0]
    print('The most frequent destination station was ' + most_end_station)

    # Used value_count with two arguments to get the pair of stations that are most used in conjunction with each other
    # value_counts requires higher version of Python

    try:
        most_station_combo = df.value_counts(['Start Station', 'End Station']).idxmax()
        print('The stations that were the most frequent origination and destination pair are',most_station_combo[0], 'and', most_station_combo[1] + '.')
    except:
        most_station_combo = df.groupby(['Start Station', 'End Station']).count().idxmax()
        print('The stations that were the most frequent origination and destination pair are',most_station_combo[0][0], 'and', most_station_combo[0][1] + '.')
        
    print(f'\nThis took {time.time() - start_time:.5f} seconds.')
    print('\n' + '_' * 96 + '\n')

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.
    
    Args:
        (df) df - dataframe with the data modified based on user entry.
    Returns:
        N/A - print output to screen only
    
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Used sum method to total all trips
    total_travel = df['Trip Duration'].sum()
    print('The total amount of travel time for all trips during the selected period is ' + str(timedelta(seconds = int(total_travel))))
 
    # Used mean method to determine the average duration of all trips
    mean_travel = df['Trip Duration'].mean()
    print('During the selected time period the average trip was ' + str(timedelta(seconds = int(mean_travel))) + '.')

    print(f'\nThis took {time.time() - start_time:.5f} seconds.')
    print('\n' + '_' * 96 + '\n')


def user_stats(df):
    """
    Displays statistics on bikeshare users on three fields: bikeshare membership, gender, and age.
    
    Args:
        (df) df - dataframe with the data modified based on user entry.
    Returns:
        N/A - print output to screen only
    
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # For loop to interate through the user types and print out both the index and the value for the index.
    user_types = df['User Type'].value_counts()
    for i in range (2):
        print('Of the bikeshare users during this time period, {} were {}s.'.format(user_types.iloc[i], user_types.index[i].lower()))
    
    '''
    Because there is no gender and age data for Washington, try and except was used to skip when Washington 
    was chosen. A for loop interates through the gender types and prints out both the index and the value 
    for the index.
    '''

    try:
        user_gender = df['Gender'].value_counts()
        print('\n')
        for i in range (2):
            print('Of the bikeshare users during this time period, {} were {}s.'.format(user_gender.iloc[i], user_gender.index[i].lower()))
    except: 
        print('\nThere is no gender data for Washington')
    
    # Ages are calculated by subtracting the year of the data from the year of birth.
    try:
        user_yob = df['Birth Year']
        young = 2017 - int(user_yob.max())
        eldest = 2017 - int(user_yob.min())
        mostyob = 2017 - int(user_yob.mode()[0])
        
        print('\n\nThe range in ages of people using the bikeshare at the time this data was collected is {} to {}.'.format(young, eldest))
        print('The most common age was {}.\n'.format(mostyob))
    except:
        print('There is no age data for Washington')
    
    print(f'\nThis took {time.time() - start_time:.5f} seconds.')
    print('\n' + '            o           ' * 4)
    print('           /\\\\          ' * 4)
    print('         _ \\-<          ' * 4)
    print('________(_)/(_)_________' * 4 + '\n')


def raw_data(df):
    """
    Displays the raw data five lines at a time if the user replies y to the input query.
    
    Args:
        (df) df - dataframe with the data modified based on user entry.
    Returns:
        N/A - print output to screen only
    """
    
    '''
    Initial check if the user wants to view the raw data. If y, the head method is used to get the first five 
    lines of data from the df
    '''

    check1 = 'y'
    check1 = input("\nWould you like to view some of the raw data? (y/n)  ").lower()
    print(check1)
    if check1 == 'y':
        print(df.head(),'\n')
    else: 
        return

    '''
    Looped check if the user wants to view more raw data. The if statement has a double condition, one if the 
    user wants more data, and the second to check if all the data has already been retrieved.The index (i) for 
    the loop is incremented by five in the if statement and five lines of data a printed at a time.
    '''
    
    i = 5
    check2 = 'y'
    while check2 == 'y':
        check2 = input("Do you wish to view more raw data? (y/n)  ").lower()
        if check2 == 'y' and i <= df.shape[0] + 1:
            print(df[i:i+5],'\n')
            i += 5
            continue
        else:
            break
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)
        
        restart = input('\nWould you like to look at data for another city, month, or day? (y/n)  ')
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()
