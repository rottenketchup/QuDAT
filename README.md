# CS-Project

Model: represents the state of the application and any business logic or operations that should be performed by it. Business logic should be encapsulated in the model, along with any implementation logic for persisting the state of the application.

View: responsible for presenting content through the user interface. There should be minimal logic within views, and any logic in them should relate to presenting content.

Controller: Controllers are the components that handle user interaction, work with the model, and ultimately select a view to render. The view only displays information; the controller handles and responds to user input and interaction. In the MVC pattern, the controller is the initial entry point, and is responsible for selecting which model types to work with and which view to render (hence its name - it controls how the app responds to a given request).

definitions adapted from: https://docs.microsoft.com/en-in/aspnet/core/mvc/overview?WT.mc_id=dotnet-35129-website&view=aspnetcore-6.0

1. input query (from view)
2. process query (controller and model)
    * identify user intent (what information regarding the company do they want?: revenue, market cap, free cash flow, and so on)
    * identify the company name and find the company's ticker symbol
3. scrape and cleanse the relevant data needed (controller and model)
4. format and display retrieved data (controller and view)

Every query should be matched to one of the following intents:
    - company profile
        * one line of long business summary
        * country
        * industry

    - stock price/stock price history
        * current, open, day high & low, previous close
        * 52-week-high & low
        
    - market cap
    - PE ratio 
        forward, trailing PE
    - EPS
    - volume
    - dividend rate
        5 year average too, trailing annual
    
    - revenue
    - gross/operating/net margins
    - financials (quarter or year?)
        sales, cost of revenue, gross income, opex, operating income, net income

    - returns/growth
        average return, earnings growth (earnings quarterly growth?), revenue growth
    - analyst reports
        * 1 year target (target low price, target median price or target mean price, target high price)
        * recommendation mean, numberOfAnalystOpinions


(output shortName, if available, before any response)


write tests: https://realpython.com/python-testing/#testing-your-code
