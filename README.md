# golem-price-updater
automatically adjust the price for your golem node based on the current price of GLM

# Usage:
set this file to run as a cron job every hour (or as often as you see fit)
1. make the file executable
```chmod +x golem-price-update.py```

1. run the program with your settings, and `-u` or `--update_cron` to add it to your crontab to run automatically. (requires the `python-crontab` module)
    
    example: `python3 golem-price-update.py -w 100 -p 0.5 --update_cron`


    you can also manually add it to your crontab (with `crontab -e`)

    ```0 * * * * /path/to/golem-price-update.py > /dev/null```

    you can provide parameters to tell the script how to estimate the cost

    ```0 * * * * /path/to/golem-price-update.py --currency EUR --watts 250 --price_kwh 0.17 > /dev/null```

for a full list of options see `golem-price-update.py --help`

```
usage: golem-price-update.py [-h] [--currency CURRENCY] [--price_kwh PRICE_KWH] [-w WATTS] [-p PROFIT] [-t THREADS] [-u] [--dry_run]

automatically adjust golem provider prices. GLM Price provided by CoinGecko

optional arguments:
  -h, --help            show this help message and exit
  --currency CURRENCY   desired fiat currency for prices, default: USD
  --price_kwh PRICE_KWH
                        electricity price per kwH in your fiat currency, default: 0.1
  -w WATTS, --watts WATTS
                        power usage of your provider in watts, default: 150
  -p PROFIT, --profit PROFIT
                        desired additional profit beyond electricity costs, (1.0 is 100 percent), default: 0.1 (10 percent)
  -t THREADS, --threads THREADS
                        number of threads on golem provider. t = 0 is all threads. t < 0 is t less that all threads. t > 1 is t threads. if t is higher than available threads, maximum of all
                        threads will be used. if all threads - t is less than 1, 1 thread will be used. default: all threads
  -u, --update_cron     run this script every hour with the same settings by adding it to the cron file
  --dry_run             display result but do not actually update, (applied to cron setting as well)
```


Pricing Data provided by CoinGecko
