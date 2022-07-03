from math import ceil
import uvicorn
from fastapi import FastAPI
import datetime as dt
from typing import Optional
from pydantic import BaseModel, Field
import random
import uuid

# initializing app
app = FastAPI()

# initializing model classes
class TradeDetails(BaseModel):
    buySellIndicator: str = Field(description="A value of BUY for buys, SELL for sells.")
    price: float = Field(description="The price of the Trade.")
    quantity: int = Field(description="The amount of units traded.")

class Trade(BaseModel):
    asset_class: Optional[str] = Field(alias="assetClass", default=None, description="The asset class of the instrument traded. E.g. Bond, Equity, FX...etc")
    counterparty: Optional[str] = Field(default=None, description="The counterparty the trade was executed with. May not always be available")
    instrument_id: str = Field(alias="instrumentId", description="The ISIN/ID of the instrument traded. E.g. TSLA, AAPL, AMZN...etc")
    instrument_name: str = Field(alias="instrumentName", description="The name of the instrument traded.")
    trade_date_time: dt.datetime = Field(alias="tradeDateTime", description="The date-time the Trade was executed")
    trade_details: TradeDetails = Field(alias="tradeDetails", description="The details of the trade, i.e. price, quantity")
    trade_id: str = Field(alias="tradeId", default=None, description="The unique ID of the trade")
    trader: str = Field(description="The name of the Trader")

# constants
asset_classes = ["Bond", "Equity", "FX"]
first_names = ["John", "Jane", "Joe", "Jack", "Jill", "Rose", "Dipesh", "Sachin", "Raj", "Raju", "Ravi", "Ramesh", "Rob", "Robert", "Kevin", "Justin", "Mark", "Matt", "Andrew", "Ross", "Mike", "Mathew", "Angelina", "Priya", "Sufi", "Shreya", "Sneha", "Kiara", "Ritika", "Shivani", "Sushmita", "Patrick", "Andrena", "Abraham", "Aakash"]
last_names = ["Doe", "Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Wilson", "Moore", "Taylor", "Anderson", "Thomas", "Roberts", "Khan", "Lopez", "Lewis", "Jackson", "Sharma", "Rongara", "Rajput", "Saifi", "Sibli", "Toppo", "Shah", "Rao", "Patil", "Pichai", "Musk"]
instrument_ids = ["TSLA", "AAPL", "AMZN", "GOOG", "MSFT", "FB", "NFLX", "BABA", "NVDA"]
instrument_names = {"TSLA": "Tesla", "AAPL": "Apple", "AMZN": "Amazon", "GOOG": "Google", "MSFT": "Microsoft", "FB": "Facebook", "NFLX": "Netflix", "BABA": "Baidu", "NVDA": "Nvidia"}
buysell_indicators = ["BUY", "SELL"]
trade_date_times = [dt.datetime.now() - dt.timedelta(days=i) for i in range(1, 100)]
sortbyList = ["price", "quantity", "date", "trader"]

# building dataset
trades = []
for i in range(1000):
    instrument_id = random.choice(instrument_ids)
    should_add_assetclass = random.random() < 0.5
    should_add_counterparty = random.random() < 0.5
    asset_class = random.choice(asset_classes) if should_add_assetclass else None
    counterparty = random.choice(first_names) + " " + random.choice(last_names) if should_add_counterparty else None
    trades.append(Trade(
        assetClass=asset_class,
        counterparty=counterparty,
        instrumentId=instrument_id,
        instrumentName=instrument_names[instrument_id],
        tradeDateTime=random.choice(trade_date_times),
        tradeDetails=TradeDetails(
            buySellIndicator=random.choice(buysell_indicators),
            price=random.uniform(1.0, 9000.0),
            quantity=random.randint(1, 100)
        ),
        tradeId=str(uuid.uuid4()),
        trader=random.choice(first_names) + " " + random.choice(last_names)
    ))

# sorting method
def sort_trade_by_price(trade, desc):
    sort_by_price = lambda x: x.trade_details.price
    return sorted(trade, key=sort_by_price, reverse=desc)

def sort_trade_by_quantity(trade, desc):
    sort_by_quantity = lambda x: x.trade_details.quantity
    return sorted(trade, key=sort_by_quantity, reverse=desc)

def sort_trade_by_date(trade, desc):
    sort_by_date = lambda x: x.trade_date_time
    return sorted(trade, key=sort_by_date, reverse=desc)

def sort_trade_by_trader_name(trade, desc):
    sort_by_trader_name = lambda x: x.trader
    return sorted(trade, key=sort_by_trader_name, reverse=desc)

# sorting redirect mehod
def sortTrades(trade, sortby, desc):
    if sortby == "price":
        return sort_trade_by_price(trade, desc)
    elif sortby == "quantity":
        return sort_trade_by_quantity(trade, desc)
    elif sortby == "date":
        return sort_trade_by_date(trade, desc)
    elif sortby == "trader":
        return sort_trade_by_trader_name(trade, desc)
    else:
        return "inavlid sortby"

