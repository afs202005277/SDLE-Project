import bsddb3.db as bdb

# Define the environment and database
env_file = "myenv"
db_file = "mydb.db"

env = bdb.DBEnv()

try:
    # Create the environment if it doesn't exist
    env.open(env_file, bdb.DB_CREATE | bdb.DB_INIT_LOCK | bdb.DB_INIT_LOG | bdb.DB_INIT_MPOOL | bdb.DB_INIT_TXN)

    # Create the database within the environment
    db = bdb.DB(env)
    db.open(db_file, db.DB_HASH, bdb.DB_CREATE)

    # Start a transaction
    txn = env.txn_begin()

    # Insert data into the database within the transaction
    db.put(b'key1', b'value1', txn)
    db.put(b'key2', b'value2', txn)

    # Commit the transaction to save the changes
    txn.commit()
    txn = None  # Transaction is complete, so set it to None

    # Read data from the database
    value1 = db.get(b'key1')
    value2 = db.get(b'key2')

    print(f'key1: {value1.decode()}')
    print(f'key2: {value2.decode()}')

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    if txn:
        # If there's an active transaction, abort it to discard changes
        txn.abort()
        db.close()
    if env is not None:
        env.close()
