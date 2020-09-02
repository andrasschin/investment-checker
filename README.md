# InvestmentChecker
A simple Python program that let's you track your long-term investments on the stock market.

# Usage
After running `main.py` the main menu opens up. The main menu has 3 elements: __My Stocks, Add Stock, Create Report__.

## My Stocks
The My Stocks window simply displays the added stocks.

## Add Stock
Here the user can add stocks to the program. Investment Checker uses [yahooquery](https://pypi.org/project/yahooquery/) so to find stocks make sure to use the stocks' ticker
from [Yahoo Finance](finance.yahoo.com) (e.g. iShares Core S&P 500 ETF can be found simply by SXR8 on Google Finance, but on Yahoo Finance you have to be more specific 
with SXR8.DE or SXR8.F). After finding the stock the user has to specify stock's quantity, buying price (using "." for decimal points) and the date on which the stock was bought (in the format YYYY.MM.DD). 
The program creates an excel sheet in __data/stocks.xlsx__ for every added stock.

## Create Report
By clicking on Create Report the program gets the current prices of the added stocks and then shows a summary about the stocks and their gains/losses. Clicking the __Log__ button, 
Investment Checker logs the data in __data/stocks.xlsx__ to the proper sheet and creates two basic charts about the stock's performance. Investment Checker also creates summary
sheets for each used currency.

# Missing features
These features are currently missing from Investment Checker, since they weren't a priority for the creator. They might be added later.
- Deleting/editing stocks (these can be manually done in __data/stocks.csv__)
- Sorting the stocks in My Stocks and Create Report

# Images
![alt text](https://i.imgur.com/aCBUOA5.png, "Create Report")
![alt text](https://i.imgur.com/pBpgFqh.png, "Example of excel sheet")
