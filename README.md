# SillyMoney

SillyMoney is a simple stock market simulator that let's you develop some intuition for short-term trading of securities. All of the data in SillyMoney is real, historical day-resolution stock data scraped from either AMEX, NASDAQ, or NYSE stock exchanges between the dates of January 1st 2010 and January 1st 2017.

The basis of the simulator is that one of 4000+ securities is chosen at random and presented to the user on a random date between 2010 and 2017. The user is shown historical pricing for this security over the last year and is given three choices: *Buy*, *Sell*, or *Advance*. Choosing *Buy* will purchase a single share of the security at the current market price and advance forward in time one day. Choosing *Sell* will sell all held shares (if any) at the current market price and begin the process over with a new security. Choosing *Advance* will advance forward in time one day without any action. In addition to these three options, the user may also quit at any time and save their results via the command line prompt. Below is a visual explanation of the interface:

![](fig1.png?raw=true)

The user is encouraged to develop a strategy that allows them to maintain a high average daily return over many days of trading, and a summary of the user's performance is routinely printed to the standard output. Of course, SillyMoney is only meant to provide intuition for design of a successful trading algorithm, and a more complete simulator (such as [Quantopian](http://quantopian.com)) should be used to perform rigorous backtesting.



## Setup
Prerequisites:  
Python 3  
Numpy  
Matplotlib  

The simulation is managed by `Broker` as defined in `sim.py` and running the simulator is as simple as `python sim.py`.
There are some adjustable parameters as described in Broker, and the user may also experiment with passing scalar or vector analysis functions to Broker as explained in the documentation.
