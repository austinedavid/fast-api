old_list = [
    {"id": 1, "name": "David"},
    {"id": 2, "name": "Mesoma"},
    {"id": 3, "name": "Augustine"},
    {"id": 4, "name": "Ugochukwu"},
    {"id": 5, "name": "Ezeme"},
]

old_list = list(filter(lambda item: item["id"] != 1, old_list))
print(old_list)
