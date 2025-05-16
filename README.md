# Manual Test Cases: Alpha Vantage currency_exchange_rate Endpoint

Goal: Verify API, that includes data formatting and ranges.
Non-Goal: Verifying the internal API logic

For manual tests, note that testing is relying on the external API availability
and might not be available. Executing tests will effect the allowed rate per
usage tier.

For each Persona a test suite should be generated - here to avoid duplication 
this is skipped.

Personas used for testing:
    1. Free_API_user
    2. Premium_API_user


## Endpoint: https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={FROM_CURRENCY}&to_currency={TO_CURRENCY}&apikey={YOUR_API_KEY}


# Test Cases - Overview

Test Case 1.1: Valid Currency Exchange (USD to EUR)

Test Case 1.2: Valid Currency Exchange (BTC to USD)

Test Case 1.3: Valid Currency Exchange (BTC to DOGE)

Test Case 2.1: Invalid from_currency Code

Test Case 2.2: Invalid to_currency Code

Test Case 2.3: Invalid from_currency and to_currency Code

Test Case 3.1: Missing from_currency Parameter

Test Case 3.2: Missing to_currency Parameter

Test Case 3.3: Missing both from_currency and to_currency Parameter

Test Case 4.1: Same from_currency and to_currency

Test Case 5.1: Case sensitivty of Currency Codes (lower)

Test Case 5.2: Case sensitivty of Currency Codes (Miexed Caser)

Test Case 6.1: Invalid API Key

Test Case 6.2: Demo API Key

Test Case 6.3: Missing API Key

Test Case 7.1: Rate limiting



Automated: Test Case 1.1, 6.3


## How to run the automated test
Make sure Python is installed and configured. Otherwise install Python
Install required Python modules via PIP if needed:
> pip install pytest pytest-mock requests pytest-html

Navigatre into the root directory (where this file is located)
run:
> pytest

Check terminal output and test results written to /results/report.html


# Manual Test Cases - detailed

### Test Case 1.1: Valid Currency Exchange (USD to EUR)
Test Case ID: CER-001

Description: Verify that a valid exchange rate is returned for a standard
physical currency pair (USD to EUR).

Steps:
1. Construct the API request URL with from_currency=USD, to_currency=EUR
and a valid apikey.
2. Send the request to the endpoint.
3. Observe the response.

Expected Result: 
    The API should return a JSON response containing the exchange rate
    information, including the fields 
        "Realtime Currency Exchange Rate", 
        "From_Currency Code", 
        "To_Currency Code", 
        "Exchange Rate", 
        "Last Refreshed", 
        "Time Zone", 
        "Bid Price",  
        "Ask Price". 
        The status code should be 200 OK.
Actual Result:
Pass/Fail:

### Test Case 1.2: Valid Currency Exchange (BTC to USD)
Test Case ID: CER-002

Description: Verify that a valid exchange rate is returned for a digital and 
physical currency pair (BTC to USD).

Steps:
1. Construct the API request URL with from_currency=BTC, to_currency=USD
       and a valid apikey.
2. Send the request to the endpoint.
3. Observe the response.

Expected Result: 
    The API should return a JSON response containing the exchange rate
    information, including the fields 
        "Realtime Currency Exchange Rate", 
        "From_Currency Code", 
        "To_Currency Code", 
        "Exchange Rate", 
        "Last Refreshed", 
        "Time Zone", 
        "Bid Price",  
        "Ask Price". 
        The status code should be 200 OK.
Actual Result:
Pass/Fail:

### Test Case 1.3: Valid Currency Exchange (BTC to DOGE)
Test Case ID: CER-003

Description: Verify that a valid exchange rate is returned for a digital
currency pair (BTC to DOGE).

Steps:
1. Construct the API request URL with from_currency=BTC, to_currency=DOGE
    and a valid apikey.
2. Send the request to the endpoint.
3. Observe the response.

Expected Result: 
    The API should return a JSON response containing the exchange rate
    information, including the fields 
        "Realtime Currency Exchange Rate", 
        "From_Currency Code", 
        "To_Currency Code", 
        "Exchange Rate", 
        "Last Refreshed", 
        "Time Zone", 
        "Bid Price",  
        "Ask Price". 
        The status code should be 200 OK.
Actual Result:
Pass/Fail:

### Test Case 2.1: Invalid from_currency Code
Test Case ID: CER-004

Description: Verify that an appropriate error is returned when an invalid 
from_currency code is provided.

