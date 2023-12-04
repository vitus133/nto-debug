#!/usr/bin/python3
import os
import yaml


def parse_mc(data, object):
    for file in data.get("spec").get("config").get("storage").get("files"):
        key = file.get("path")
        object[key] = {}
        object[key]["contents"] = file.get("contents").get("source")


def parse_td(data, object):
    profiles = data.get('spec').get('profile')
    for profile in profiles:
        key = profile.get('name')
        object[key] = profile.get('data')


def parse_kc(data, object):
    kc = data.get('spec').get('kubeletConfig')
    if object.get("KubeletConfig") is not None:
        print(f'Multiple kubelet configurations found:',
              f'{object.get("KubeletConfig")}')
        return
    object["KubeletConfig"] = kc


# parsers.keys() can be used for iteration as dict maintains insertion order
# since python 3.7
parsers = {
    "MachineConfig": parse_mc,
    "Tuned": parse_td,
    "KubeletConfig": parse_kc
}


def parse_items(sets):
    for dset in sets:
        files, set = dset[0], dset[1]
        for item in files:
            with open(item, 'r') as file:
                data = yaml.safe_load(file)
                kind = data.get("kind")
                if kind not in parsers.keys():
                    continue
                parsers[kind](data, set[kind])


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
            parsers.keys(), (compare_mc, compare_td, compare_kc)):
        func(set1.get(item), set2.get(item))


def init():
    d1 = {
        "MachineConfig": {},
        "Tuned": {},
        "KubeletConfig": {}
    }
    d2 = {
        "MachineConfig": {},
        "Tuned": {},
        "KubeletConfig": {}
    }
    return d1, d2


if __name__ == "__main__":
    d1, d2 = init()
    day1_files = [os.path.join("day1", f) for f in os.listdir("day1")]
    day2_files = [os.path.join("day2", f) for f in os.listdir("day2")]

    parse_items([[day1_files, d1,], [day2_files, d2]])
    compare_items(d1, d2)
