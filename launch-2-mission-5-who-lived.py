# Launch 2 - Mission 5 - Who Lived Here
from hub import port
import runloop
import motor_pair
import motor

NORMAL_SPEED = 180
FAST_SPEED = 720

START_ATTACHMENT_POSITION = 60

async def main():

    # Bring attachment to starting position
    await motor.run_for_degrees(port.D, START_ATTACHMENT_POSITION, NORMAL_SPEED)

    # Pair motors
    motor_pair.pair(motor_pair.PAIR_1, port.A, port.E)

    # Move forward
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 870, 0, velocity=NORMAL_SPEED)

    # Move attachment to left
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 100, -80, velocity=FAST_SPEED)

    # Add delay before going more left to add more force and settle things down
    await runloop.sleep_ms(500)

    # Move attachment to left
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 100, -80, velocity=NORMAL_SPEED)

    # Return
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -800, 0, velocity=NORMAL_SPEED)

    # Stop motor pair
    motor_pair.stop(motor_pair.PAIR_1)

runloop.run(main())