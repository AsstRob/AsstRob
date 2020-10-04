import RPi.GPIO as GPIO
import time
from asst_rob.core.directions import Directions
from asst_rob.core.navigation.base_navigator import BaseNavigator
from threading import Thread
from multiprocessing import Process

SENSOR_SETTLE_TIME = 0.00001
MAX_DISTANCE = 30.0
MEASURE_REFERENCE = 17150
MEASURE_INTERVAL_TIME = 0.1
#add pins

#left sensor
TRIG_1 = 17
ECHO_1 = 4
#mid sensor
TRIG_2 = 22
ECHO_2 = 5
#right sensor
TRIG_3 = 18
ECHO_3 = 23

class CollisionDetector(BaseNavigator):

    def __init__(self):
        super().__init__()
        self.__turn_label = Directions.NONE         # If a turn(s) is/are taken, which side: 0 - no turns, 1 - left(s), 2 - right(s)
        self.__turn_count = 0                       # How many turns taken to that side: 0 - no turns (a counter turn to the label side will decrease __turn_count by 1)
        self.__side = Directions.NONE               # Which side of the path the asstrob is on: 0 - center, 1 - left, 2 - right

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(ECHO_1,GPIO.IN )
        GPIO.setup(TRIG_1, GPIO.OUT )
        GPIO.setup(ECHO_2,GPIO.IN )
        GPIO.setup(TRIG_2, GPIO.OUT )
        GPIO.setup(ECHO_3,GPIO.IN )
        GPIO.setup(TRIG_3, GPIO.OUT )

    def __get_collision_data(self):
        while True:
            GPIO.output(TRIG_1, GPIO.LOW)
            time.sleep(MEASURE_INTERVAL_TIME); #DELAY
            GPIO.output(TRIG_1, GPIO.HIGH)
            time.sleep(SENSOR_SETTLE_TIME)
            GPIO.output(TRIG_1, GPIO.LOW)
            while GPIO.input(ECHO_1) == 0:
                start_1 = time.time()
            while GPIO.input(ECHO_1) == 1:
                end_1 = time.time()

            duration_1 = end_1 - start_1

            distance_1 = duration_1 * MEASURE_REFERENCE
            distanceRound_1 = round(distance_1, 2)

            print("Distance of sensor 1 :", distanceRound_1, "cm")

            GPIO.output(TRIG_2, GPIO.LOW)
            time.sleep(MEASURE_INTERVAL_TIME); #DELAY
            GPIO.output(TRIG_2, GPIO.HIGH)
            time.sleep(SENSOR_SETTLE_TIME)
            GPIO.output(TRIG_2, GPIO.LOW)
            while GPIO.input(ECHO_2) == 0:
                start_2 = time.time()
            while GPIO.input(ECHO_2) == 1:
                end_2 = time.time()

            duration_2 = end_2 - start_2

            distance_2 = duration_2 * MEASURE_REFERENCE
            distanceRound_2 = round(distance_2, 2)

            print("Distance of sensor 2 :", distanceRound_2, "cm")

            GPIO.output(TRIG_3, GPIO.LOW)
            time.sleep(MEASURE_INTERVAL_TIME); #DELAY
            GPIO.output(TRIG_3, GPIO.HIGH)
            time.sleep(SENSOR_SETTLE_TIME)
            GPIO.output(TRIG_3, GPIO.LOW)
            while GPIO.input(ECHO_3) == 0:
                start_3= time.time()
            while GPIO.input(ECHO_3) == 1:
                end_3 = time.time()

            duration_3 = end_3 - start_3

            distance_3 = duration_3 * MEASURE_REFERENCE
            distanceRound_3 = round(distance_3, 2)

            print("Distance of sensor 3 :", distanceRound_3, "cm")

            left_val = (distanceRound_1<MAX_DISTANCE)
            mid_val = (distanceRound_2<MAX_DISTANCE)
            right_val = (distanceRound_3<MAX_DISTANCE)
            
            print(left_val,mid_val,right_val)

            return left_val,mid_val,right_val


    def get_direction(self):
        """
        This is the entry point for pilot module to check for the next movement direction from collision detector.
        Will check for any collisions and fixes for making asstrob facing forward and send any signal to fix that.
        If all the 3 sensors are sending false signal, only then the returned signal will be reverse.
        Otherwise, if there are any collisions or fixes the signal will be left/right, or none if there are no collisions

        :return (Directions): If there are any fixes a Directions signal will be sent
        """
        left, mid, right = self.__get_collision_data()

        if not left and not mid and not right:
            """All sensors are blocked."""
            return Directions.REVERSE
        elif self.__turn_label == Directions.NONE:
            """No turns to be fixed. AsstRob going straight."""
            if mid:
                """Center sensor has no collisions. Won't have collisions."""
                return Directions.NONE
            else:
                if self.__side == Directions.NONE:
                    """In center of the path."""
                    if left:
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
                    if right:
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
                    if left:
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
            if right:
                """
                A right turn can be taken to fix a left.
                Takes a right.
                Decrement __turn_count by 1
                
                :return (Direction): RIGHT
                """
                self.__turn_count -= 1

                if self.__turn_count == 0:
                    """"If __turn_count is 0 then,
                    Set __turn_label to Directions.NONE (AsstRob is going straight)
                    """
                    self.__turn_label = Directions.NONE

                return Directions.RIGHT

            elif mid:
                """
                A right turn cannot be taken. If mid sensor detects no collisions, will not output any signal.
                
                :return (Direction): NONE
                """

                return Directions.NONE

            else:
                """"
                Only another left turn is possible. Will send a left signal.
                Increment __turn_count by 1
                
                :return (Direction): LEFT
                """
                self.__turn_count += 1
                return Directions.LEFT

        elif self.__turn_label == Directions.RIGHT:
            """AsstRob had turned to right needs to be fixed with left turn(s)."""
            if left:
                """
                A left turn can be taken to fix a right.
                Takes a left.
                Decrement __turn_count by 1

                :return (Direction): LEFT
                """
                self.__turn_count -= 1

                if self.__turn_count == 0:
                    """"
                    If __turn_count is 0 then,
                    Set __turn_label to Directions.NONE (AsstRob is going straight)
                    """
                    self.__turn_label = Directions.NONE

                return Directions.LEFT

            elif mid:
                """
                A left turn cannot be taken. If mid sensor detects no collisions, will not output any signal.

                :return (Direction): NONE
                """

                return Directions.NONE

            else:
                """"
                Only another right turn is possible. Will send a right signal.
                Increment __turn_count by 1

                :return (Direction): RIGHT
                """
                self.__turn_count += 1
                return Directions.RIGHT

        return Directions.NONE


