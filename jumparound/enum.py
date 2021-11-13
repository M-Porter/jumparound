from enum import IntEnum


class ViewMode(IntEnum):
    BASIC = 1
    FULL = 2
    COMBINED = 3

    def next(self):
        if self.value == max(ViewMode):
            return ViewMode(min(ViewMode))
        return ViewMode(self.value + 1)
