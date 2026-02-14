from hub import port
import runloop
import motor_pair
import motor

# ======================
# CONSTANTS
# ======================
DRIVE_SPEED = 180
TURN_SPEED = 180
NORMAL_SPEED = 90
FAST_SPEED = 720

ATTACH_START = 230
SILO_DROP = 80
WHO_LIVED_HERE_PUSH = 120

# ======================
# SETUP
# ======================
motor_pair.pair(motor_pair.PAIR_1, port.A, port.E)

# ======================
# FUNCTIONS
# ======================
async def reset_attachment():
    await motor.run_to_absolute_position(
        port.D, ATTACH_START, NORMAL_SPEED
    )

async def drive(deg):
    await motor_pair.move_for_degrees(
        motor_pair.PAIR_1, deg, 0, velocity=DRIVE_SPEED
    )
    motor_pair.stop(motor_pair.PAIR_1)

async def turn(deg):
    await motor.run_for_degrees(port.A, deg, TURN_SPEED)

async def silo_mission():
    # Turn toward silo
    await turn(-90)

    # Drive to silo
    await drive(410)

    # Align
    await turn(100)
    await drive(80)

    # Operate silo (5 times)
    for _ in range(5):
        await motor.run_to_absolute_position(
            port.D, ATTACH_START - SILO_DROP, FAST_SPEED
        )
        await reset_attachment()

    # Back away
    await drive(-250)

async def who_lived_here_mission():
    # Turn toward Who Lived Here
    await turn(90)

    # Drive to model
    await drive(300)

    # Activate model
    await motor.run_to_absolute_position(
        port.D, WHO_LIVED_HERE_PUSH, FAST_SPEED
    )

    await runloop.sleep_ms(300)

    # Reset attachment
    await reset_attachment()

    # Back away
    await drive(-150)

# ======================
# MAIN RUN
# ======================
async def main():
    await reset_attachment()
    await silo_mission()
    await who_lived_here_mission()

runloop.run(main())
