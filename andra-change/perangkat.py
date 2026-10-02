from pybricks.hubs import InventorHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Port, Direction
from pybricks.robotics import DriveBase

hub = InventorHub()

left = Motor(Port.B, Direction.CLOCKWISE)
right = Motor(Port.A, Direction.CLOCKWISE)

line_sensor = ColorSensor(Port.C)
sensor = line_sensor

wall_sensor = ColorSensor(Port.E)
eyes = UltrasonicSensor(Port.F)

WHEEL_DIAMETER = 56
AXLE_TRACK = 114

robot = DriveBase(left, right, wheel_diameter=WHEEL_DIAMETER, axle_track=AXLE_TRACK)

robot.settings(
    straight_speed=120,
    straight_acceleration=300,
    turn_rate=100,
    turn_acceleration=200
)