# Flight Search Service
This project implements three services: `provider-a`, `provider-b`, and `airflow` to search for flights and return search results in a specified currency.

## Provider-a Service
The `provider-a` service implements a single POST endpoint `/search` that returns flight search results from the `response_a.json` file with a 30-second delay.

## Provider-b Service
The `provider-b` service implements a single POST endpoint `/search` that returns flight search results from the `response_b.json` file with a 60-second delay.

## Airflow Service
The `airflow` service implements a POST endpoint `/search` that sends search requests to `provider-a` and `provider-b` services and returns a unique `search_id` for the search.

The `airflow` service also implements a GET endpoint `/results/{search_id}/{currency}` that returns the search results from both `provider-a` and `provider-b` services for the specified `search_id` in the specified `currency`. The search results are accumulated and sorted by price, and the response contains the search status as either `PENDING` or `COMPLETED` depending on the stage of the search.

To convert the search results to a common currency, the `airflow` service downloads the exchange rates at noon each day and also on the first run. The converted search results include a `price` field with the amount in the specified currency and a `pricing` field with the exchange rate used for the conversion.

## Quick start:

Get the code:

    $ git clone https://github.com/Tremos/airflow_search_service.git

Build:

    $ cd airflow_search_service
    $ docker-compose up --build

The application will be launched on `port 9000`. http://127.0.0.1:9000/

`provider-a` and `provider-b` respectively on port `9001`, `9002`

### Provider-a
`POST /search` returns flights' data from response_a.json with 30 seconds delay

### Provider-b
`POST /search` returns flights' data from response_b.json with 60 seconds delay

### Airflow
`POST /search` returns `search_id`

`GET /results/{search_id}/{currency}` returns flights' data along with `search_id` and `status` of search in json

**Parameters:**

`search_id` : unique search id of search

`currency` : representation of currency in 3 letters. Example: `KZT` 