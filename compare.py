#!/usr/bin/python3
import os
import yaml


def parse_mc(data, object, name):
    for file in data.get("spec").get("config").get("storage").get("files"):
        key = file.get("path")
        object[key] = {}
        object[key]["contents"] = file.get("contents").get("source")
        object[key]["object-name"] = name


def parse_td(data, object):
    profiles = data.get('spec').get('profile')
    for profile in profiles:
        key = profile.get('name')
        object[key] = profile.get('data')


def parse_kc(data, object):
    kc = data.get('spec').get('kubeletConfig')
    if object.get('kc') != None:
        print(f"Multiple kubelet configurations found: {object.get('kc')}")
        return
    object['kc'] = kc

def parse_items(sets):
    for dset in sets:
        files, set = dset[0], dset[1]
        for item in files:
            with open(item, 'r') as file:
                data = yaml.safe_load(file)
                name = data.get("metadata").get("name")
                if data.get("kind") == "MachineConfig":
                    parse_mc(data, set['mc'], name)
                if data.get("kind") == "Tuned":
                    parse_td(data, set['td'])
                if data.get("kind") == "KubeletConfig":
                    parse_kc(data, set['kc'])


def compare_kc(set1, set2):
    print(f"kubeletconfigs are {'identical' if set1 == set2 else 'different'}")


def compare_td(set1, set2):
    identical = True
    for key in set1:
        v1 = set1.get(key).split('\n')
        v2 = set2.get(key, '').split('\n')
        if v2 == '':
            print(f"{key} is found in set1 and not found in set 2")
            continue
        for idx in range(len(v1)):
            if v1[idx] != v2[idx]:
                print(f">>{v1[idx]}")
                print(f"<<{v1[idx]}")
                identical = False
    print(f"Tuned profiles are {'identical' if identical else 'different'}")


def compare_mc(set1, set2):
    for key in set1:
        v1 = set1.get(key)
        v2 = set2.get(key, '')
        if v2 == '':
            print(f"{key} is found in set1 and not found in set 2")
            print(v1)
            print(v2)
            continue
        if v1.get('contents') != v2.get('contents'):
            print(
                f"different: key {key}, MachineConfig {v1.get('object-name')}")
            print(f"set1 {v1.get('contents')}")
            print(f"set2 {v2.get('contents')}")


def compare_items(set1, set2):
    for item, func in zip(
            ('mc', 'kc', 'td'), (compare_mc, compare_kc, compare_td)):
        func(set1.get(item), set2.get(item))


def init():
    d1 = {
        "mc": {},
        "td": {},
        "kc": {}
    }
    d2 = {
        "mc": {},
        "td": {},
        "kc": {}
    }
    return d1, d2


if __name__ == "__main__":
    d1, d2 = init()
    day1_files = [os.path.join("day1", f) for f in os.listdir("day1")]
    day2_files = [os.path.join("day2", f) for f in os.listdir("day2")]

    parse_items([[day1_files, d1,], [day2_files, d2]])
    compare_items(d1, d2)
