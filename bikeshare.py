import time
import pandas as pd
import numpy as np

# Here we just leave some options for the user to set clear statistic about his choice
# using dictionary & lists & show these lists to the user & then return the value of each choice
# & to avoid invalid input we used while loop

survey_data = {'chicago': 'chicago.csv', 'new york': 'new_york_city.csv', 'washington': 'washington.csv'}
months = ["january", "february", "march", "april", "may", "june", "all"]
days = ["saturday", "sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "all"]

def get_filters():
    print('Hello! Let\'s explore some insightful US bike share data!')
    city = input("Kindly select a city to run its data:\n Chicago\n or New York\n or Washington\n").lower()
    while city.lower() not in survey_data.keys():
        print("Invalid Input")
        city = input("Kindly select a city to run its data:\n Chicago\n or New York\n or Washington\n").lower()

    month = input("wanna filter {}\'s data by month? Select the month or All for no filter:"
                  "\n- January\n- February\n- March\n- April\n- May\n- June\n- All\n".format(city)).lower()
    while month.lower() not in months:
        print(" Something went wrong, choose for the list")
        month = input("wanna filter {}\'s data by month? Select the month or All for no filter:"
                   "\n- January\n- February\n- March\n- April\n- May\n- June\n- All\n".format(city)).lower()

    day = input("to filter {} & {}\'s data by date, just choose from the following list:"
                "\n - Saturday\n - Sunday\n - Monday\n - Tuesday\n - Wednesday\n - Thursday\n - Friday\n - All\n".format(city, month)).lower()
    while day.lower() not in days:
        print("OOPS! Wrong choice")
        day = input("to filter {} & {}\'s data by date, just choose from the following list:"
                 "\n - Saturday\n - Sunday\n - Monday\n - Tuesday\n - Wednesday\n - Thursday\n - Friday\n - All\n".format(city, month)).lower()
    print("-" * 40)
    return city, month, day

def load_data(city, month, day):
    # this step is bout loading the data of the city, month & day converting the data to datetime

    df = pd.read_csv(survey_data[city])
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df['month'] = df["Start Time"].dt.month
    df['days'] = df["Start Time"].dt.day_name()
    df["start hour"] = df["Start Time"].dt.hour

    if month != 'all':
        months_list = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months_list.index(month)+1
        df = df[df['month'] == month]
    if day != 'all':
        days_list = ['saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday']
        df = df[df['days'] == day.title()]
    return df


def time_stats(df):
    # extracting some info about the most common month & day using .mode (),
    # but it does not work good with me in common_month,
    # so a friend advised me to use .value_counts().idxmax() instead & it works good

    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # display the most common month
    common_month = df['month'].value_counts().idxmax()
    print("The most common month is : {}".format(common_month))

    # display the most common day of week
    common_day = df['days'].mode()[0]
    print("The most common day is : {}".format(common_day))

    # display the most common start hour
    common_hour = df['start hour'].mode()[0]
    print("The most common hour: {}".format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    # still using .mode(), but with diff inputs & extract the most frequent & used station as start & end station

    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start = df["Start Station"].mode()[0]
    print("The most common start station is : ", common_start)

    # display most commonly used end station
    common_end = df["End Station"].mode()[0]
    print("The most common end station is : ", common_end)

    # display most frequent combination of start station and end station trip
    df["line"] = df["Start Station"]+","+df["End Station"]
    freq_station = df["line"].mode()[0]
    print("The most frequent station is :", freq_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    # start using aggregation & round the result to have more valid statistics

    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_duration = df["Trip Duration"].sum().round()
    print(" The total travel time is :", total_travel_duration)

    # display mean travel time
    mean_time = df["Trip Duration"].mean().round()
    print("The average travel time is :", mean_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    # still using aggregation, but adding if function to handle the 2 missing columns in washington sheet

    """Displays statistics on bikes hare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    users_count = df["User Type"].value_counts().to_frame()
    print("The count of users is :", users_count)

    # Display counts of gender
    if city.lower() != "washington":
        gender_count = df["Gender"].value_counts().to_frame()
        print("The count of gender is :", gender_count)
    else:
        print("There is no data for this city")


    # Display earliest, most recent, and most common year of birth
    if city.lower() != 'washington':
        recent_year = int(df["Birth Year"].max())
        print(" The most recent year is :", recent_year)
    else:
        print("There is no data for this city")

    if city.lower() != 'washington':
        early_year = int(df["Birth Year"].min())
        print(" The earliest year is :", early_year)
    else:
        print("There is no data for this city")

    if city.lower() != 'washington':
        common_year = int(df["Birth Year"].mode()[0])
        print("The most common year is :", common_year)
    else:
        print("There is no data for this city")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_rows(df):
    # asking the user if he wanna see 5 rows using elif & while loops & if he answered no,it will be the end

    print("\n Raw data is available to check...\n")
    pd.set_option('display.max_columns', 200)
    index = 0
    user_input = input("Wanna display 5 rows of data? yes or no\n").lower()
    if user_input not in ['yes', 'no']:
        print("Plz enter yes or no")
    elif user_input != 'yes':
        print("Thanks for your time")
    else:
        while index+5 < df.shape[0]:
            print(df.iloc[index:index+5])
            index += 5
            user_input = input("Wanna display more 5 rows?\n").lower()
            if user_input != 'yes':
                print("Thanks for your time")
                break


def main():
    while True:
        city, month, day = get_filters()
        print(city, month, day)
        df = load_data(city, month, day)
        print(df.head())
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_rows(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print("Thanks for your time")
            break


if __name__ == "__main__":
    main()