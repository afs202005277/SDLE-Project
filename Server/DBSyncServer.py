import schedule
import functools
import time
from env import SYNC_DB_REPLICAS_EVERY_X_MINUTES, NUM_REPLICAS
from DatabaseManagement import DatabaseManagement

db_manager = DatabaseManagement()

sync_replicas = functools.partial(db_manager.sync_replicas, NUM_REPLICAS)

sync_replicas()

schedule.every(SYNC_DB_REPLICAS_EVERY_X_MINUTES).minutes.do(sync_replicas)

while True:
    schedule.run_pending()
    time.sleep(1)