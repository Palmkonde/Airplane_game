"""
    Module that contains Airplane class 
    Factory Medthod
"""
from typing import List, Tuple, Union
import math


class BaseAirplane:
    """ Base Class for Airplane and Missiles """

    def __init__(self,
                 size: int,
                 center: Tuple[float, float],
                 speed: float) -> None:

        self._size = size
        self._center = center
        self._point = [
            # Top vertex
            (self._center[0], self._center[1] - self._size),

            # Bottom Left
            (self._center[0] - self._size,
             self._center[1] + self._size),

            # Bottom
            (self._center[0], self._center[1] + self._size*0.3),

            # Bottom Right
            (self._center[0] + self._size,
             self._center[1] + self._size)
        ]

        self._speed = speed
        self._is_alive = True

    def rotation_points(self, angle: int | float) -> None:
        """rotate points of airplnae from input angle 

        Args:
            angle (int | float): angle that wants Object to rotate in degrees
        Returns:
            None: This function is rotating an Object 
        """

        assert isinstance(angle, (float, int)), \
            f"angle should be float or int, but got {type(angle)}"

        cx, cy = self.get_center()
        all_points = self.get_points()

        theta_1 = math.radians(angle)
        new_points = []

        rotate_matrix = [
            [math.cos(theta_1), -math.sin(theta_1)],
            [math.sin(theta_1), math.cos(theta_1)]
        ]

        # Update all points
        for x, y in all_points:
            v_center_xy = [x - cx, y - cy]
            new_xy = []

            # Matrix multiplication
            for i in range(2):
                res = 0
                for j in range(2):
                    res += rotate_matrix[i][j] * v_center_xy[j]
                new_xy.append(res)

            new_xy[0] += cx
            new_xy[1] += cy
            new_points.append(tuple(new_xy))

        # Update latest point after rotate
        self._point = new_points

    def bouncing_box(self) -> Tuple[float, float, float, float]:
        """Get the (Axis-Aligned Bounding Box) for object

        Returns:
            Points (Tuple[float, float, float, float]): Bounding Box of an Object 
                                                        using for colliding detection
                                                        it contains min_x, max_x, min_y, max_y
                                                        respectively
        """

        points = self.get_points()

        min_x = min(map(lambda x: x[0], points))
        max_x = max(map(lambda x: x[0], points))
        min_y = min(map(lambda y: y[1], points))
        max_y = max(map(lambda y: y[1], points))

        return min_x, max_x, min_y, max_y

    def is_colliding(self, other: Union["Airplane", "Missile"]) -> bool:
        """check is colision 

        Args:
            other (Airplane | Missile): Other Object to check that it collide 
                                        with `this` object or not

        Returns:
            bool: return `True` when it is collide and `False` when it doesn't
        """
        min_x1, max_x1, min_y1, max_y1 = self.bouncing_box()
        min_x2, max_x2, min_y2, max_y2 = other.bouncing_box()

        if max_x1 < min_x2 or max_x2 < min_x1:
            return False
        if max_y1 < min_y2 or max_y2 < min_y1:
            return False

        return True

    # Acess data part
    def set_is_alive(self, state: bool) -> None:
        """set is alive of this object

        Args:
            state (bool): `True` or `False`

        Returns:
            None: nothing
        """
        self._is_alive = state

    def get_points(self) -> List[Tuple[float, float]]:
        """ Return point of object

        Returns:
            List[Tuple[float,float]]: list of points of this object
        """
        return self._point

    def get_vector(self) -> List[float]:
        """Return vector of obeject

        Calculate vector of object

        Returns:
            List[float]: Reuturn vector of object such that tail is at center 
                         and nose is at top of this object
        """
        cx, cy = self._center
        nose_x, nose_y = self._point[0]
        v_center_nose = [nose_x - cx, nose_y - cy]
        return v_center_nose

    def get_center(self) -> Tuple[float, float]:
        """Get center of an object

        Returns:
            Tuple(float, float): center of Object
        """
        return self._center

    def get_speed(self) -> float:
        """Get speed of an object

        Returns:
            float: speed of Object
        """
        return self._speed

    def get_alive(self) -> bool:
        """Check that Object is still alive or not

        Returns:
            bool: `True` when it still alive `False` when it doesn't
        """
        return self._is_alive


