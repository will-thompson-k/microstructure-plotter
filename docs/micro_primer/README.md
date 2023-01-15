
# Microstructure Primer

Markets can be decomposed into exchanges and the participants that trade on those exchanges: 

1. **"market makers" or "scalpers" or "liquidity providers":** those offering to provide a quantity needed for a theoretical premium over what they think the security is worth.  

2. **"takers"**, those who want a certain amount of a security and are willing to "take" the market makers' price. They could want to get into that position for a number of reasons: 

- they think the <ins>market is mispriced</ins> (relative to their own view on whatever horizon they think) 
- they are trying to <ins>hedge a risk</ins> in their portfolio 
- they are executing for behalf of a client 

Of course, most sophisticated players <ins>don't fall cleanly</ins> into either of these categories. 

Generally, there are _more market makers_ than _takers_ at any given time. 

The market makers compete with one another either by providing **better prices**, or **offering more size**, or having **waited around in a queue longer** (time priority), or **paying for the right to match first** (think "free" brokerage companies selling your orders). Their price and quantities are **aggregated** by the exchange to form a **"central limit order book"** (CLOB), which reflect the current overall "best market price" to buy or sell a security at any time. 

The exchange provides the platform (i.e. software) for the makers and takers to meet and trade. In the event that a taker wants to initiate a trade  (be the "aggressor"), the exchange has a **matching engine** with a series of rules to determine how much of the taker's order to allocate to each of the market makers' orders (the "passive parties"). _Different matching engines rules incentivize different types of competition among market makers._

[order book](/assets/order_book.png)

The exchange software has a number of connected nodes, chief among them: 

- **an order book**: a data structure aggregating the market makers' orders into "the market" for a given security 
- **a matching engine**: adds orders to the order book and executes trades between parties, allocating a given taker's order among the market makers  
- **a pricefeed**: disseminates quotes, trades, etc - changes in public market state (unless it's a dark pool!) 
- **an order gateway**: an API for participants to communicate their price and quantity preferences to the exchange - depending on the exchange, there might be a multitude of order types (particularly if there are restrictions like REG NMS) 

How these participants interact, their impact on market prices, and the way exchange software behave are <ins>**market microstructure**</ins>.

Since most of these participants are actually **trading algos** 🤖, the timescales at which all these interactions occur is _quite small_. In many web-based AI applications, **25 milliseconds (ms)** is considered a bleeding edge response time (also accounting for the fact that internet is a very unpredictable and slow medium). For most of these market participants to compete, they need response times of **<1 microsecond (us)** ⏰.

The pace at which market prices change depends on the regime: if it's 7pm on a Thursday, there may be barely any updates within an hour. If it's [**non-farm payrolls**](https://www.cnbc.com/nonfarm-payrolls/), then there is likely a _ton_ of activity and the exchange is likely overloaded/queuing. 

This means that raw market data is fundamentally **_asynchronous_, _non-uniform_, _event-level_ time series**. 

For a very confusing, vague explanation, read the Wikipedia article [here](https://en.wikipedia.org/wiki/Market_microstructure).