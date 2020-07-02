from asst_rob.core.navigation.base_navigator import BaseNavigator


class Navigator(BaseNavigator):

    def __init__(self):
        super().__init__()

    def get_direction(self):

        return self.__direction