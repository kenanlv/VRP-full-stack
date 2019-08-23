from huey import MemoryHuey
from app import db
from huey import crontab

huey = MemoryHuey()

# @huey.periodic_task(crontab(minute='0', hour='3'))
# @huey.periodic_task(crontab(minute='*/3')) #for every three minute
@huey.periodic_task(crontab(minute='*/1'))
def every_six_seconds():
    print('This task runs every six seconds')
