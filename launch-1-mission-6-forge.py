# Launch 1 - Mission 6 - Forge
from hub import port
import runloop
import motor_pair
import motor

NORMAL_SPEED = 180
FAST_SPEED = 720

START_ATTACHMENT_POSITION = 10

async def main():

    # Bring attachment to starting position
    await motor.run_for_degrees(port.D, START_ATTACHMENT_POSITION, NORMAL_SPEED)

    # Move left
    await motor.run_for_degrees(port.E, 200, NORMAL_SPEED)

    # Move right
    await motor.run_for_degrees(port.A, -220, NORMAL_SPEED)


    # Pair motors
    motor_pair.pair(motor_pair.PAIR_1, port.A, port.E)

    # # Move forward
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 680, 0, velocity=NORMAL_SPEED)


    # Make a right turn
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 130, 100, velocity=FAST_SPEED)

    # Make left turn
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 100, -100, velocity=FAST_SPEED)

    # Return
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -800, 0, velocity=NORMAL_SPEED)
    motor_pair.stop(motor_pair.PAIR_1)

runloop.run(main())