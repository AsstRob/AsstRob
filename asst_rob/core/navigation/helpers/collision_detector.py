from asst_rob.core.directions import Directions
from asst_rob.core.navigation.base_navigator import BaseNavigator


class CollisionDetector(BaseNavigator):

    def __init__(self):
        super().__init__()
        self.__turn_label = Directions.NONE       # If a turn(s) is/are taken, which side: 0 - no turns, 1 - left(s), 2 - right(s)
        self.__turn_count = 0       # How many turns taken to that side: 0 - no turns (a counter turn to the label side will decrease __turn_count by 1)
        self.__side = Directions.NONE             # Which side of the path the asstrob is on: 0 - center, 1 - left, 2 - right

    def __get_collision_data(self):
        import RPi.GPIO as GPIO
        import time
        
        GPIO.setmode(GPIO.BCM)
        
        safe_distance = 30
        #add pins

        #left sensor
        TRIGGER_1 = 18
        ECHO_1 = 24
        #mid sensor
        TRIGGER_2 = 18
        ECHO_2 = 24
        #right sensor
        TRIGGER_3 = 18
        ECHO_3 = 24
        
        GPIO.setup(TRIGGER_1, GPIO.OUT)
        GPIO.setup(ECHO_1, GPIO.IN)
        GPIO.setup(TRIGGER_2, GPIO.OUT)
        GPIO.setup(ECHO_2, GPIO.IN)
        GPIO.setup(TRIGGER_3, GPIO.OUT)
        GPIO.setup(ECHO_3, GPIO.IN)

        GPIO.output(TRIGGER_1, True)
        GPIO.output(TRIGGER_2, True)
        GPIO.output(TRIGGER_3, True)
        time.sleep(0.00001)
        GPIO.output(TRIGGER_1, False)
        GPIO.output(TRIGGER_2, False)
        GPIO.output(TRIGGER_3, False)

        while GPIO.input(ECHO_1)==0:
            start_1 = time.time();
        while GPIO.input(ECHO_2)==0:
            start_2 = time.time();
        while GPIO.input(ECHO_3)==0:
            start_3 = time.time();
        while GPIO.input(ECHO_1)==1:
            end_1 = time.time();
        while GPIO.input(ECHO_2)==1:
            end_2 = time.time();
        while GPIO.input(ECHO_3)==1:
            end_3 = time.time();

        duration_1 = end_1-start_1
        duration_2 = end_2-start_2
        duration_3 = end_3-start_3

        distance_1 = round(duration_1*17150,2)
        distance_2 = round(duration_2*17150,2)
        distance_3 = round(duration_3*17150,2)

        left_val = (distance_1<safe_distance)
        mid_val = (distance_2<safe_distance)
        right_val = (distance_3<safe_distance)

        return left_val,mid_val,right_val

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


