#!/usr/bin/python3
import os
import yaml


def parse_mc(data, object, name):
	for file in data.get("spec").get("config").get("storage").get("files"):
		key = file.get("path")
		object[key] = {}
		object[key]["contents"] = file.get("contents").get("source")
		object[key]["flie-name"] = name
	


def parse_items(sets):
	for dset in sets:
		files, set = dset[0], dset[1]
		for item in files:
			with open(item, 'r') as file:
				data = yaml.safe_load(file)
				if data.get("kind") == "MachineConfig":
					name = data.get("metadata").get("name")
					parse_mc(data, set['mc'], name)


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
			print(f"different: key {key}, file {v1.get('file-name')}")
			print(f"set1 {v1.get('contents')}")
			print(f"set2 {v2.get('contents')}")



if __name__ == "__main__":
	d1 = {}
	d1["mc"] = {}
	d2 = {}
	d2["mc"] = {}
	day1_files = [os.path.join("day1", f) for f in os.listdir("day1")]
	day2_files = [os.path.join("day2", f) for f in os.listdir("day2")]

	parse_items([[day1_files, d1,], [day2_files, d2]])
	compare_mc(d1.get('mc'), d2.get('mc'))



