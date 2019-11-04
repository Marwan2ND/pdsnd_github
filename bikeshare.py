import time
import pandas as pd
import numpy as np
import json
def user_input(message, user_list):
    """
    An utility function to obtain user specific input value
    Args:
        (str) message - an information message for a particular request
    Returns:
        (str) user_data - requested data from user
    """

    while True:
        user_data = input(message).lower()
        if user_data in user_list:
            break
        if user_data == 'all':
            break
    
    return user_data


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

CITIES = ['chicago', 'new york', 'washington']

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']

DAYS = ['sunday', 'monday', 'tuesday', 'wednesday', \
        'thursday', 'friday', 'saturday' ]

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
 
    city = input('\nPlease enter one of the following cities: Chicago, New York, Washington\n').lower()

    while True:
       if city in CITIES:
           break
       else:
           city = input('Enter Correct city: ').lower()
            
    # get user input for month (all, january, february, ... , june)
    
    month = user_input('Please enter one of the following months: january, february, march, april, may, june, OR all\n', MONTHS)


    

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = user_input('Please enter one of the following weekdays: monday, tuesday, wednesday, thursday, friday, saturday , sunday, OR all\n', DAYS)

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

    # extract month and day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        month =  MONTHS.index(month) + 1
        df = df[ df['month'] == month ]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[ df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_month = df['month'].value_counts().idxmax()
    print("The most common MONTH is :", most_month)

    # display the most common day of week
    most_day_of_week = df['day_of_week'].value_counts().idxmax()
    print("The most common DAY of week is :", most_day_of_week)

    # display the most common start hour

    most_start_hour = df['hour'].value_counts().idxmax()
    print("The most common start hour is :", most_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# Displays statistics station stats
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_start_station = df['Start Station'].value_counts().idxmax()
    print("The most commonly used start station :", most_start_station)

    # display most commonly used end station
    most_end_station = df['End Station'].value_counts().idxmax()
    print("The most commonly used end station :", most_end_station)

    # display most frequent combination of start station and end station trip
    most_start_end_station = df[['Start Station', 'End Station']].mode().loc[0]
    print("The most commonly used start station and end station : {}, {}"\
            .format(most_start_end_station[0], most_start_end_station[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# Displays statistics trip duration stats
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()
    print("Total travel time :", total_travel)

    # display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print("Mean travel time :", mean_travel)

    # display mean travel time
    max_travel = df['Trip Duration'].max()
    print("Max travel time :", max_travel)
    
    # display min travel time
    min_travel = df['Trip Duration'].min()
    print("min travel time :", min_travel)

    
    # display mode travel time
    mode_travel = df['Trip Duration'].mode()
    print("Mode travel time :", mode_travel)
    
    # display median travel time
    median_travel = df['Trip Duration'].median()
    print("median travel time :", median_travel)

    print('-'*40)

    print("\n")
    print("Travel time for each user type:\n")
    # display the total trip duration for each user type
    group_by_user = df.groupby(['User Type']).sum()['Trip Duration']
    for index, user_trip in enumerate(group_by_user):
        print("  {}: {}".format(group_by_user.index[index], user_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Counts of user types:\n")
    user_counts = df['User Type'].value_counts()
    # iteratively print out the total numbers of user types 
    for index, user_count in enumerate(user_counts):
        print("  {}: {}".format(user_counts.index[index], user_count))
    

    if 'Gender' in df.columns:
        user_stats_gender(df)

    if 'Birth Year' in df.columns:
        user_stats_birth(df)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats_gender(df):
    """Displays statistics of analysis based on the gender of bikeshare users."""

    # Display counts of gender
    print("Counts of gender:\n")
    gender_counts = df['Gender'].value_counts()
    # iteratively print out the total numbers of genders 
    for index,gender_count   in enumerate(gender_counts):
        print("  {}: {}".format(gender_counts.index[index], gender_count))
    
    print()
    print('-'*40)

def user_stats_birth(df):
    """Displays statistics of analysis based on the birth years of bikeshare users."""

    # Display earliest, most recent, and most common year of birth
    birth_year = df['Birth Year']
    
    # the most common birth year
    most_year = birth_year.value_counts().idxmax()
    print("The most common birth year:", most_year)
    
    # the most recent birth year
    most_recent = birth_year.max()
    print("The most recent birth year:", most_recent)
    
    # the most earliest birth year
    earliest_year = birth_year.min()
    print("The most earliest birth year:", earliest_year)
        
    # the most median birth year
    median_year = birth_year.median()
    print("The median birth year:", median_year)


def table_stats(df, city):
    """Displays statistics on bikeshare users."""
    print('\nCalculating Dataset Stats...\n')
    
    # counts the number of missing values in the entire dataset
    number_of_missing = np.count_nonzero(df.isnull())
    print("The number of missing values in the {} dataset : {}".format(city, number_of_missing))

    # counts the number of missing values in the User Type column
    number_of_nonzero = np.count_nonzero(df['User Type'].isnull())
    print("The number of missing values in the \'User Type\' column: {}".format(number_of_missing))

def display_data(df):
    """Displays raw bikeshare data."""
    row_length = df.shape[0]

    # iterate from zero to the number of rows in steps of 5
    for i in range(0, row_length, 5):
        
        yes = input('\nDo you want to see 5 lines of raw data? Enter: \'yes\' OR \'no\'\n> ')
        if yes.lower() != 'yes':
            break
        
        # retrieve and convert data to json format
        # split each json row data 
        row_data = df.iloc[i: i + 5].to_json(orient='records', lines=True).split('\n')
        for row in row_data:
            # pretty print each user data
            parsed_row = json.loads(row)
            json_row = json.dumps(parsed_row, indent=2)
            print(json_row)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        table_stats(df, city)

        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()