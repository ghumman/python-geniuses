# Mission 7 - Heavy Lifting
from hub import port
import runloop
import motor_pair
import motor

NORMAL_SPEED = 180
ATTACHMENT_UP_POSITION = 170
ATTACHMENT_DOWN_POSITION = -120


async def main():

    # Bring attachment to up position
    await motor.run_for_degrees(port.D, ATTACHMENT_UP_POSITION, NORMAL_SPEED)

    # Make a right turn
    await motor.run_for_degrees(port.A, -170, NORMAL_SPEED)

    # Pair motors
    motor_pair.pair(motor_pair.PAIR_1, port.A, port.E)

    # Move forward
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 640, 0, velocity=NORMAL_SPEED)
    motor_pair.stop(motor_pair.PAIR_1)

    # Make a left turn
    await motor.run_for_degrees(port.A, 130, NORMAL_SPEED)

    # Move forward
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 380, 0, velocity=180)
    motor_pair.stop(motor_pair.PAIR_1)

    # Make a left turn
    await motor.run_for_degrees(port.A, 65, NORMAL_SPEED)

    # Move forward
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 260, 0, velocity=180)
    motor_pair.stop(motor_pair.PAIR_1)

    # Bring attachment to down position
    await motor.run_for_degrees(port.D, ATTACHMENT_DOWN_POSITION, NORMAL_SPEED)

    # Make left turn with 2 motors
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 40, -100, velocity=NORMAL_SPEED)

    # Bring attachment to up position
    await motor.run_for_degrees(port.D, ATTACHMENT_UP_POSITION, NORMAL_SPEED)

    # Make right turn with 2 motors
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 60, 100, velocity=NORMAL_SPEED)

runloop.run(main())