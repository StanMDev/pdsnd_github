import datetime
import time
import pandas as pd
import numpy as np
import os

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

    #clear screen before start
    os.system('clear')
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    input_ok = 0
    city = input("Please enter the city (chicago, new york city, washington) you would like to analyse: ").lower()
    
    while not input_ok == 1:
        if city == 'stop':
            exit()
        else:
            if city not in ('chicago', 'new york city', 'washington'):
                print ("Sorry, your entry does not match the available cities. Try again or enter stop to exit.")
                city = input("Please enter the city (chicago, new york city, washington) you would like to analyse: ").lower()
            else:
                input_ok = 1
    

    # TO DO: get user input for month (all, january, february, ... , june)
    input_ok = 0
    month = input("Please enter the month (all, january, february, ... , june) you would like to analyse: ").lower()
    
    while not input_ok == 1:
        if month == 'stop':
            exit()
        else:
            if month not in ('all','january','february','march','april','may','june'):
                print ("Sorry, your entry is not valid. Try again or enter stop to exit.")
                month = input("Please enter the month (all, january, february, ... , june) you would like to analyse: ").lower()
            else:
                input_ok = 1

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    input_ok = 0
    day = input("Please enter the weekday (all, Mon, Tue, Wed, Thu, Fri, Sat, Sun ) you would like to analyse: ").lower()
    
    while not input_ok == 1:
        if day == 'stop':
            exit()
        else:
            if day not in ('all', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'):
                print ("Sorry, your entry is not valid. Try again or enter stop to exit.")
                day = input("Please enter the weekday (all, Mon, Tue, Wed, Thu, Fri, Sat, Sun ) you would like to analyse: ").lower()
            else:
                input_ok = 1


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
    filename = CITY_DATA[city]
    df = pd.read_csv(filename) 

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    #weekday will use 0 for monday and 6 for sunday
    df['day_of_week'] = df['Start Time'].dt.weekday

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # Add count for combination of Start- and End-Station for later calculation  #LinkRef: 1
    df['CountStationCombo']=df.groupby(['Start Station', 'End Station'])['End Station'].transform('size')


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january','february','march','april','may','june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month] 

    # filter by day of week if applicable
    if day != 'all':
        # get the index for a weekday
        days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
        day = days.index(day)        
        
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]-1 
    months = ['january','february','march','april','may','june']
    print('Most common Month:', months[popular_month])

    # TO DO: display the most common day of week
    popular_day = df['day_of_week'].mode()[0] 
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    print('Most common Day:', days[popular_day])

    # TO DO: display the most common start hour
    popular_hour = df['hour'].mode()[0] 
    print('Most Frequent Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start = df['Start Station'].mode()[0] 
    print('Most commonly used start station:', popular_start)

    # TO DO: display most commonly used end station
    popular_end = df['End Station'].mode()[0] 
    print('Most commonly used end station:', popular_end)

    # TO DO: display most frequent combination of start station and end station trip
    # Count for Combination already done in function load_data #LinkRef 2
    print('Most frequent combination of start station and end station: {} --> {}' \
        .format( df.loc[df['CountStationCombo'].idxmax()][4], df.loc[df['CountStationCombo'].idxmax()][5]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time 
    # Data stored as seconds will be converted to more meaning units #LinkRef 3
    traveltime = int(df['Trip Duration'].sum())
    print('Total travel time: {} (Days HH:MM:SS)'.format(str(datetime.timedelta(seconds= traveltime))))

    # TO DO: display mean travel time
    # Data stored as seconds will be converted to more meaning units #LinkRef 3
    travelmean = int(df['Trip Duration'].mean())
    print('Mean of travel time: {} (HH:MM:SS)'.format(str(datetime.timedelta(seconds= travelmean))))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Attention:
    #some files do not contain any data regarding birth
    #in case of missing data no calculation and display of data
        
    #printing result value_count would be more efficient, but always prints additional type info
    #to look nicer result will be stored in a separate df and printed by looping throw
    #print(df['User Type'].value_counts())


    try:
        # TO DO: Display counts of user types
        print('\nFollowing user types apply:')   
        dfs = df['User Type'].value_counts()
        for key, value in dfs.iteritems():
            print(key, value)        

        
        # TO DO: Display counts of gender
        print('\nUser split into gender as:')   
        dfs = df['Gender'].value_counts()
        for key, value in dfs.iteritems():
            print(key, value)
        
        print("\n")
        
        # TO DO: Display earliest, most recent, and most common year of birth
        dobMin = int(df['Birth Year'].min())
        print("\nThe earliest year of birth (not cleaned): {}".format(dobMin))
        
        
        #Clean up DOB considering entries less than 1916 as mistyping 2016
        dfd = df[df['Birth Year'] > 1916]
        dobMinC = int(dfd['Birth Year'].min())
        print("\nThe earliest year of birth (cleaned): {}".format(dobMinC))
        
        
        dobMax = int(df['Birth Year'].max())
        print("\nThe most recent year of birth: {}".format(dobMax))
        #print(int(df['Birth Year'].max()))
        
        dobMode = int(df['Birth Year'].mode())
        print("\nThe most common year of birth: {}".format(dobMode))
        #print(int(df['Birth Year'].mode()))

        
    except:
        print('Sorry there are no data to be analysed.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):

    """ Display 5 Records as Raw Date """
    print(df.sample(5))


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        #Display sample raw data upon user request, continue until user denies
        input_ok = 0
        input_status = 1
        while not input_ok == 1:
            # Depending on the number of iterations use different wording
            if input_status == 1:
                raw_input = input('\nWould you like to see some raw data? Enter yes or no.\n').lower()
                input_status = 2
            else:   
               raw_input = input('\nWould you like to see further raw data? Enter yes or no.\n').lower() 
               
            if raw_input == 'yes':
                # show raw data
                raw_data(df)
            else:
                input_ok = 1


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print("\nThank you for your interest in bike sharing data.") 
            break
        else:
            #clean sreen for new start
            os.system('clear')

if __name__ == "__main__":
    main()