from asst_rob.core.navigation.helpers.collision_detector import CollisionDetector
from asst_rob.core.navigation.helpers.navigator import Navigator


class Pilot:
    def __init__(self):
        super().__init__()
        self.__is_run = True
        self.__navigator = Navigator()
        self.__collision_detector = CollisionDetector()

    def travel(self):
        while self.__is_run:
            print("Traveling...")

        print("Stopped...")

    def stop(self):
        self.__is_run = False
        print("Stopping...")
