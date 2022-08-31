# 2023 [Backend Project] Searching Tweets

## Approach

I have used inversted index approach to find te queries faster in large datasets. Once inversted index is created for all the words present in dataset, I look for the query structure and try to peroform operations on it. I have shown results and time taken by different queries in the code itself.

Design decisions, tradeoffs, or assumptions:

For solving expressions in query I have used expression_list stack approach other than stack which holds result of query
Storage space would be more compare to starter code as I am using lists to solve logical expressions withing query.
Assumptions querys would not be having irrelevant spaces or invalid operaters other than mentioned in the instructions given prehand.


## Running instructions

python starter_code.py

## Complexity analysis
Indexing takes O(n*m) where n is number of tweets and m is the number of words in each tweet

Searching takes O(n) where n is the number of words in query.

Retrieving top 5 rakes O(n) where n is number of tweets