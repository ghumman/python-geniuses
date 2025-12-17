# Launch 0 - Mission 8 - Silo
from hub import port
import runloop
import motor_pair
import motor

NORMAL_SPEED = 90
FAST_SPEED = 720
START_ATTACHMENT_POSITION = 170
LOWER_ATTACHMENT_POSITION = 30

async def main():

    # Bring attachment to starting position
    await motor.run_for_degrees(port.D, START_ATTACHMENT_POSITION, NORMAL_SPEED)

    # Make a right turn
    await motor.run_for_degrees(port.A, -90, 180)

    # Pair motors
    motor_pair.pair(motor_pair.PAIR_1, port.A, port.E)

    # Move forward
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 430, 0, velocity=180)
    motor_pair.stop(motor_pair.PAIR_1)

    # Make a left turn
    await motor.run_for_degrees(port.A, 95, 180)

    # Move forward
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 80, 0, velocity=180)
    motor_pair.stop(motor_pair.PAIR_1)

    # Move the attachment
    for i in range(5):
        await motor.run_for_degrees(port.D, LOWER_ATTACHMENT_POSITION - START_ATTACHMENT_POSITION, FAST_SPEED)
        await motor.run_for_degrees(port.D, START_ATTACHMENT_POSITION - LOWER_ATTACHMENT_POSITION, FAST_SPEED)

    # Move backward
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -250, 0, velocity=NORMAL_SPEED)
    motor_pair.stop(motor_pair.PAIR_1)

runloop.run(main())