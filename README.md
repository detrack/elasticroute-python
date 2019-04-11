[![Build Status](https://travis-ci.com/detrack/elasticroute-python.svg?branch=master)](https://travis-ci.com/detrack/elasticroute-python)
[![PyPI version](https://badge.fury.io/py/elasticroute.svg)](https://badge.fury.io/py/elasticroute)
[![Python Versions](https://img.shields.io/pypi/pyversions/elasticroute.svg)](https://pypi.org/project/elasticroute/)
[![Coverage Status](https://coveralls.io/repos/github/detrack/elasticroute-python/badge.svg?branch=master)](https://coveralls.io/github/detrack/elasticroute-python?branch=master)

# ElasticRoute for Python

![ElasticRoute Logo](http://elasticroute.staging.wpengine.com/wp-content/uploads/2019/02/Elastic-Route-Logo-Text-on-right-e1551344046806.png)

### API for solving large scale travelling salesman/fleet routing problems

You have a fleet of just 10 vehicles to serve 500 spots in the city. Some vehicles are only available in the day. Some stops can only be served at night. How would you solve this problem?

You don't need to. Just throw us a list of stops, vehicles and depots and we will do the heavy lifting for you. _Routing as a Service!_

**BETA RELASE:**  ElasticRoute is completely free-to-use until 30th April 2020!

## Quick Start Guide

Install with pip:

    pip install elasticroute

In your code, set your default API Key (this can be retrieved from the dashboard of the web application):

```python
import elasticroute as er
er.defaults.API_KEY = "my_super_secret_key"
```

Create a new `Plan` object and givt it a name/id:

```python
plan = er.Plan()
plan.id = "my_first_plan"
```

Give us an array of stops:

```python
plan.stops = [
    {
        "name": "Changi Airport",
        "address": "80 Airport Boulevard (S)819642",
    },
    {
        "name": "Gardens By the Bay",
        "lat": "1.281407",
        "lng": "103.865770",
    },
    # add more stops!
    # both human-readable addresses and machine-friendly coordinates work!
]
```

Give us an array of your available vehicles:

```python
plan.vehicles = [
    {
        "name": "Van 1"
    },
    {
        "name": "Van 2"
    },
]
```

Give us an array of depots (warehouses):

```python
plan.depots = [
    {
        "name": "Main Warehouse",
        "address":  "61 Kaki Bukit Ave 1 #04-34, Shun Li Ind Park Singapore 417943",
    },
]
```

Set your country and timezone (for accurate geocoding):

```python
plan.generalSettings["country"] = "SG"
plan.generalSettings["timezone"] = "Asia/Singapore"
```

Call `solve()` and save the result to a variable:

```python
solution = plan.solve()
```

Inspect the solution!

```python
for stop in solution.stops:
  print("Stop {} will be served by {} at time {}".format(stop["name"], stop["assign_to"], stop["eta"]))
```

Quick notes:

-   The individual stops, vehicles and depots can be passed into the `Plan` as either dictionaries or instances of `elasticroute.Stop`, `elasticroute.Vehicle` and `elasticroute.Depot` respectively. Respective properties are the same as the dictionary keys.
-   Solving a plan returns you an instance of `elasticroute.Solution`, that has mostly the same properties as `elasticroute.Plan` but not the same functions (see advanced usage)
-   Unlike when creating `Plan`'s, `Solution.stops|vehicles|depots` returns you instances of `elasticroute.Stop`, `elasticroute.Vehicle` and `elasticroute.Depot` accordingly instead of dictionaries.

## Advanced Usage

### Setting time constraints

Time constraints for Stops and Vehicles can be set with the `from` and `till` keys of `elasticroute.Stop` and `elasticroute.Vehicle`:

```python
morning_only_stop = er.Stop()
morning_only_stop["name"] = "Morning Delivery 1"
morning_only_stop["from"] = 900
morning_only_stop["till"] = 1200
# add address and add to plan...
morning_shift_van = er.Vehicle()
morning_shift_van["name"] = "Morning Shift 1"
morning_shift_van["from"] = 900
morning_shift_van["till"] - 1200
# add to plan and solve...
```

Not specifying the `from` and `till` keys of either class would result it being defaulted to `avail_from` and `avail_to` keys in the `elasticroute.defaults.generalSettings` dictionary, which in turn defaults to `500` and `1700`.

### Setting home depots

A "home depot" can be set for both Stops and Vehicles. A depot for stops indicate where a vehicle must pick up a stop's goods before arriving, and a depot for vehicles indicate the start and end point of a Vehicle's journey (this implicitly assigns the possible jobs a Vehicle can take).
By default, for every stop and vehicle, if the depot field is not specified we will assume it to be the first depot.

```python
common_stop = er.Stop()
common_stop["name"] = "Normal Delivery 1"
common_stop["depot"] = "Main Warehouse"
# set stop address and add to plan...
rare_stop = er.Stop()
rare_stop["name"] = "Uncommon Delivery 1"
rare_stop["depot"] = "Auxillary Warehouse"
# set stop address and add to plan...
plan.vehicles = [
    {
        "name": "Main Warehouse Van",
        "depot": "Main Warehouse"
    },
    {
        "name": "Auxillary Warehouse Van",
        "depot": "Auxillary Warehouse"
    }
]
plan.depots = [
    {
        "name": "Main Warehouse",
        "address": "Somewhere"
    },
    {
        "name": "Auxillary Warehouse",
        "address": "Somewhere else"
    }
]
# solve and get results...
```

**IMPORTANT:** The value of the `depot` fields MUST correspond to a matching `elasticroute.Depot` in the same plan with the same name!

### Setting load constraints

Each vehicle can be set to have a cumulative maximum weight, volume and (non-cumulative) seating capacity which can be used to determine how many stops it can serve before it has to return to the depot. Conversely, each stop can also be assigned weight, volume and seating loads.
The keys are `weight_load`, `volume_load`, `seating_load` for Stops and `weight_capacity`, `volume_capacity` and `seating_capacity` for Vehicles.

### Alternative connection types (for large datasets)

By default, all requests are made in a _synchronous_ manner. Most small to medium-sized datasets can be solved in less than 10 seconds, but for production uses you probably may one to close the HTTP connection first and poll for updates in the following manner:

```python
import time

plan = er.Plan()
plan.connection_type = "poll";
# do the usual stuff
solution = plan.solve()
while solution.status != "planned":
    solution.refresh()
    time.sleep(2)
    # or do some threading or promise
```

Setting the `connection_type` to `"poll"` will cause the server to return you a response immediately after parsing the request data. You can monitor the status with the `status` and `progress` properties while fetching updates with the `refresh()` method.

In addition, setting the `connectionType` to `"webhook"` will also cause the server to post a copy of the response to your said webhook. The exact location of the webhook can be specified with the `webhook` property of `Plan` objects.
