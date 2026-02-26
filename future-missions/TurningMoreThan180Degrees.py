# Launch 13 - Mission 10 - Tip The Scale
from hub import port, motion_sensor
import runloop
import motor_pair
import motor

NORMAL_SPEED = 150
ATTACHMENT_UP_POSITION = 120
TURN_SPEED = 150
FIRST_TURN_ANGLE = 65
SECOND_TURN_ANGLE = 115
FIRST_LEFT_TURN_ANGLE = -100
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

    # Bring attachment to up position
    # await motor.run_for_degrees(port.D, 20 , NORMAL_SPEED)

    # Move forward
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 460, 0, velocity=NORMAL_SPEED)


    await left_turn(motor_pair.PAIR_1, 90)

    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 500, 0, velocity=NORMAL_SPEED)

    await left_turn(motor_pair.PAIR_1, 170)

    motion_sensor.reset_yaw(0)
    await runloop.sleep_ms(500)

    await left_turn(motor_pair.PAIR_1, 10)

    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 100, 0, velocity=NORMAL_SPEED)

    await motor.run_for_degrees(port.D, 40 , NORMAL_SPEED)

    for i in range(3):
        await left_turn(motor_pair.PAIR_1, 20)
        await right_turn(motor_pair.PAIR_1, -10)





runloop.run(main())
