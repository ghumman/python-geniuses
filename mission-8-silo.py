from hub import port
import runloop
import motor_pair
import motor

async def main():

    await motor.run_to_absolute_position(port.D, 0, 90)

    await motor.run_for_degrees(port.A, -90, 180)
    motor_pair.pair(motor_pair.PAIR_1, port.A, port.E)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 250, 0, velocity=180)
    motor_pair.stop(motor_pair.PAIR_1)
    await motor.run_for_degrees(port.A, 100, 180)

    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 250, 0, velocity=180)
    motor_pair.stop(motor_pair.PAIR_1)
    for i in range(5):
        await motor.run_for_degrees(port.D, -100, 1000)
        await motor.run_for_degrees(port.D, 100, 1000)

    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -250, 0, velocity=180)
    motor_pair.stop(motor_pair.PAIR_1)

runloop.run(main())
