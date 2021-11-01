from django.http.response import JsonResponse
from django.shortcuts import render
import pymongo
import json
# Create your views here.


def get_collections(requests, count):
    conn_str = "mongodb://p:Q3HE2B7iiqQXU5xDG6@161.97.105.217/nfts?retryWrites=true&w=majority"
    client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
    db = client.nfts
    d = list(db.collections.find({}))
    sorted_list = sorted(d, key=lambda d: d['stats']['totalVolume'])

    payload = sorted_list[-count:]
    payload.reverse()

    data = {}
    for i in range(len(payload)):
        data[i] = payload[i]

    return JsonResponse(data)


def get_collections_by_days(requests, days):
    conn_str = "mongodb://p:Q3HE2B7iiqQXU5xDG6@161.97.105.217/nfts?retryWrites=true&w=majority"
    client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
    db = client.nfts
    d = list(db.collections.find({}))

    if days == 1:
        sorted_list = sorted(d, key=lambda d: d['stats']["oneDayVolume"])
    elif days == 7:
        sorted_list = sorted(d, key=lambda d: d['stats']["sevenDayVolume"])
    elif days == 30:
        sorted_list = sorted(d, key=lambda d: d['stats']["thirtyDayVolume"])

    payload = sorted_list[-20:]
    payload.reverse()

    data = {}
    for i in range(len(payload)):
        data[i] = payload[i]

    return JsonResponse(data)

def get_collection_details(request,collection_name):
    conn_str = "mongodb://p:Q3HE2B7iiqQXU5xDG6@161.97.105.217/nfts?retryWrites=true&w=majority"
    client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
    db = client.nfts
    d = list(db.collections.find({}))
    final_list = []

    for i in d:
        if i['_id'].find(collection_name) != -1:
            final_list.append(i)

    sorted_list = sorted(final_list, key=lambda final_list: final_list['stats']['totalVolume'])

    sorted_list.reverse()

    data = {}
    for i in range(len(sorted_list)):
        data[i] = sorted_list[i]

    return JsonResponse(final_list)