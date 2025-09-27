import motor
from hub import port

# Run two motors on ports A and B for 360 degrees at 720 degrees per second.
# The motors run at the same time.
motor.run_for_degrees(port.A, 360, 720)
motor.run_for_degrees(port.E, -360, 720)