[![Build Status](https://travis-ci.com/detrack/elasticroute-python.svg?branch=master)](https://travis-ci.com/detrack/elasticroute-python)
[![PyPI version](https://badge.fury.io/py/elasticroute.svg)](https://badge.fury.io/py/elasticroute)
[![Python Versions](https://img.shields.io/pypi/pyversions/elasticroute.svg)](https://pypi.org/project/elasticroute/)
[![Coverage Status](https://coveralls.io/repos/github/detrack/elasticroute-python/badge.svg?branch=master)](https://coveralls.io/github/detrack/elasticroute-python?branch=master)

# ElasticRoute for Python

![ElasticRoute Logo](http://elasticroute.staging.wpengine.com/wp-content/uploads/2019/02/Elastic-Route-Logo-Text-on-right-e1551344046806.png)

With effect from 02 January 2021, we will deprecate support for this client library and there will be no future updates. If you are currently using the client library, the integrations done based on it should still be able to work. Moving forward, we recommend the use of our API documentation ([Dashboard](https://www.elasticroute.com/dashboard-api-documentation/) and [Routing Engine](https://www.elasticroute.com/routing-engine-api-documentation/)) to build your integration.

### API for solving large scale travelling salesman/fleet routing problems

You have a fleet of just 10 vehicles to serve 500 spots in the city. Some vehicles are only available in the day. Some stops can only be served at night. How would you solve this problem?

You don't need to. Just throw us a list of stops, vehicles and depots and we will do the heavy lifting for you. _Routing as a Service!_

## Preamble

We offer two API's: The Dashboard API, for developers looking to integrate their existing system with our [ElasticRoute Dashboard](https://www.elasticroute.com/); and the Routing Engine API, for developers looking to solve the Vehicle Routing Problem in a headless environment. The Routing Engine API is only available by request, while the Dashboard API is generally available. Read more [here](https://www.elasticroute.com/routing-engine-api-documentation/).

**Backwards-compatibility notice:** Due to significant overhauls in the backend API, major version 2 of this library is _not_ compatible with code written to work with version 1 of this library.

## Quick Start Guide (Dashboard API)

Install with pip:

    pip install elasticroute

Create an instance of `DashboardClient`, passing your API key to the constructor. The API Key can be retrieved from the dashboard of the [web application](https://app.elasticroute.com)).

```python
from elasticroute.clients import DashboardClient

dashboard = DashboardClient("YOUR_API_KEY_HERE")
```

You can then programmatically create stops to appear on your Dashboard:

```python
from elasticroute.dashboard import Stop

stop = Stop()
stop["name"] = "Changi Airport"
stop["address"] = "80 Airport Boulevard (S)819642"

dashboard.stops.create(stop)
```

Data attributes of models in this library are accessed and modified using the index operator `[]`. You can get/set any attributes listed in [this page](https://www.elasticroute.com/dashboard-api-documentation/) (under _Field Headers and Description_) that are not marked as **Result** or **Readonly**. Keys passed to the index operator **must** be strings. Passing non-string keys or attempting to modify readonly attributes will trigger a warning.

By default, this creates a stop on today's date. Change the date by passing the `date` keyword argument:

```python
dashboard.stops.create(stop, date="2019-01-01")
```

Date strings must follow the `YYYY-MM-DD` format.

All CRUD operations are available for stops with the following method signatures:

```python
dashboard.stops.create(stop)
dashboard.stops.retrieve(stop_name)
dashboard.stops.update(stop)
dashboard.stops.delete(stop)
```

All methods accept the `date` keyword argument. The `create` method throws an exception (`elasticroute.errors.repository.ERServiceException`) if a stop with an existing name already exists on the same day, while the `retrieve`, `update` and `delete` methods will throw an exception if a stop with the given name does not exist on that day.

CRUD operations are also available for Vehicles:

```python
from elasticroute.dashboard import Vehicle

vehicle = Vehicle()
vehicle["name"] = "Morning shift driver"
vehicle["avail_from"] = 900
vehicle["avail_to"] = 1200

dashboard.vehicles.create(vehicle)
dashboard.vehicles.retrieve(vehicle_name)
dashboard.vehicles.update(vehicle)
dashboard.vehicles.delete(vehicle)
```

Like for stops, the `create` method throws `elasticroute.errors.repository.ERServiceException` if a vehicle with the same name already exists on the same account, while `retrieve`, `update`, `delete` methods will throw an exception if a vehicle with the given name does not yet exist in the account.

Unlike stops, vehicles are not bound by date, and are present across all dates.

Both stops and vehicles accept a dictionary in their constructor that automatically sets their corresponding data attributes.

The library helps you check for invalid values before requests are sent to the server. For instance, setting a vehicle's `avail_to` data attribute to `2500` will trigger a `elasticroute.errors.validator.BadFieldError` when performing any CRUD operations.

Currently, the Dashboard API is unable to perform CRUD operations on depots. Since the details of depots are likely not going to be changed frequently, please configure (using the web application) all the depots that your team has before using this library to perform plans.

### Programmatically starting the planning process

Once you have created more than one stop for the day (and created a starting depot via the web application), you can remotely start and stop the planning process:
```python
    # where dashboard is an instance of elasticroute.clients.DashboardClient and date is a string in YYYY-MM-DD format
    dashboard.stops.start_planning(date)
    dashboard.stops.stop_planning(date)
```
## Quick Start Guide (Routing Engine API)

The Routing Engine API is only available by request; please get in touch with us if you require our headless routing capabilities. Attempting to use the Routing Engine API with an unauthorized API Key will result in your requests being rejected.

If you haven't already, install this library:

    pip install elasticroute>=2.0.0

Create an instance of `RoutingClient`, passing your API key in the constructor:

```python
from elasticroute.clients import RoutingClient

router = RoutingClient("YOUR_API_KEY_HERE")
```

Create a new `Plan` object:

```python
from elasticroute.routing import Plan

plan = Plan("some-unique-id")
```

Give us a list of stops:

```python
from elasticroute.routing import Stop
plan.stops = [
    Stop({
        "name": "Changi Airport",
        "address": "80 Airport Boulevard (S)819642",
    }),
    Stop({
        "name": "Gardens By the Bay",
        "lat": "1.281407",
        "lng": "103.865770",
    }),
    # add more stops!
    # both human-readable addresses and machine-friendly coordinates work!
]
```

Give us a list of your available vehicles:

```python
from elasticroute.routing import Vehicle
plan.vehicles = [
    Vehicle({
        "name": "Van 1"
    }),
    Vehicle({
        "name": "Van 2"
    }),
]
```

Give us a list of depots (warehouses):

```python
from elasticroute.routing import Depot
plan.depots = [
    Depot({
        "name": "Main Warehouse",
        "address":  "61 Kaki Bukit Ave 1 #04-34, Shun Li Ind Park Singapore 417943",
    }),
]
```

Set your country and timezone:

```python
plan.generalSettings["country"] = "SG"
plan.generalSettings["timezone"] = "Asia/Singapore"
```

Use the client to submit the plan:

```python
plan = router.plans.create(plan)
```

The planning process is asynchronous as it takes some time to complete. Persist the value of the plan id you used earlier, and retrieve it in a separate process at a later time:

```python
plan = router.plans.retrieve(plan_id)
```

`plan.status` should give you `"planned"` when the process is complete. Inspect the solution:

```python
for stop in plan.stops:
  print("Stop {} will be served by {} at time {}".format(stop["name"], stop["assign_to"], stop["eta"]))
```

## Advanced Usage

### Setting time constraints

Time constraints for Stops and Vehicles can be set with the `from` and `till` keys of `elasticroute.common.Stop`, and the `avail_from` and `avail_to` keys of `elasticroute.common.Vehicle`:

```python
morning_only_stop = Stop()
morning_only_stop["name"] = "Morning Delivery 1"
morning_only_stop["from"] = 900
morning_only_stop["till"] = 1200
# add address and add to plan...
morning_shift_van = Vehicle()
morning_shift_van["name"] = "Morning Shift 1"
morning_shift_van["avail_from"] = 900
morning_shift_van["avail_till"] - 1200
# add to plan and solve, or upload to dashboard using DashboardClient
```

`elasticroute.common.Stop` is the parent class of `elasticroute.routing.Stop` and `elasticroute.dashboard.Stop`; Vehicles work in a similar manner

### Setting home depots

A "home depot" can be set for both Stops and Vehicles. A depot for stops indicate where a vehicle must pick up a stop's goods before arriving, and a depot for vehicles indicate the start and end point of a Vehicle's journey (this implicitly assigns the possible jobs a Vehicle can take).
By default, for every stop and vehicle, if the depot field is not specified we will assume it to be the first depot.

```python
common_stop = Stop()
common_stop["name"] = "Normal Delivery 1"
common_stop["depot"] = "Main Warehouse"
# set stop address
rare_stop = Stop()
rare_stop["name"] = "Uncommon Delivery 1"
rare_stop["depot"] = "Auxillary Warehouse"
# set stop address
main_warehouse_van = Vehicle({
    "name": "Main Warehouse Van",
    "depot": "Main Warehouse"
})
aux_warehouse_van = Vehicle({
    "name": "Auxillary Warehouse Van",
    "depot": "Auxillary Warehouse"
})

# if using DashboardClient:
dashboard.stops.create(common_stop)
dashboard.stops.create(rare_stop)
dashboard.vehicles.create(main_warehouse_van)
dashboard.vehicles.create(aux_warehouse_van)

# if using RoutingClient:
plan = Plan("my_plan")
plan.stops = [common_stop, rare_stop]
plan.vehicles = [main_warehouse_van, aux_warehouse_van]
plan.depots = [
    Depot({
        "name": "Main Warehouse",
        "address": "Somewhere"
    }),
    Depot({
        "name": "Auxillary Warehouse",
        "address": "Somewhere else"
    })
]
router.plans.create(plan)
```

For this to work, there must be a corresponding depot with the same name in the dashboard (if using `DashboardClient`) or in the same plan (if using `RoutingClient`)

### Setting load constraints

Each vehicle can be set to have a cumulative maximum weight, volume and (non-cumulative) seating capacity which can be used to determine how many stops it can serve before it has to return to the depot. Conversely, each stop can also be assigned weight, volume and seating loads.
The keys are `weight_load`, `volume_load`, `seating_load` for Stops and `weight_capacity`, `volume_capacity` and `seating_capacity` for Vehicles.
