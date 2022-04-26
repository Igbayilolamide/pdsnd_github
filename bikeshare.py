import time
import pandas as pd
import numpy as np
import sys

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
cities = ['chicago','new york city','washington','newyork','new york']
months = ['all','january','february','march','april','may','june']
dow = ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']

def call_exit():
    """ Exits the session """
    sys.exit("..Exiting session..")

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')
    print('We have data for Chicago, New York City and Washington.')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = str(input("What city do you want to explore? ")).lower()
        if city not in cities:
            print("Entered city is invalid or not in the list. ")
            confirmation = input("Would you like to retry? Type yes or no to exit: ")
            if confirmation == 'yes':
                continue
            else:
                call_exit()
        else:
            break

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = str(input("\nEnter a month between January through June or all to view all months: ")).lower()
        if month not in months:
            print("You've entered an invalid month or one which data is unavailable, Try again. ")
            confirmation = input("Would you like to retry? Type yes or no to exit: ")
            if confirmation == 'yes':
                continue
            else:
                call_exit()
        else:
            break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = str(input("\nWhat day of the week do you require data? e.g. all, monday: ")).lower()
        if day not in dow:
            print("You've entered an invalid day, Try again. ")
            confirmation = input("Would you like to retry? Type yes or no to exit: ")
            if confirmation == 'yes':
                continue
            else:
                call_exit()
        else:
            break


    print('-'*40)
    return city, month, day

def confirm_data(city,month,day):
    """ Function prints requested data and exits if user says no"""
    print("\nYou have requested Bikeshare's data for: \nCity: {}, Month: {}, Day: {} ".format(city.title(),month.title(),day.title()))
    ask = input("\nDo you wish to continue? Enter yes to continue, no to exit:")
    if ask != 'yes':
        call_exit()

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
    # confirms your input
    confirm_data(city,month,day)
    
    # handles different inputs for new york
    if city in ['newyork','new york','new york city']:
        city = 'new york city'

    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Day of week'] = df['Start Time'].dt.day_name()
    # at this point the df contains all the data without any filter

    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month)

        # filter by month to create the new dataframe
        df = df[df['Month'] == month]
    # at this point df is filtered by months

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['Day of week'] == day.title()]
    # at this point df is filtered by month and day

    return df
#function to capitalize first letter of city

def time_stats(df):

    """\nDisplays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df['Month'].mode()[0]
    print("\nThe most common month for Bikeshare in {} is: {} \n".format(city,common_month))

    # TO DO: display the most common day of week
    common_day = df['Day of week'].mode()[0]
    print("\nThe most common day of the week for Bikeshare in {} is: {} \n".format(city,common_day))

    # TO DO: display the most common start hour
    df['Hours'] = df['Start Time'].dt.hour
    common_start = df['Hours'].mode()[0]
    print("\nThe most common start hour for Bikeshare in {} is: {} \n".format(city,common_start))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):

    """\nDisplays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_station = df['Start Station'].mode()[0]
    print("\nThe most popular start station for Bikeshare in {} is: {} \n".format(city,common_station))

    # TO DO: display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print("\nThe most popular end station for Bikeshare in {} is: {} \n".format(city,common_end))

    # TO DO: display most frequent combination of start station and end station trip
    # creat a df for each combination of start and end stations
    new_df = pd.DataFrame(df['Start Station'] + "," + df['End Station'] , columns = ['new'])
    start,end = new_df['new'].mode()[0].split(",")
    print("\nThe most popular stations to start and end in {} are '{}' and '{}' respectively \n".format(city,start,end))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):

    """\nDisplays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    df['End Time'] = pd.to_datetime(df['End Time'])
    # creates a new column that stores difference of each trip's start and end time
    df['diff'] = (df['End Time'] - df['Start Time'])#/np.timedelta64(1,'s')
    total_time = df['diff'].sum()
    print("\nThe total trip duration is: {} ".format(total_time))

    # TO DO: display mean travel time
    average_time = df['diff'].mean()
    print("\nThe average trip duration is: {} ".format(average_time))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """\nDisplays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print("\nDetails of user types for {} is:\n{}".format(city,user_types))

    # TO DO: Display counts of gender
    try:
        gender = df['Gender'].value_counts()
        print("\nCount of users in {} based on gender:\n {}".format(city,gender))
    except KeyError:
        print("\nNo gender details for Washington\n")

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        earliest_year = df['Birth Year'].min()
        recent_year = df['Birth Year'].max()
        common_year = df['Birth Year'].mode()[0]
        print("\nFind below details about the age of users in {}:\n".format(city))
        print("The oldest user(s) was/were born in: {}\n".format(earliest_year))
        print("\nThe youngest user(s) was/were born in: {}\n".format(recent_year))
        print("\nMajority of the users were born in: {}\n".format(common_year))

    except KeyError:
        print("\nNo Date of Birth details for Washington\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#function that loops through df returning 5 records
def five_records(df):
    """ Function that recturns five records from the dataframe """
    # start of index
    i = 0
    # end of index
    n = 5
    while True:
        try:
            raw_data = input("\nWould you like to see 5 lines of raw data? Enter yes or no.\n")
            if raw_data.lower() == 'no':
                break
            elif raw_data.lower() not in ['yes','no']:
                print("\nOops!, you entered an invalid value, Try again ")
                continue
            else:
                #prints all columns and rows from i to n
                print(df[:][i:n])
                i += 5
                n += 5
        except:
            print("\nYou have reached the end of the file!")
            break

def main():
     while True:
        global city
        city, month, day = get_filters()
        df = load_data(city, month, day)
        city = city.title()
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        five_records(df)


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            call_exit()


if __name__ == "__main__":
	main()
