import SvrHelperFuncs

class PrecDemo:
    def __init__(self, path, title, intervals, demo_next):
        self.path = path  # location of demo file on disk
        self.title = title  # name of demo file
        self.intervals = intervals  # intervals to record
        self.rec_title = SvrHelperFuncs.clean_demo_title(title)
        self.demo_next = demo_next  # name of next demo to play

