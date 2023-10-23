import berkeleydb

db_path = "./databases/test_db.db"
db = berkeleydb.hashopen(db_path, "c")  # "c" indicates create mode

# Insert data into the database
key = b"my_key"
value = b"my_value"
db[key] = value

# Retrieve data from the database
retrieved_value = db.get(key, None)
if retrieved_value is not None:
    print(f"Key: {key}, Value: {retrieved_value.decode('utf-8')}")

# Delete data from the database
if key in db:
    del db[key]

db.close()
