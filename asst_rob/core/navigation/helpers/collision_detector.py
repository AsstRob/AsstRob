from asst_rob.core.directions import Directions
from asst_rob.core.navigation.base_navigator import BaseNavigator


class CollisionDetector(BaseNavigator):

    def __init__(self):
        super().__init__()
        self.__turn_label = Directions.NONE       # If a turn(s) is/are taken, which side: 0 - no turns, 1 - left(s), 2 - right(s)
        self.__turn_count = 0       # How many turns taken to that side: 0 - no turns (a counter turn to the label side will decrease __turn_count by 1)
        self.__side = Directions.NONE             # Which side of the path the asstrob is on: 0 - center, 1 - left, 2 - right

    def __get_collision_data(self):
        """
        This function will check for the 3 ultrasonic sensor data separately.
        Based on the sensory values, 3 values of a tuple will be passed either any collisions from left, mid, right sensors

        :returns (tuple): if there are collisions (True: No collision, False: colliding)
        """
        return True, True, True

    def get_direction(self):
        """
        This is the entry point for pilot module to check for the next movement direction from collision detector.
        Will check for any collisions and fixes for making asstrob facing forward and send any signal to fix that.
        If all the 3 sensors are sending false signal, only then the returned signal will be reverse.
        Otherwise, if there are any collisions or fixes the signal will be left/right, or none if there are no collisions

        :return (Directions): If there are any fixes a Directions signal will be sent
        """
        collision_data = self.__get_collision_data()

        if not collision_data[0] and not collision_data[1] and not collision_data[2]:
            """All sensors are blocked."""
            return Directions.REVERSE
        elif self.__turn_label == Directions.NONE:
            """No turns to be fixed. AsstRob going straight."""
            if collision_data[3]:
                """Center sensor has no collisions. Won't have collisions."""
                return Directions.NONE
            else:
                if self.__side == Directions.NONE:
                    """In center of the path."""
                    if collision_data[0]:
                        """
                            Left is clear. Takes a left.
                            Set __side to LEFT
                            Set __turn_count (to left) to 1
                            Set __turn_label to LEFT
                            
                            :return (Direction): LEFT
                        """
                        # self.__side = Directions.LEFT
                        self.__turn_count = 1
                        self.__turn_label = Directions.LEFT
                        return Directions.LEFT
                    else:
                        """Takes a right"""
                        return Directions.RIGHT
                elif self.__side == Directions.LEFT:
                    """In the left side of the path."""
                    if collision_data[2]:
                        """
                        If right turn is possible.
                        Set __side to RIGHT if AsstRob is now on right side
                        Set __turn_count (to right) to 1
                        Set __turn_label to RIGHT
                        
                        :return (Direction): RIGHT
                        """
                        # self.__side = Directions.RIGHT            # Changing sides needs to be fixed
                        self.__turn_count = 1
                        self.__turn_label = Directions.RIGHT
                        return Directions.RIGHT
                    else:
                        """
                        Takes a left.
                        Set __turn_count (to left) to 1
                        Set __turn_label to LEFT
                        
                        :return (Direction): LEFT
                        """
                        self.__turn_count = 1
                        self.__turn_label = Directions.LEFT
                        return Directions.LEFT

                elif self.__side == Directions.RIGHT:
                    """In the right side of the path."""
                    if collision_data[1]:
                        """
                        If left turn is possible.
                        Set __side to LEFT if AsstRob is now on left side
                        Set __turn_count (to left) to 1
                        Set __turn_label to LEFT

                        :return (Direction): LEFT
                        """
                        # self.__side = Directions.RIGHT            # Changing sides needs to be fixed
                        self.__turn_count = 1
                        self.__turn_label = Directions.LEFT
                        return Directions.LEFT
                    else:
                        """
                        Takes a right.
                        Set __turn_count (to right) to 1
                        Set __turn_label to RIGHT

                        :return (Direction): RIGHT
                        """
                        self.__turn_count = 1
                        self.__turn_label = Directions.RIGHT
                        return Directions.RIGHT

        elif self.__turn_label == Directions.LEFT:
            """AsstRob had turned to left needs to be fixed with right turn(s)."""
            pass
        elif self.__turn_label == Directions.RIGHT:
            """AsstRob had turned to right needs to be fixed with left turn(s)."""
            pass

        return Directions.NONE


