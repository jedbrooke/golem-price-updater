#!/usr/local/bin/python3
import requests
import os
import argparse
import subprocess
import sys
import time
import shlex
import random

def parse_args():
    parser = argparse.ArgumentParser(description="automatically adjust golem provider prices. GLM Price provided by CoinGecko")
    parser.add_argument("--currency",type=str,help="desired fiat currency for prices, default: USD",default="USD")
    
    # TODO: if there's some kind of API for getting your local electricty costs feel free to submit a PR
    parser.add_argument("--price_kwh",type=float,help="electricity price per kwH in your fiat currency, default: 0.1",default=0.1)
    parser.add_argument("-w","--watts",type=int,help="power usage of your provider in watts, default: 150",default=150)
    # TODO: add option to target earnings that could have been made by mining a coin/other workload
    parser.add_argument("-p","--profit",type=float,help="desired additional profit beyond electricity costs, (1.0 is 100 percent), default: 0.1 (10 percent)",default=0.1)
    parser.add_argument("-t","--threads",type=int,help='''number of threads on golem provider. \n
    t = 0 is all threads. \n
    t < 0 is t less that all threads. \n
    t > 1 is t threads. \n
    if t is higher than available threads, maximum of all threads will be used. \n
    if all threads - t is less than 1, 1 thread will be used. \n
    default: all threads''',default=0)
    parser.add_argument("-u","--update_cron",action="store_true",help="run this script every hour with the same settings by adding it to the cron file")
    parser.add_argument("--dry_run",action="store_true",help="display result but do not actually update, (applied to cron setting as well)")

    # TODO: add option to go based off of prices of similar nodes instead of electricty cost

    return parser.parse_args()


def print_arg(k,v) -> str:
    if type(v) is bool:
        if v:
            return f"--{k}"
        else:
            return ""
    return f"--{k} {v}"

if __name__ == "__main__":
    args = parse_args()
    if args.update_cron:
        try:
            from crontab import CronTab
            from crontabs import CronTabs
        except ModuleNotFoundError:
            print("")
            print("module `python-crontab` is required to update the crontab, it can be installed with:")
            print("")
            print("pip3 install python-crontab")
            print("")
            exit(0)

        args_dict = vars(args)
        del args_dict["update_cron"]
        cmd = f"{os.path.abspath(__file__)} {' '.join([print_arg(k,v) for k,v in args_dict.items()])} > /dev/null 2>&1"
        comment = "update GLM price, set by script"
        cron = CronTab(user=True)
        job = cron.new(command=cmd,comment=comment)
        # TODO make this settable by an arg
        job.minute.on(random.randint(0,59))
        job.hour.every(1)
        if args.dry_run:
            print("removing the following jobs from crontab")
            print(*cron.find_comment(comment),sep="\n")
            print("adding the following to cron tab:")
            print(job)
        else:
            # remove old job
            cron.remove_all(comment=comment)
            cron.append(job)
            cron.write()

            


    request = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids=golem&vs_currencies={args.currency}")
    json_data = request.json()
    glm_price = json_data["golem"][args.currency.lower()]

    num_threads = os.cpu_count()
    if args.threads > 0:
        num_threads = min(os.cpu_count(),args.threads)
    if args.threads < 0:
        num_threads = max(os.cpu_count() + args.threads,1)

    cost_per_hour = (args.watts * 0.001) * args.price_kwh
    desired_income_per_hour = cost_per_hour * (1 + args.profit)
    price_per_thread_fiat = desired_income_per_hour / num_threads
    price_per_thread_glm = price_per_thread_fiat * (1 / glm_price)
    if args.dry_run:
        print("CPU per hour:",price_per_thread_glm)
    else:
        # set the price
        golem_path = os.path.expanduser("~/.local/bin/golemsp")
        
        # broken in yagna 0.9.1
        # cmd = f"{golem_path} preset update --no-interactive --price Duration=0 --price CPU={price_per_thread_glm/3600} --pricing linear vm"
        # print(cmd)
        # subprocess.call(shlex.split(cmd))
        # cmd = f"{golem_path} preset update --no-interactive --price Duration=0 --price CPU={price_per_thread_glm/3600} --pricing linear wasmtime"
        # subprocess.call(shlex.split(cmd))
        
        
        # fixed in yagna 0.9.1
        subprocess.call([golem_path,"settings","set","--cpu-per-hour",str(price_per_thread_glm)])
        subprocess.call([golem_path,"settings","set","--env-per-hour","0"])
        subprocess.call([golem_path,"settings","set","--starting-fee","0"])


