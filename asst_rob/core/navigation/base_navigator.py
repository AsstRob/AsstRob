from threading import Thread

from asst_rob.core.directions import Directions


class BaseNavigator(Thread):

    def __init__(self):
        """
            There are 4 directions represented from integers 1-4 (These values will be used for directions in the whole project)
            1 - Left
            2 - Right
            3 - Forward
            4 - Reverse
        """
        super().__init__()
        self.__direction = Directions.FORWARD

    def get_direction(self):
        return self.__direction

    def update_direction(self, direction):
        self.__direction = direction
