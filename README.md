

<h1 align="center">Scott's Stocks</h1>

<div align="center">

  [![Status](https://img.shields.io/badge/status-active-success.svg)]() 

</div>

---

<p align="center"> A full stack application to help choose stocks for trading algorithms. This also includes a SQLite database of historical data to train the algorithms on.
    <br> 
</p>

## 📝 Table of Contents
- [About](#about)
- [Usage](#usage)
- [TODO](../TODO.md)
- [Built Using](#built_using)
- [Authors](#authors)


## 🧐 About <a name = "about"></a>
With inspiration from several trading and investors across the internet, the goal is to create a full stack application that I can deploy and use as a market trading platform but also a way to find new opportunities.

So far this is a fairly simple project with only limitted support for trading strategies. But I will continue to add more generic strategies and custom ones going forward. 

There are also plans to support options and algorithmic trading in the future. 

I would love to create a bot that trades throughout the day and posts it's trades/value on a live chart.

![Screenshot of GME listing](screenshots/Screen%20Shot%202021-02-24%20at%2012.58.46%20PM.png)

## 🎈 Usage <a name="usage"></a>
This app is built on FastAPI and Uvicorn. To start a local Uvicorn server run:

```
uvicorn main:app --reload
```

Most development happens in the main.py file but there are other scripts to populate your database with stock data.

## 🚀 Deployment <a name = "deployment"></a>
This app is not ready for deployment as of yet, but to run it locally you need to populate a secrets.py file.

After creating the secrets.py file, you need to run a sequence of scripts to build oyur backend and database.

Run create_db.py to build your SQLite database and schema.
1. ```python create_db.py```

Run populate_stocks.py to populate the SQLite database with the ticker symbols and information about each company/etf/fund.

2. ```python populate_stocks.py```

Run populate_prices.py to gather the historical data for each symbol from the Alpaca API.

3. ```python populate_prices.py```

## To Do
- [x] Generate project scaffolding.
- [x] Build database and schema.
- [x] Make scripts to populate DB.
- [x] Populate the DB.
- [x] Create front end to display, sort, and find symbols.
- [x] Create details page to display symbol info.
- [x] Create trading strategies.
- [ ] Allow application of trading strategies by stock.
- [ ] Basic trading algorithm/bot.
- [ ] Execute trades by user direction.
- [ ] Execute trades by bot direction.
- [ ] Create trade tracker


## ⛏️ Built Using <a name = "built_using"></a>
- [SQLite](https://www.sqlite.org/index.html) - Database
- [FastAPI](https://fastapi.tiangolo.com/) - Server Framework
- [Semantic UI](https://semantic-ui.com/) - Frontend Framework
- [Uvicorn](https://www.uvicorn.org/) - Server Environment

## ✍️ Authors <a name = "authors"></a>
- [@scott-olson](https://github.com/scott-olson) 

See also the list of [contributors](https://github.com/Scott-Olson/Scotts_Stocks/graphs/contributors) who participated in this project.

## 🎉 Acknowledgements <a name = "acknowledgement"></a>
  Check out [Part Time Larry](https://www.youtube.com/channel/UCY2ifv8iH1Dsgjrz-h3lWLQ) for inspiration and tutorials.