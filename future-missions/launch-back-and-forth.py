# Launch 1 to launch 2 - back and forth
from hub import port, motion_sensor
import runloop
import motor_pair
import motor

NORMAL_SPEED = 720
ATTACHMENT_UP_POSITION = 120
TURN_SPEED = 720
FIRST_TURN_ANGLE = 45
SECOND_TURN_ANGLE = 85
FIRST_LEFT_TURN_ANGLE = 45
SECOND_LEFT_TURN_ANGLE = 100


async def left_turn(pair, degrees, speed=TURN_SPEED):
    """
    Turn robot left using gyro (yaw) for a specified degrees
    """
    target_yaw = degrees * 10# convert degrees to decidegrees
    motor_pair.move(pair, -100, velocity=speed)

    while True:
        yaw, pitch, roll = motion_sensor.tilt_angles()
        print("Yaw (decidegrees):", yaw)
        if yaw >= target_yaw:
            break
        await runloop.sleep_ms(10)

    motor_pair.stop(pair)

async def right_turn(pair, degrees, speed=TURN_SPEED):
    """
    Turn robot right using gyro (yaw) for a specified degrees
    """
    target_yaw = -degrees * 10# negative for right turn (decidegrees)
    motor_pair.move(pair, 100, velocity=speed)# opposite direction of left turn

    while True:
        yaw, pitch, roll = motion_sensor.tilt_angles()
        print("Yaw (decidegrees):", yaw)
        if yaw <= target_yaw:
            break
        await runloop.sleep_ms(10)

    motor_pair.stop(pair)



async def main():
    # Reset yaw at the very start of mission
    motion_sensor.set_yaw_face(motion_sensor.TOP)
    motion_sensor.reset_yaw(0)

    # Pair motors
    motor_pair.pair(motor_pair.PAIR_1, port.A, port.E)

    # Move forward
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 200, 0, velocity=NORMAL_SPEED)
    motor_pair.stop(motor_pair.PAIR_1)

    # Make first right turn using yaw
    await right_turn(motor_pair.PAIR_1, FIRST_TURN_ANGLE)

    # Move forward
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 500, 0, velocity=NORMAL_SPEED)
    motor_pair.stop(motor_pair.PAIR_1)

    # Make first right turn using yaw
    await right_turn(motor_pair.PAIR_1, SECOND_TURN_ANGLE)

    # Move forward
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 1300, 0, velocity=NORMAL_SPEED)
    motor_pair.stop(motor_pair.PAIR_1)

    # Make first left turn using yaw
    await left_turn(motor_pair.PAIR_1, FIRST_LEFT_TURN_ANGLE)

    # Move forward
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 1300, 0, velocity=NORMAL_SPEED)
    motor_pair.stop(motor_pair.PAIR_1)

    # Make second left turn using yaw
    await left_turn(motor_pair.PAIR_1, SECOND_LEFT_TURN_ANGLE)

    # Move forward
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 600, 0, velocity=NORMAL_SPEED)
    motor_pair.stop(motor_pair.PAIR_1)


runloop.run(main())
