# golem-price-updater
automatically adjust the price for your golem node based on the current price of GLM

# Usage:
set this file to run as a cron job every hour (or as often as you see fit)
1. make the file executable
```chmod +x golem-price-update.py```

1.  add it to your crontab (with `crontab -e`)

    ```0 * * * * /path/to/golem-price-update.py > /dev/null```

    you can provide parameters to tell the script how to estimate the cost

    ```0 * * * * /path/to/golem-price-update.py --currency EUR --watts 250 --price_kwh 0.17 > /dev/null```

for a full list of options see `golem-price-update.py --help`
```
usage: golem-price-update.py [-h] [--currency CURRENCY] [--price_kwh PRICE_KWH] [-w WATTS] [-p PROFIT] [-t THREADS]

automatically adjust golem provider prices

optional arguments:
  -h, --help            show this help message and exit
  --currency CURRENCY   desired fiat currency for prices
  --price_kwh PRICE_KWH
                        electricity price per kwH
  -w WATTS, --watts WATTS
                        power usage of your provider in watts
  -p PROFIT, --profit PROFIT
                        desired additional profit beyond electricity costs, (1.0 is 100 percent)
  -t THREADS, --threads THREADS
                        number of threads on golem provider (default is all threads)
```
