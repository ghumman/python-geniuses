from hub import port, motion_sensor
import runloop
import motor_pair
import motor

NORMAL_SPEED = 150
TURN_SPEED = 150
ATTACHMENT_UP_POSITION = 120
ATTACHMENT_DOWN_TARGET = 0


async def turn_and_lower(pair, turn_degrees):

    motion_sensor.reset_yaw(0)
    target_yaw = turn_degrees * 10# decidegrees

    # Start lowering attachment (reverse direction)
    motor.run(port.D, -NORMAL_SPEED)

    # Start turning left
    motor_pair.move(pair, -100, velocity=TURN_SPEED)

    while True:
        yaw, pitch, roll = motion_sensor.tilt_angles()
        current_position = motor.relative_position(port.D)

        turn_done = yaw >= target_yaw
        attachment_done = current_position <= ATTACHMENT_DOWN_TARGET

        if turn_done:
            motor_pair.stop(pair)

        if attachment_done:
            motor.stop(port.D)

        if turn_done and attachment_done:
            break

        await runloop.sleep_ms(10)

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



async def main():

    motion_sensor.set_yaw_face(motion_sensor.TOP)
    motion_sensor.reset_yaw(0)

    motor_pair.pair(motor_pair.PAIR_1, port.A, port.E)

    # Move forward
    await motor_pair.move_for_degrees(
        motor_pair.PAIR_1,
        200,
        0,
        velocity=NORMAL_SPEED
    )

    # Bring attachment UP first
    await motor.run_for_degrees(
        port.D,
        ATTACHMENT_UP_POSITION,
        NORMAL_SPEED
    )

    await left_turn(motor_pair.PAIR_1, 20)


    # Move forward again
    await motor_pair.move_for_degrees(
        motor_pair.PAIR_1,
        230,
        0,
        velocity=NORMAL_SPEED
    )

    # 🚀 Turn AND lower together
    await turn_and_lower(motor_pair.PAIR_1, 35)


runloop.run(main())
