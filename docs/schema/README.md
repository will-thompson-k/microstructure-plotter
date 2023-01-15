# Schema

Here are the fields and data types expected for each data input. Only the quote data is a required input. All others are optional. 

## Quote Data

- **timestamp:** Nanosecond precision EPOCH timestamp INT
- **symbol:** STR 
- **bid_price:** FLOAT 
- **ask_price:** FLOAT 
- **micro_price:** FLOAT 

## Trade Data

- **timestamp:** Nanosecond precision EPOCH timestamp INT
- **symbol:** STR 
- **price:** FLOAT 

## Fill Data 

- **timestamp:** Nanosecond precision EPOCH timestamp INT
- **symbol:** STR 
- **price:** FLOAT 
- **is_buy:** BOOL 
- **is_aggressive:** BOOL 

## Orders Data 

- **timestamp:** Nanosecond precision EPOCH timestamp INT
- **symbol:** STR 
- **price:** FLOAT 
- **is_new:** BOOL 
- **is_cancel:** BOOL 
- **is_reject:** BOOL 
- **is_ack:** BOOL 

## Valuation Data 

- **timestamp:** Nanosecond precision EPOCH timestamp INT
- **symbol:** STR 
- **theo_price:** FLOAT 

## Code 

Reference [microplot::schema](/microplot/schema.py).