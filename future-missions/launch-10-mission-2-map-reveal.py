# Mission 3 - Mineshift with Yaw-Based Left Turns
from hub import port, motion_sensor
import runloop
import motor_pair
import motor

NORMAL_SPEED = 180
ATTACHMENT_UP_POSITION = 170
TURN_SPEED = 80
FIRST_TURN_ANGLE = 50
SECOND_TURN_ANGLE = -20
THIRD_TURN_ANGLE = 120
FOURTH_TURN_ANGLE = 170



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
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 850, 0, velocity=NORMAL_SPEED)
    motor_pair.stop(motor_pair.PAIR_1)

    # Make first left turn using yaw
    await left_turn(motor_pair.PAIR_1, FIRST_TURN_ANGLE)

    # Move forward
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 220, 0, velocity=NORMAL_SPEED)
    motor_pair.stop(motor_pair.PAIR_1)

    # Move backward
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -70, 0, velocity=NORMAL_SPEED)
    motor_pair.stop(motor_pair.PAIR_1)

    # Bring attachment to mid position
    await motor.run_for_degrees(port.D, ATTACHMENT_UP_POSITION - 110, NORMAL_SPEED)

    # Make right turn using yaw
    await right_turn(motor_pair.PAIR_1, SECOND_TURN_ANGLE)



    # Move forward
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 20, 0, velocity=NORMAL_SPEED)

    # Bring attachment to up position
    await motor.run_for_degrees(port.D, ATTACHMENT_UP_POSITION, NORMAL_SPEED)

    # Make right turn using yaw
    await right_turn(motor_pair.PAIR_1, THIRD_TURN_ANGLE)

    # Move forward
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 300, 0, velocity=NORMAL_SPEED)

    # Bring attachment to down position
    await motor.run_for_degrees(port.D, -170, NORMAL_SPEED)    
    await motor.run_for_degrees(port.D, -50, NORMAL_SPEED)



runloop.run(main())
