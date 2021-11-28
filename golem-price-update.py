#!/usr/local/bin/python3
import requests
import os
import argparse
import subprocess
import sys
import time

def parse_args():
    parser = argparse.ArgumentParser(description="automatically adjust golem provider prices")
    parser.add_argument("--currency",type=str,help="desired fiat currency for prices",default="USD")
    
    # TODO: if there's some kind of API for getting your local electricty costs feel free to submit a PR
    parser.add_argument("--price_kwh",type=float,help="electricity price per kwH",default=0.1)
    parser.add_argument("-w","--watts",type=int,help="power usage of your provider in watts",default=150)
    # TODO: add option to target earnings that could have been made by mining a coin/other workload
    parser.add_argument("-p","--profit",type=float,help="desired additional profit beyond electricity costs, (1.0 is 100 percent)",default=0.1)
    parser.add_argument("-t","--threads",type=int,help="number of threads on golem provider (default is all threads)",default=os.cpu_count())

    # TODO: add option to go based off of prices of similar nodes instead of electricty cost

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    request = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids=golem&vs_currencies={args.currency}")
    json_data = request.json()
    glm_price = json_data["golem"][args.currency.lower()]

    cost_per_hour = (args.watts * 0.001) * args.price_kwh
    desired_income_per_hour = cost_per_hour * (1 + args.profit)
    price_per_thread_fiat = desired_income_per_hour / args.threads
    price_per_thread_glm = price_per_thread_fiat * (1 / glm_price)
    # set the price
    golem_path = os.path.expanduser("~/.local/bin/golemsp")
    subprocess.call([golem_path,"settings","set","--cpu-per-hour",str(price_per_thread_glm)])
    subprocess.call([golem_path,"settings","set","--env-per-hour","0"])
    subprocess.call([golem_path,"settings","set","--starting-fee","0"])