Steps:
1.  Construct the API request URL with an invalid from_currency
(e.g., from_currency=XYZ), a valid to_currency (e.g., to_currency=USD), 
and a valid apikey.
2. Send the request to the endpoint.
3. Observe the response.

Expected Result: 
The API should return a JSON response containing the error message, including 
the field "Error Message" with the content "Invalid API call. 
Please retry or visit the documentation 
(https://www.alphavantage.co/documentation/) for CURRENCY_EXCHANGE_RATE."

Actual Result:
Pass/Fail:

### Test Case 2.2: Invalid to_currency Code
Test Case ID: CER-005

Description: Verify that an appropriate error is returned when an invalid 
to_currency code is provided.

Steps:
1.  Construct the API request URL with a valid from_currency
(e.g., from_currency=USD), and an invalid to_currency (e.g., to_currency=XYZ), 
and a valid apikey.
2. Send the request to the endpoint.
3. Observe the response.

Expected Result: 
The API should return a JSON response containing the error message, including 
the field "Error Message" with the content "Invalid API call. 
Please retry or visit the documentation 
(https://www.alphavantage.co/documentation/) for CURRENCY_EXCHANGE_RATE."

Actual Result:
Pass/Fail:

### Test Case 2.3: Invalid from_currency and to_currency Code
Test Case ID: CER-006

Description: Verify that an appropriate error is returned when an invalid 
from_currency and an invalid to_currency code is provided.

Steps:
1.  Construct the API request URL with an invalid from_currency
(e.g., from_currency=XYZ), and an invalid to_currency (e.g., to_currency=ZYX), 
and a valid apikey.
2. Send the request to the endpoint.
3. Observe the response.

Expected Result: 
The API should return a JSON response containing the error message, including 
the field "Error Message" with the content "Invalid API call. 
Please retry or visit the documentation 
(https://www.alphavantage.co/documentation/) for CURRENCY_EXCHANGE_RATE."

Actual Result:
Pass/Fail:


### Test Case 3.1: Missing from_currency Parameter
Test Case ID: CER-007

Description: Verify that an appropriate error is returned when a missing 
from_currency is provided.

Steps:
1.  Construct the API request URL with an empty from_currency
(e.g., from_currency=""), and a valid to_currency (e.g., to_currency=USD), 
and a valid apikey.
2. Send the request to the endpoint.
3. Observe the response.

Expected Result: 
The API should return a JSON response containing the error message, including 
the field "Error Message" with the content "Invalid API call. 
Please retry or visit the documentation 
(https://www.alphavantage.co/documentation/) for CURRENCY_EXCHANGE_RATE."

Actual Result:
Pass/Fail:

### Test Case 3.2: Missing to_currency Parameter
Test Case ID: CER-008

Description: Verify that an appropriate error is returned when a missing 
to_currency is provided.

Steps:
1.  Construct the API request URL with a vaild from_currency
(e.g., from_currency=USD), and an empty to_currency (e.g., to_currency=""), 
and a valid apikey.
2. Send the request to the endpoint.
3. Observe the response.

Expected Result: 
The API should return a JSON response containing the error message, including 
the field "Error Message" with the content "Invalid API call. 
Please retry or visit the documentation 
(https://www.alphavantage.co/documentation/) for CURRENCY_EXCHANGE_RATE."

Actual Result:
Pass/Fail:

### Test Case 3.3: Missing both from_currency and to_currency Parameter
Test Case ID: CER-009

Description: Verify that an appropriate error is returned when a missing 
to_currency is provided.

Steps:
1.  Construct the API request URL with an empty from_currency
(e.g., from_currency=""), and an empty to_currency (e.g., to_currency=""), 
and a valid apikey.
2. Send the request to the endpoint.
3. Observe the response.

Expected Result: 
The API should return a JSON response containing the error message, including 
the field "Error Message" with the content "Invalid API call. 
Please retry or visit the documentation 
(https://www.alphavantage.co/documentation/) for CURRENCY_EXCHANGE_RATE."

Actual Result:
Pass/Fail:

### Test Case 4.1: Same from_currency and to_currency
Test Case ID: CER-010

Description: Verify that a valid exchange rate is returned when valid 
currency codes are provided (EUR to EUR).

Steps:
1. Construct the API request URL with from_currency=EUR, to_currency=EUR
    and a valid apikey.
2. Send the request to the endpoint.
3. Observe the response.

Expected Result: 
    The API should return a JSON response containing the exchange rate
    information, including the fields 
        "Realtime Currency Exchange Rate", 
        "From_Currency Code", 
        "To_Currency Code", 
        "Exchange Rate", 
        "Last Refreshed", 
        "Time Zone", 
        "Bid Price",  
        "Ask Price". 
        The status code should be 200 OK.
Actual Result:
Pass/Fail:


### Test Case 5.1: Case sensitivty of Currency Codes (lower)
Test Case ID: CER-0011

Description: Verify that a valid exchange rate is returned when lowercase 
currency codes are provided (usd to eur).

Steps:
1. Construct the API request URL with from_currency=usd, to_currency=eur
    and a valid apikey.
2. Send the request to the endpoint.
3. Observe the response.

Expected Result: 
    The API should return a JSON response containing the exchange rate
    information, including the fields 
        "Realtime Currency Exchange Rate", 
        "From_Currency Code", 
        "To_Currency Code", 
        "Exchange Rate", 
        "Last Refreshed", 
        "Time Zone", 
        "Bid Price",  
        "Ask Price". 
        The status code should be 200 OK.
Actual Result:
Pass/Fail:


### Test Case 5.2: Case sensitivty of Currency Codes (Miexed Caser)
Test Case ID: CER-0012

Description: Verify that a valid exchange rate is returned when lowercase 
currency code is paired with a capitalized currency code are provided (usd to EUR).

Steps:
1. Construct the API request URL with from_currency=usd, to_currency=EUR
    and a valid apikey.
2. Send the request to the endpoint.
3. Observe the response.

Expected Result: 
    The API should return a JSON response containing the exchange rate
    information, including the fields 
        "Realtime Currency Exchange Rate", 
        "From_Currency Code", 
        "To_Currency Code", 
        "Exchange Rate", 
        "Last Refreshed", 
        "Time Zone", 
        "Bid Price",  
        "Ask Price". 
        The status code should be 200 OK.
Actual Result:
Pass/Fail:


### Test Case 6.1: Invalid API Key
Test Case ID: CER-0013

Description: Verify that an appropriate error is returned when an invalid API 
key is provided.

Steps:
1. Construct the API request URL with from_currency=USD, to_currency=EUR
    and an invalid apikey=invalidtestapikey.
2. Send the request to the endpoint.
3. Observe the response.

Expected Result: 
    The API should return a message indicating the use of an invalid key.
        The status code should be 200 OK.
Actual Result:
    The API does not check for invalid free keys, any key will result in a 
    response without any error message.
    Only the 'demo' key is checked and yields an information message. 
Pass/Fail:
    Fail

    
### Test Case 6.2: Demo API Key
Test Case ID: CER-0014

Description: Verify that an appropriate information is returned when the 'demo'
API key is provided.

Steps:
1. Construct the API request URL with from_currency=USD, to_currency=EUR
    and an invalid apikey=demo.
2. Send the request to the endpoint.
3. Observe the response.

Expected Result: 
    The API should return a message of type informaion with the following fields
    "Information": "The **demo** API key is for demo purposes only. 
    Please claim your free API key at 
    (https://www.alphavantage.co/support/#api-key) to explore our full API 
    offerings. It takes fewer than 20 seconds."
    The status code should be 200 OK.

Actual Result:
Pass/Fail:

### Test Case 6.3: Missing API Key
Test Case ID: CER-0015

Description: Verify that an appropriate error is returned when no
API key is provided.

Steps:
1. Construct the API request URL with from_currency=USD, to_currency=EUR
    and an invalid apikey=.
2. Send the request to the endpoint.
3. Observe the response.

Expected Result: 
    The API should return an error message with the following fields
     "Error Message": 
     "the parameter apikey is invalid or missing. Please claim your free API key 
     on (https://www.alphavantage.co/support/#api-key). It should take less than 
     20 seconds."
    The status code should be 200 OK.

Actual Result:
Pass/Fail:

### Test Case 7.1: Rate limiting
Test Case ID: CER-0016

Description: Observe the behavior when multiple requests are made, 
check for limiting

Steps:
0. Generate a new key
1. Construct the API request URL with from_currency=USD, to_currency=EUR
    and an invalid apikey=newKey.
2. Send the request to the endpoint.
3. Observe the response.
4. Repeat steps 2 and 3 for 25 times.

Expected Result: 
    The API should return an error message with the following fields
    "Information": 
    "We have detected your API key as newKey and our standard API rate limit is 
    25 requests per day. Please subscribe to any of the premium plans at 
    https://www.alphavantage.co/premium/ to instantly remove all daily rate 
    limits."
}
    The status code should be 200 OK.

Actual Result:
Pass/Fail:
