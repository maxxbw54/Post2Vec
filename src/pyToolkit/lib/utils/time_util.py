# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：		time_util
   Description :	
   Author :			bowenxu
   Create date：		12/9/18
   Update date:		12/9/18
-------------------------------------------------
"""

import datetime


class Timer:
    start_time = None
    end_time = None

    def set_start_time(self):
        self.start_time = datetime.datetime.now()

    def set_end_time(self):
        self.end_time = datetime.datetime.now()

    def get_time_diff_in_seconds(self):
        if self.start_time is None or self.end_time is None:
            return None
        time_diff = self.end_time - self.start_time
        return time_diff.seconds


def get_current_time():
    import time
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
