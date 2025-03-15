from pytz import utc
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler =  AsyncIOScheduler(timezone=utc)