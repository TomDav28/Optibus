from resources.data_helper import *

if __name__ == '__main__':
    verify_all_trips_arrived_to_all_stops()
    verify_all_trips_arrived_in_the_same_order()
    print_ordered_stops()
    print_max_min_mean_trip_length()
    print_max_min_mean_stop_diff()