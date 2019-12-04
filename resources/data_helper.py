import pandas as pd
import numpy as np

from resources.base_settings import DATA_CSV_PATH

'''
returns unique trip IDs and stop IDs
'''


def get_unique_values():
    stop_set = set(drivers_data["stop_id"])
    trip_list = list(set(drivers_data["trip_id"]))
    return {
        "stop_set": stop_set,
        "trip_list": trip_list
    }


'''
load the data and sort it first by trip and then by time
'''
drivers_data = pd.read_csv(DATA_CSV_PATH)
drivers_data["time"] = pd.to_datetime(drivers_data["time"])
drivers_data.sort_values(by=["trip_id", "time"], inplace=True)
'''
Unique values that make iterations simpler
'''
unique_values = get_unique_values()

'''
Compares the given set of stops to the set of all stops - called by groupby
'''


def all_stop_ids_present(series):
    return set(series) == unique_values["stop_set"]


'''
Grouping by trip and aggregating with all_stop_ids_present
If there are unfulfilled trips, print their codes
'''


def verify_all_trips_arrived_to_all_stops():
    grouped_result = drivers_data.groupby("trip_id").agg({'stop_id': all_stop_ids_present})
    trips_not_arrived = grouped_result.index[grouped_result['stop_id'] == False].tolist()
    if len(trips_not_arrived) > 0:
        print("\nTrips that didn't arrive to all stops:\n" + str(trips_not_arrived))
    else:
        print("\nAll trips arrived to all stops!\n")


'''
Compares stop_id lists between subsequent pairs of trips, One inequality is enough to fail. 
Prints out the trip codes that were found different
'''


def verify_all_trips_arrived_in_the_same_order():
    flag = True
    trip_count = len(unique_values["trip_list"])
    for i in range(trip_count - 1):

        current_trip = unique_values["trip_list"][i]
        next_trip = unique_values["trip_list"][i + 1]
        current_subset = drivers_data.loc[drivers_data.trip_id == current_trip, "stop_id"]
        next_subset = drivers_data.loc[drivers_data.trip_id == next_trip, "stop_id"]
        is_identical = current_subset.tolist() == next_subset.tolist()

        flag = flag and is_identical

        if not is_identical:
            print("trips {current} and {next} are not identical \n".format(
                current=current_trip,
                next=next_trip
            ))

    if flag:
        print("\nAll trips are identical \n")


'''
Takes the stops of the last trip and prints them
'''


def print_ordered_stops():
    ordered_stops = drivers_data.loc[drivers_data.trip_id == unique_values["trip_list"][0], "stop_name"].tolist()
    print("Stop order: \n" + "\n".join(ordered_stops))


'''
Next 4 functions are group_by aggregate functions:
min datetime difference
max datetime difference
mean datetime difference
total trip length
'''


def min_diff(series):
    diff_list = [diff.total_seconds() / 60.0
                 for diff in np.diff(series.tolist())]
    return min(diff_list)


def max_diff(series):
    diff_list = [diff.total_seconds() / 60.0
                 for diff in np.diff(series.tolist())]
    return max(diff_list)


def mean_diff(series):
    diff_list = [diff.total_seconds() / 60.0
                 for diff in np.diff(series.tolist())]
    return np.mean(diff_list)


def trip_length(series):
    return (max(series) - min(series)).total_seconds() / 60.0


'''
Next 2 functions groups by trip, aggregates with the relevant function/s above
prints max, min, and min values
'''


def print_max_min_mean_trip_length():
    grouped_result = drivers_data.loc[:, ["trip_id", "time"]] \
        .groupby("trip_id") \
        .agg({
        'time': trip_length
    })
    print("\nMax length: {max} minutes \nMin length: {min} minutes \nMean length: {mean} minutes".format(
        max=max(grouped_result.time),
        min=min(grouped_result.time),
        mean=np.mean(grouped_result.time).round(2)
    ))


def print_max_min_mean_stop_diff():
    grouped_result = drivers_data.loc[:, ["trip_id", "time"]] \
        .groupby("trip_id") \
        .agg({
        'time': [min_diff, max_diff, mean_diff]
    })
    print("\nMax interval: {max} minutes \nMin interval: {min} minutes \nMean interval: {mean} minutes".format(
        max=max(grouped_result.time.max_diff),
        min=min(grouped_result.time.min_diff),
        mean=np.mean(grouped_result.time.mean_diff).round(2)
    ))
