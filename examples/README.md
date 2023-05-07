## Parking garages

With this you can read the occupancy of the parking garages in Ghent.

Parameters:

- **limit** (default: 10) - How many results you want to retrieve.

| Variable | Type | Description |
| :------- | :--- | :---------- |
| `garage_id` | string | The id of the garage |
| `name` | string | The name of the garage |
| `parking_type` | string | The type of parking |
| `url` | string | The url with more information about the garage |
| `is_open` | boolean | Whether the garage is open or not |
| `free_parking` | boolean | Whether there is free parking or not |
| `temporary_closed` | boolean | Whether the garage is temporarily closed or not |
| `free_space` | integer | The amount of free parking spaces |
| `total_capacity` | integer | The total capacity of the garage |
| `availability_pct` | float | The percentage of free parking spaces |
| `occupancy_pct` | integer | The percentage of occupied parking spaces |
| `longitude` | float | The longitude of the garage |
| `latitude` | float | The latitude of the garage |
| `updated_at` | datetime | The last time the data was updated |

## Park and Ride

With this you can read the occupancy of the park and rides in Ghent.

Parameters:

- **limit** (default: 10) - How many results you want to retrieve.
- **gentse_feesten** - Whether a park and ride location is used for the [Gentse Feesten](https://gentsefeesten.stad.gent).

| Variable | Type | Description |
| :------- | :--- | :---------- |
| `spot_id` | string | The id of the park and ride |
| `name` | string | The name of the park and ride |
| `parking_type` | string | The type of parking |
| `url` | string | The url with more information about the park and ride |
| `is_open` | boolean | Whether the park and ride is open or not |
| `free_parking` | boolean | Whether there is free parking or not |
| `temporary_closed` | boolean | Whether the park and ride is temporarily closed or not |
| `gentse_feesten` | boolean | Whether the park and ride is used for the [Gentse Feesten](https://gentsefeesten.stad.gent) |
| `free_space` | integer | The amount of free parking spaces |
| `total_capacity` | integer | The total capacity of the park and ride |
| `availability_pct` | float | The percentage of free parking spaces |
| `occupancy_pct` | integer | The percentage of occupied parking spaces |
| `longitude` | float | The longitude of the park and ride |
| `latitude` | float | The latitude of the park and ride |
| `updated_at` | datetime | The last time the data was updated |

## BlueBikes

This dataset consists of information about the rental locations of the bluebikes

| Variable | Type | Description |
| :------- | :--- | :---------- |
| `spot_id` | string | The id of the bluebike location |
| `name` | string | Name of the bluebike location |
| `spot_type` | integer | The type of the bluebike location |
| `bikes_in_use` | integer | The amount of bikes in use |
| `bikes_available` | integer | The amount of bikes available |
| `last_update` | datetime | The last time the data was updated |
| `longitude` | float | The longitude of the bluebike location |
| `latitude` | float | The latitude of the bluebike location |

## Partago

This dataset consists of information about the Partago vehicles and where they are located.

Parameters:

- **limit** (default: 10) - How many results you want to retrieve.

| Variable | Type | Description |
| :------- | :--- | :---------- |
| `name` | string | Name of the Partago vehicle |
| `vehicle_type` | Vehicle (dict) | The vehicle information (brand, mode, fuel etc.) |
| `picture_url` | string | The url of a picture of the vehicle |
| `station_type` | string | The type of station (free floating or fixed) |
| `last_update` | datetime | The last time the data was updated |
| `longitude` | float | The longitude of the vehicle |
| `latitude` | float | The latitude of the vehicle |
