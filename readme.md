# MyTradeApi - Trade Details API
This API is used to get the trade details on our platform, with lots of search/filter/sort options.

## Built with
- [Python](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://uvicorn.org/)

## Requirements
- Python 3.9.1
- FastApi 0.78.0
- Uvicorn 0.18.2 with CPython 3.9.1

## EndPoints:
### GET ```\trades```
List all trades

#### Query Parameters:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| ```page``` | Integer | (Mandatory) Page number |
| ```per_page``` | Integer | (Optional) Number of items per page (default 10)|
| ```sort``` | String | (Optional) Sort order |
| ```isdesc``` | Boolean | (Optional) Sort order (default false) |

#### Response:

| Field | Type | Description |
| --------- | ---- | ----------- |
| ```status``` | String | (Mandatory) Status of the request (```success``` or ```failure```) |
| ```page``` | Integer | (OnSuccess - String) Page number out of the total pages separated by ```/``` |
| ```page_rate``` | Integer | (OnSuccess) Items per page |
| ```total_trades``` | Integer | (OnSuccess) Total number of trades |
| ```trades``` | Array | (OnSuccess) List of trades (Refer [```Trade Object Details```](#trade-object-details) for more details) |
| ```message``` | String | (OnFailure - String) Error message |
| ```sortbyReceived``` | String | (OnFailure - String) If wrong sortby parameter is passed, this will be the sortby parameter received |
| ```sortbyList``` | Array | (OnFailure - Array) List of sortby parameters accepted


### Demo Request:
```dotnetcli
curl -X 'GET' \
  'http://127.0.0.1:8000/trades?page=1&page_rate=10&sort_by=trader&isdesc=false' \
  -H 'accept: application/json'
```

### Demo Response:
```json
{
  "status": "success",
  "page": "1/100",
  "page_rate": 10,
  "total_trades": 1000,
  "trades": [
    {
      "assetClass": null,
      "counterparty": null,
      "instrumentId": "MSFT",
      "instrumentName": "Microsoft",
      "tradeDateTime": "2022-05-12T22:09:16.456336",
      "tradeDetails": {
        "buySellIndicator": "BUY",
        "price": 7382.530071657349,
        "quantity": 13
      },
      "tradeId": "1a29538a-49fe-4dca-9c87-3f5395171452",
      "trader": "Kevin Williams"
    },
    {
      "assetClass": null,
      "counterparty": "Jill Lopez",
      "instrumentId": "NFLX",
      "instrumentName": "Netflix",
      "tradeDateTime": "2022-03-26T22:09:16.456336",
      "tradeDetails": {
        "buySellIndicator": "SELL",
        "price": 1394.2438962342758,
        "quantity": 9
      },
      "tradeId": "435434d8-dee1-4962-863d-8aa673f45a71",
      "trader": "Ross Taylor"
    },
    ...
  ]
}
```
  
### Get ```\trades\{trade_id}``` 
Get a single trade by tradeId

#### Url Parameters:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| ```trade_id``` | String | (Mandatory) TradeId of the trade |

#### Response:

| Field | Type | Description |
| --------- | ---- | ----------- |
| ```status``` | String | (Mandatory) Status of the request (```success``` or ```failure```) |
| ```trade``` | TradeDetails | (OnSuccess) Result trade (Refer [```Trade Object Details```](#trade-object-details) for more details) |
| ```message``` | String | (OnFailure - String) Error message |

#### Demo Request:
```dotnetcli
curl -X 'GET' \
  'http://127.0.0.1:8000/trade/f3fe036a-1104-4190-a6b6-64df41ebf4cb' \
  -H 'accept: application/json'
```

#### Demo Response:
```json
{
  "status": "success",
  "trade": {
    "assetClass": "Equity",
    "counterparty": "Kevin Lewis",
    "instrumentId": "GOOG",
    "instrumentName": "Google",
    "tradeDateTime": "2022-04-03T22:09:16.456336",
    "tradeDetails": {
      "buySellIndicator": "SELL",
      "price": 2450.6348023787905,
      "quantity": 73
    },
    "tradeId": "f3fe036a-1104-4190-a6b6-64df41ebf4cb",
    "trader": "Jeff Smith"
  }
}
```

### Get ```\search``` 
Search for trades with given values

Query will be applied for followig fields:
* ```counterparty``` (If available)
* ```instrumentId```
* ```instrumentName```
* ```trader```

#### Query Parameters:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| ```search``` | String | (Mandatory) Keyword to be searched |
| ```case_sensitive``` | Boolean | (Optional) If passed ```true```, search will be case sensitive (default: ```false```)
| ```page``` | Integer | (Mandatory) Page number |
| ```page_rate``` | Integer | (Optional) Items per page (default: 10) |
| ```sort_by``` | String | (Optional) Sort data by (Accepted values: ```["price", "quantity", "date", "trader"]```) |
| ```isdesc``` | Boolean | (Optional) If passed ```true```, sort data in descending order (default: ```false```) |

#### Response:

| Field | Type | Description |
| --- | --- | --- |
| ```status``` | String | (Mandatory) Status of the request (```success``` or ```failure```) |
| ```page``` | String | (OnSuccess) Page number out of the total pages separated by ```/``` |
| ```page_rate``` | Integer | (OnSuccess) Items per page |
| ```total_trades``` | Integer | (OnSuccess) Total number of trades |
| ```trades``` | Array | (OnSuccess) List of trades (Refer [```Trade Object Details```](#trade-object-details) for more details) |
| ```message``` | String | (OnFailure) Error message |
| ```sortbyReceived``` | String | (OnFailure) If wrong sortby parameter is passed, this will be the sortby parameter received |
| ```sortbyList``` | Array | (OnFailure) List of sortby parameters accepted  |
  
#### Demo Request:
```dotnetcli
curl -X 'GET' \
  'http://127.0.0.1:8000/search?page=1&search=John%20Jackson&page_rate=10&case_sensitive=true&sort_by=price&isdesc=true' \
  -H 'accept: application/json'
```

#### Demo Response:
```json
{
  "status": "success",
  "page": "1/1",
  "page_rate": 10,
  "total_trades": 1,
  "trades": [
    {
      "assetClass": "FX",
      "counterparty": "John Jackson",
      "instrumentId": "GOOG",
      "instrumentName": "Google",
      "tradeDateTime": "2022-05-11T22:48:37.305865",
      "tradeDetails": {
        "buySellIndicator": "BUY",
        "price": 8133.685963802577,
        "quantity": 50
      },
      "tradeId": "43b84119-effc-42d2-9ca8-4ab38573ac21",
      "trader": "Robert Williams"
    },
    ...
  ]
}
```

### Get ```\filter``` 
Filter trades with given values

Query will be applied for following fields
* ```asset_class``` (If available)
* ```trade_date_time```
* ```price```
* ```buy_sell_indicator```

#### Query Parameters:

| Parameter | Type | Description |
| --------- | ----------- | ------------ |
| ```asset_class``` | String | (Optional) ```asset_class``` of trade |
| ```start``` | datetime | (Optional) The minimum date for the tradeDateTime field. |
| ```end``` | datetime | (Optional) The maximum date for the tradeDateTime field. |
| ```min_price``` | INT | (Optional) The minimum price for the price field. |
| ```max_price``` | INT | (Optional) The maximum price for the price field. |
| ```trade_type``` | String | (Optional) ```buy_sell_indicator``` of trade |
| ```page``` | INT | (Optional) Page number |
| ```page_rate``` | INT | (Optional) Items per page |
| ```sort_by``` | String | (Optional) Sort data by (Accepted values: ```["price", "quantity", "date", "trader"]```) |
| ```isdesc``` | Boolean | (Optional) If passed ```true```, sort data in descending order (default: ```false```) |


#### Response:

| Field | Type | Description |
| --- | --- | --- |
| ```status``` | String | (Mandatory) Status of the request (```success``` or ```failure```) |
| ```page``` | String | (OnSuccess) Page number out of the total pages separated by ```/``` |
| ```page_rate``` | Integer | (OnSuccess) Items per page |
| ```total_trades``` | Integer | (OnSuccess) Total number of trades |
| ```trades``` | Array | (OnSuccess) List of filtered trades (Refer [```Trade Object Details```](#trade-object-details) for more details) |
| ```message``` | String | (OnFailure) Error message |
| ```sortbyReceived``` | String | (OnFailure) If wrong sortby parameter is passed, this will be the sortby parameter received |
| ```sortbyList``` | Array | (OnFailure) List of sortby parameters accepted  |

#### Demo Request:
```dotnetcli
curl -X 'GET' \
  'http://127.0.0.1:8000/filter?page=1&page_rate=10&asset_class=Equity&start=2022-04-03T22%3A09%3A16.456336&min_price=1000' \
  -H 'accept: application/json'
```

#### Demo Response:
```json
{
  "status": "success",
  "page": "1/16",
  "page_rate": 10,
  "total_trades": 153,
  "trades": [
    {
      "assetClass": "Equity",
      "counterparty": null,
      "instrumentId": "MSFT",
      "instrumentName": "Microsoft",
      "tradeDateTime": "2022-06-08T22:48:37.305865",
      "tradeDetails": {
        "buySellIndicator": "SELL",
        "price": 5706.071302522822,
        "quantity": 11
      },
      "tradeId": "abf45a43-2195-48b6-9bf9-d5370aba9b5a",
      "trader": "Jack Brown"
    },
    {
      "assetClass": "Equity",
      "counterparty": "Ravi Miller",
      "instrumentId": "BABA",
      "instrumentName": "Baidu",
      "tradeDateTime": "2022-06-16T22:48:37.305865",
      "tradeDetails": {
        "buySellIndicator": "SELL",
        "price": 3011.4906799033542,
        "quantity": 35
      },
      "tradeId": "fa1b6d16-e8ed-465b-9340-5ccc4cc856f1",
      "trader": "Rob Lewis"
    },
    ...
  ]
}
```

## ```Trade``` Object Details
Trade Object has following fields:
| Field | Type | Description |
| --- | --- | --- |
| ```assetClass``` | String | (Optional) Asset class of the trade |
| ```counterparty``` | String | (Optional) Counterparty of the trade |
| ```instrumentId``` | String | (Mandatory) Instrument ID of the trade |
| ```instrumentName``` | String | (Mandatory) Instrument name of the trade |
| ```tradeDateTime``` | String | (Mandatory) Date and time of the trade |
| ```tradeDetails``` | TradeDetailsObject | (Mandatory) Trade details of the trade |
| ```tradeId``` | String | (Mandatory) Trade ID of the trade |
| ```trader``` | String | (Mandatory) Trader of the trade |

## ```TradeDetails``` Object Details
TradeDetails Object has following fields:
| Field | Type | Description |
| --- | --- | --- |
| ```buySellIndicator``` | String | (Mandatory) Buy/Sell indicator of the trade |
| ```price``` | Integer | (Mandatory) Price of the trade |
| ```quantity``` | Integer | (Mandatory) Quantity of the trade |