class Airplane(BaseAirplane):
    """ Class Airplane inherit from BaseAirplane use of main player character """

    def __init__(self,
                 size: int,
                 center: Tuple[float, float],
                 speed: float) -> None:
        super().__init__(size=size, center=center, speed=speed)

    def move_forward(self) -> None:
        """ Move this plane forward the top nose of it 

        Returns:
            None: Moving an object forward that nose it to
        """

        # Get nessary Data
        cx, cy = self.get_center()
        v_center_nose = self.get_vector()
        speed = self.get_speed()
        all_points = self.get_points()

        # List of new points
        new_points = []

        # Calculate what direction of this vector and update it
        angle = math.atan2(v_center_nose[1], v_center_nose[0])
        move_x = speed * math.cos(angle)
        move_y = speed * math.sin(angle)

        # Update all point of airplane
        self._center = (cx + move_x, cy + move_y)
        for x, y in all_points:
            new_x = x + move_x
            new_y = y + move_y

            new_points.append(tuple([new_x, new_y]))
        self._point = new_points


class Missile(BaseAirplane):
    """ Missile inherit from BaseAirplane use for object that has target to Airplane """

    def __init__(self,
                 size: int,
                 center: Tuple[float, float],
                 speed: float,
                 max_turn_rate: float,
                 acceleration: float = 0.01,
                 max_speed: float = 0.3) -> None:

        super().__init__(size=size, center=center, speed=speed)
        self.__acceleration = acceleration
        self.__max_speed = max_speed
        self.__max_turn_rate = max_turn_rate

    def update(self, dt: float) -> None:
        """Update point with acceleration and delta time

        Update all points and speed with acceleration 
        and limit speed by max_speed

        Args:
            dt (float): delatime from pygame

        Returns:
            None: Update all Point
        """

        v_missile = self.get_vector()
        acceleration = self.get_acceleration()
        current_speed = self.get_speed()
        max_speed = self.get_max_speed()
        center = self.get_center()
        all_points = self.get_points()
        new_points = []

        if current_speed == max_speed:
            self._is_alive = False

        missile_angle = math.atan2(v_missile[1], v_missile[0])

        # Calculate new speed + accelerate
        self._speed += acceleration * dt

        new_speed = self.get_speed()
        self._speed = min(new_speed, max_speed)

        # find delta_x, delta_y
        move_x = new_speed * math.cos(missile_angle)
        move_y = new_speed * math.sin(missile_angle)

        # Update all point
        self._center = (center[0] + move_x, center[1] + move_y)
        for x, y in all_points:
            new_x = x + move_x
            new_y = y + move_y
            new_points.append(tuple([new_x, new_y]))

        self._point = new_points

    def rotation_to_target(self, target: Airplane) -> None:
        """Rotate face to target

        Args:
            target (Airplane): Object that wants missile to rotate to

        Returns:
            None: Just rotating all points
        """

        v_missile = self.get_vector()
        center_missile = self.get_center()
        center_target = target.get_center()
        max_turn_rate = math.radians(self.get_max_turn_rate())

        # convert to vector
        v_m1_t = [center_target[0] - center_missile[0],
                  center_target[1] - center_missile[1]]

        missile_angle = math.atan2(v_missile[1], v_missile[0])
        target_angle = math.atan2(v_m1_t[1], v_m1_t[0])

        diff_angle = target_angle - missile_angle

        if diff_angle > math.pi:
            diff_angle -= 2 * math.pi
        elif diff_angle < -math.pi:
            diff_angle += 2 * math.pi

        if abs(diff_angle) > max_turn_rate:
            diff_angle = max_turn_rate if diff_angle > 0 else -max_turn_rate

        self.rotation_points(math.degrees(diff_angle))

    # Acess data
    def get_acceleration(self) -> float:
        """Get acceleration of this object

        Returns:
            float: acceleration of this object
        """
        return self.__acceleration

    def get_max_speed(self) -> float:
        """Get max speed of this object

        Returns:
            float: max_speed of this object
        """
        return self.__max_speed

    def get_max_turn_rate(self) -> float:
        """Get max_turn_rate

        Returns:
            float: max_turn_rate of this object
        """
        return self.__max_turn_rate