# routes
# for getting all trades
@app.get("/trades")
def read_trades(page: int, page_rate: Optional[int] = 10, sort_by: Optional[str] = None, isdesc: Optional[bool] = False):
    page = page - 1
    resultTrades = trades
    number_of_trades = len(resultTrades)
    if number_of_trades == 0:
        return {"status": "failure","message": "Oops! No trades found"}, 404
    if page_rate <= 0:
        return {"status": "failure","message": "Oops! Invalid page rate"}, 400
    number_of_pages = ceil(number_of_trades / page_rate)
    if page >= number_of_pages or page < 0:
        return {"status": "failure","message": "Oops! Page not found"}, 404
    if sort_by:
        resultTrades = sortTrades(resultTrades, sort_by, isdesc)
        if isinstance(resultTrades, str):
            return {"status": "failure","message": "Oops! Invalid sortby property name", "sortbyReceived": sort_by, "sortbyList": sortbyList}, 400
    result = {
        "status": "success",
        "page": str(page+1)+"/"+str(number_of_pages),
        "page_rate": page_rate,
        "total_trades": number_of_trades,
        "trades": resultTrades[page * page_rate: (page + 1) * page_rate]
    }
    return result

# for getting a trade by id
@app.get("/trade/{trade_id}")
def read_trade(trade_id: str):
    result = []
    for trade in trades:
        if trade.trade_id == trade_id:
            result = {"status": "success", "trade": trade}
            break
    else:
        return {"status": "failure","message": "Trade not found"}, 404
    return result

# for getting trades by searching a keyword
@app.get("/search")
def search_trades(page:int, search: str, page_rate: Optional[int]=10, case_sensitive: Optional[bool] = False, sort_by: Optional[str] = None, isdesc: Optional[bool] = False):
    page = page - 1
    if page_rate <= 0:
        return {"status": "failure","message": "Oops! Invalid page rate"}, 400
    search = search if case_sensitive else search.lower()
    searchResults = []
    for trade in trades:
        instrument_id = trade.instrument_id.lower() if not case_sensitive else trade.instrument_id
        instrument_name = trade.instrument_name.lower() if not case_sensitive else trade.instrument_name
        trader = trade.trader.lower() if not case_sensitive else trade.trader
        counterparty = trade.counterparty
        if trade.counterparty and not case_sensitive:
            counterparty = trade.counterparty.lower()
        if search in instrument_id or search in instrument_name or search in trader or (counterparty and search in counterparty):
            searchResults.append(trade)

    number_of_trades = len(searchResults)
    if number_of_trades == 0:
        return {"status": "failure","message": "No trades found"}, 404

    number_of_pages = ceil(number_of_trades / page_rate)
    if page >= number_of_pages or page < 0:
        return {"status": "failure","message": "Page not found"}, 404

    if sort_by:
        searchResults = sortTrades(searchResults, sort_by, isdesc)
        if isinstance(searchResults, str):
            return {"status": "failure","message": "Invalid sortby property name", "sortbyReceived": sort_by, "sortbyList": sortbyList}, 400

    result = {
        "status": "success",
        "page": str(page+1)+"/"+str(number_of_pages),
        "page_rate": page_rate,
        "total_trades": number_of_trades,
        "trades": searchResults[page * page_rate: (page + 1) * page_rate]
    }
    return result

# for getting filtered trades based on different filters
@app.get("/filter")
def filter_trades_paginated(page: int, page_rate: Optional[int]=10, asset_class: Optional[str] = None, end: Optional[dt.datetime] = None, start: Optional[dt.datetime] = None, max_price: Optional[float] = None, min_price: Optional[float] = None, trade_type: Optional[str] = None, sort_by: Optional[str] = None, isdesc: Optional[bool] = False):
    page = page - 1
    if page_rate <= 0:
        return {"status": "failure","message": "Oops! Invalid page rate"}, 400
    filteredTrades = trades
    if asset_class:
        filteredTrades = [trade for trade in filteredTrades if trade.asset_class == asset_class]
    if end:
        filteredTrades = [trade for trade in filteredTrades if trade.trade_date_time <= end]
    if start:
        filteredTrades = [trade for trade in filteredTrades if trade.trade_date_time >= start]
    if max_price:
        filteredTrades = [trade for trade in filteredTrades if trade.trade_details.price <= max_price]
    if min_price:
        filteredTrades = [trade for trade in filteredTrades if trade.trade_details.price >= min_price]
    if trade_type:
        filteredTrades = [trade for trade in filteredTrades if trade.trade_details.buySellIndicator == trade_type]

    number_of_trades = len(filteredTrades)
    if number_of_trades == 0:
        return {"status": "failure","message": "No trades found"}, 404
    number_of_pages = ceil(number_of_trades / page_rate)

    if page >= number_of_pages or page < 0:
        return {"status": "failure","message": "Page not found"}, 404
    
    if sort_by:
        filteredTrades = sortTrades(filteredTrades, sort_by, isdesc)
        if isinstance(filteredTrades, str):
            return {"status": "failure","message": "Invalid sortby property name", "sortbyReceived": sort_by, "sortbyList": sortbyList}, 400

    result = {
        "status": "success",
        "page": str(page+1)+"/"+str(number_of_pages),
        "page_rate": page_rate,
        "total_trades": number_of_trades,
        "trades": filteredTrades[page * page_rate: (page + 1) * page_rate]
    }

    return result

# main method
if __name__ == "__main__":
    uvicorn.run("app:app")
