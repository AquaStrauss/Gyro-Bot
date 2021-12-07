# Gyro-Bot
A bot dedicated for Gyro Discord

This bot use CoinGecko for their API to call some info for Gyro, Moralis for the price, and Subgraph for tha APY & RFV :

- $ping : Test if the bot response (If he is Online, or if he can write in this chan)

- $price : Give the actual price

- $gyro :
  - Rank / Current Price
  - Price Change 24H/7D
  - RFV / APY
  - Market Cap /Total Volume
  - Website (If one it given in CG)
  - Community (Same as above)

- $apy : Give the actual APY from Subgraph

- $rfv : Give the actual RFV from Subgraph

- $rewards 'bag value' : Math the rewards in different periods with the bag indicated.

Added a schedule command :

- $newSchedule 'Name, desc, date(year, month, day, hour, minute)' : Create a new schedule
  - e.g. : $newSchedule NameTest DescTest 2021 12 09 19 00

- $until 'schedule name' : Give you a countdown of the selected schedule

Think to modify the config file to add the api key of Discord and Moralis.
