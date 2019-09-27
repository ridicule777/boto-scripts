#!/usr/bin/env python3

import argparse
import datetime
import sys
from calendar import monthrange
from os import path

import yaml

import boto3


def get_number_of_days_in_a_month():
    now = datetime.datetime.utcnow()
    get_date = now.strftime('%Y-%m-%d')
    strip_date = get_date.split("-")
    year = int(strip_date[0])
    month = int(strip_date[1])
    day = int(strip_date[2])
    # import pdb
    # pdb.set_trace()
    if month == 1:
        previous_month = int(12)
        year = year - 1
    else:
        previous_month = int(month - 1)
        year = year

    total_number_of_days_in_previous_month = monthrange(year, previous_month)
    return year + '-' + previous_month + '-' + total_number_of_days_in_previous_month.split('-')


def get_project_list():
    if path.exists("tags.yaml"):
        with open('tags.yaml', 'r') as f:
            config = yaml.load(f)
            project_list = config.get(project)
    else:
        print("Config File missing. Exiting script..")
    return project_list


def get_cost_based_on_tags(project_list, region, start, end):
    for name in enumerate(project_list):
        results = []
        token = None
        cost_explore = boto3.client('ce', region)
        while True:
            if token:
                kwargs = {'NextPageToken': token}
            else:
                kwargs = {}
            data = cost_explore.get_cost_and_usage(TimePeriod={'Start': start, 'End':  end}, Granularity='DAILY', Metrics=['UnblendedCost'], GroupBy=[
                {'Type': 'DIMENSION', 'Key': 'LINKED_ACCOUNT'}, {'Type': 'DIMENSION', 'Key': 'SERVICE'}], Filter={'Tags': {'Key': 'Project', 'Values': [name]}} ** kwargs)
            results += data['ResultsByTime']
            token = data.get('NextPageToken')
            print(results)
            if not token:
                break


if __name__ == "__main__":

    previous_date = get_number_of_days_in_a_month()
    year = int(previous_date[0])
    month = int(previous_date[1])
    day = int(previous_date[2])
    start = year + '-' + month + '-' + '01'
    end = year + '-' + month + '-' + day
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--days', type=int,
                        default=total_number_of_days_in_previous_month)
    parser.add_argument('-r', '--region', type=string,
                        default="ap-south-1")
    args = parser.parse_args()
    region = args.region
    project_list = get_project_list()
    get_cost_based_on_tags(project_list, region, start, end)
