import time
import pandas as pd
import numpy as np
import datetime

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
    cities = CITY_DATA.keys()
    city = input('Kindly Choose a city from the following list:(Chicago,New York City, Washington) \n').lower()
    while city not in cities:
       try:
           city = input( 'This is not a Valid Answer, Please Choose one of the following cities:(Chicago, New York City, Washington) \n').lower()
           continue
       except KeyboardInterrupt:
           print('please choose a city \n')
           continue
    print('Thank you, now let\'s choose a Duration \n')

    # get user input for month (all, january, february, ... , june)
    months  = ('january', 'february', 'march', 'april', 'may', 'june')
    month = input('Kindly Choose a Month from January to June, or Choose all to display all data: \n').lower()
    while month != 'all' and month not in months and (int(month) >= 7 or int(month) == 0) :
        month = input('please insert a valid answer \n') .lower()
        continue
    if month in months:
                print('Great, let\'s filter by the month of', month, '\n') 

    elif month == 'all':       
                print('Great, let\'s review data of all months \n ') 

    elif 1 <= int(month) <=6:    
                datetime_object = datetime.datetime.strptime(month, "%m")
                month = datetime_object.strftime("%B")                           
                print('Great, let\'s filter by the month of ', month)
                
   #print('Now, we must choose a day to filter')
    # get user input for day of week (all, monday, tuesday, ... sunday)
    days_of_week = ['all', 'sunday', 'monday', 'tueday', 'wednesday', 'thursday', 'friday', 'saturday']
    day = input('Kindly Choose a day from the days of the week or choose all.\nDo not write your answer in shortened form and use only the day you want in full statement: \n').lower()
    while day not in days_of_week:             
          day=input('Please use the full statement: \n ').lower()
          continue

    if day in days_of_week:
       print('Great, we have all the data we need!')

    print('We have the city, month and date filters, now let\'s display some statistics')

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

# convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

# extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['popular hour'] = df['Start Time'].dt.hour
# filter by month if applicable
    if month != 'all':
            # use the index of the months list to get the corresponding int
          months = ['january', 'february', 'march', 'april', 'may', 'june']
          month = months.index(month) + 1
            # filter by month to create the new dataframe
          df = df[df['month'] == month]

        # filter by day of week if applicable
    if day != 'all':
                # filter by day of week to create the new dataframe
          df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    common_month = df['month'].mode()[0]
    common_month = months[int(df['month'].mode()[0]) - 1].title()
    print('The Most Common Month is:', common_month)

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('The Most Common Day is:', common_day)

    # display the most common start hour
    common_hour = df['popular hour'].mode()[0]
    print('The Most Common Start Hour is:', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('The Most Common Start Station is:', common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('The Most Common End Station is:', common_end_station)

    # display most frequent combination of start station and end station trip
    most_frequentTrip= df.groupby(['Start Station','End Station']).size().idxmax()
    print('The Most Frequent Trip from Start station to End station is: ', most_frequentTrip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()
    print('The Total of all trips is', total_travel,'Hours')

    # display mean travel time
    mean_travel_time = df["Trip Duration"].mean()
    print('The average of all trips is', mean_travel_time, 'hours')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender
    gender = df['Gender'].value_counts()
    print(gender)

    # Display earliest, most recent, and most common year of birth
    
    birth_year_min= int(df['Birth Year'].min())
    birth_year_max= int(df['Birth Year'].max())
    birth_year_frequent= int(df['Birth Year'].mode())
    print('The Earliest Year of Birth is', birth_year_min)
    print('The Most Recent Year of Birth is', birth_year_max)
    print('The Most Common Year of Birth is', birth_year_frequent)

    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        displayfirstdata = input('\n would you like to view the first 5 rows of the data? Enter yes or no.\n')
        if displayfirstdata == 'yes':
          print(df.head())
          interval = 0
          displayseconddata = input('\n Would you like to view the next 5 rows of the data? Enter yes or no.\n')
          while displayseconddata == 'yes':
            interval = interval + 5
            print(df.iloc[interval:interval+5])
            displayseconddata = input('\n Would you like to view the next 5 rows of the data? Enter yes or no.\n')
            continue   
                
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
