"""
translated using chatgpt 3.5 from 
https://github.com/keepacom/api_backend/blob/master/src/main/java/com/keepa/api/backend/helper/KeepaTime.java
"""
import time
import math

class KeepaTime:
    keepaStartHour = 359400
    keepaStartMinute = 21564000

    @staticmethod
    def nowHours():
        return KeepaTime.unixInMillisToKeepaHour(int(time.time() * 1000))

    @staticmethod
    def nowMinutes():
        return KeepaTime.unixInMillisToKeepaMinutes(int(time.time() * 1000))

    @staticmethod
    def unixInMillisToKeepaMinutes(unix):
        return int((math.floor(unix / (60 * 1000))) - KeepaTime.keepaStartMinute)

    @staticmethod
    def unixInMillisToKeepaHour(unix):
        return int((math.floor(unix / (60 * 60 * 1000))) - KeepaTime.keepaStartHour)

    @staticmethod
    def keepaHourToUnixInMillis(hour):
        return hour * 60 * 60 * 1000 + KeepaTime.keepaStartHour * 60 * 60 * 1000

    @staticmethod
    def keepaMinuteToUnixInMillis(minute):
        return minute * 60 * 1000 + KeepaTime.keepaStartMinute * 60 * 1000

    @staticmethod
    def keepaMinuteToUnixInMillis_str(minute):
        return KeepaTime.keepaMinuteToUnixInMillis(int(minute))

