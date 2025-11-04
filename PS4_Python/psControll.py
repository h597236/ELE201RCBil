
# PS4 → Bluetooth (HC-05) → STM32
# R2 = gass (fram), L2 = rygg, venstre stikke X = ratt

import time
import math
import sys

import pygame
import serial
import serial.tools.list_ports

PORT = "COM10"      
BAUD = 9600

SEND_HZ = 20       

MAX_SPEED = 100     
MAX_STEER = 60      

DZ_STEER = 0.06     
EXPO_STEER = 0.25

#
SLEW_SPEED_UP   = 180.0
SLEW_SPEED_DOWN = 250.0
SLEW_STEER      = 600.0

SLOW_MODE_FACTOR = 0.50


BTN_PANIC = 0  
BTN_SLOW  = 1  #


def trig01(v):
    if v < -0.001 or v > 1.001:
        
        return (v + 1.0) * 0.5

    return max(0.0, min(1.0, v))

def apply_deadzone(v, dz):
    return 0.0 if abs(v) < dz else (v - math.copysign(dz, v)) / (1.0 - dz)

def apply_expo(v, expo):
    return (1.0 - expo) * v + expo * (v ** 3)

def map_stick_to_steer(stick_x):
    v = apply_deadzone(stick_x, DZ_STEER)
    v = apply_expo(v, EXPO_STEER)
    return int(round(v * MAX_STEER))

def slew_towards(current, target, max_delta):
    return min(current + max_delta, target) if target > current else max(current - max_delta, target)


print("Koplar til", PORT, "@", BAUD)
ser = serial.Serial(PORT, BAUD, timeout=0, write_timeout=1)
pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("Fant ingen kontroller. Kople til PS4-kontroller og prøv igjen.")
    sys.exit(1)

js = pygame.joystick.Joystick(0)
js.init()
print("Kontroller:", js.get_name())
print("Klar. R2 = gass, L2 = rygg. X = panikk, O = slow mode (held inne).")


cur_speed = 0.0
cur_steer = 0.0
slow_mode = False
dt = 1.0 / SEND_HZ


def get_axis_first_of(cands, default=0.0):
    for ax in cands:
        try:
            v = js.get_axis(ax)
            if abs(v) <= 1.0 or (0.0 <= v <= 1.0):
                return v
        except Exception:
            pass
    return default

try:
    while True:
        t0 = time.time()
        pygame.event.pump()

    
        raw_l2 = get_axis_first_of([4, 3])
        raw_r2 = get_axis_first_of([5, 4])

        l2 = trig01(raw_l2)   
        r2 = trig01(raw_r2)   

      
        th = r2 - l2
        target_speed = int(round(th * MAX_SPEED))

        
        lx = get_axis_first_of([0, 2, 3])
        target_steer = map_stick_to_steer(lx)

        
        slow_mode = bool(js.get_button(BTN_SLOW))

    
        if js.get_button(BTN_PANIC):
            target_speed = 0
            target_steer = 0
            slow_mode = True

        if slow_mode:
            target_speed = int(round(target_speed * SLOW_MODE_FACTOR))

    
        max_delta_speed = (SLEW_SPEED_UP if target_speed > cur_speed else SLEW_SPEED_DOWN) * dt
        max_delta_steer = SLEW_STEER * dt

        cur_speed = slew_towards(cur_speed, target_speed, max_delta_speed)
        cur_steer = slew_towards(cur_steer, target_steer, max_delta_steer)

        out_speed = int(round(cur_speed))
        out_steer = int(round(cur_steer))

        cmd = f"M {out_speed} {out_speed} S {out_steer}\n"
        ser.write(cmd.encode())

        
        rest = dt - (time.time() - t0)
        if rest > 0:
            time.sleep(rest)

except KeyboardInterrupt:
    pass
finally:
    try:
        ser.write(b"M 0 0 S 0\n")
        ser.close()
    except Exception:
        pass
    pygame.quit()
    print("\nAvslutta. Motor stoppa og servo midt.")
