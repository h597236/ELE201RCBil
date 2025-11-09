# STM32 RC Car  

## Table of Contents
- [System Overview](#system-overview)
- [Communication](#communication)
- [Motor and Servo Control](#motor-and-servo-control)
- [Python Controller Interface](#python-controller-interface)
- [Testing and Results](#testing-and-results)
- [Demo Video](#demo-video)

---

## System Overview

### Objective
Develop a **remote-controlled car** using a **PS4 controller**, a **Python interface**, and an **STM32F767** microcontroller.  
The PS4 controller connects to a PC via Bluetooth, and the PC sends UART commands through an **HC-05** Bluetooth module to the STM32.  
The STM32 then controls two DC motors and one servo using an **L293D H-bridge**.

### Features
- Wireless control using a PS4 controller  
- UART Bluetooth communication between PC and STM32  
- PWM-based speed and steering control  
- 3D-printed chassis  

### System Diagram
```
PS4 Controller → PC (Python) → HC-05 Bluetooth → STM32F767 → L293D + Servo → Motors
```

---

## Communication

### Description
The system uses **UART communication** to transfer commands from the PC to the STM32 through the **HC-05 Bluetooth module**.  
Each command follows this format:

```
M <leftSpeed> <rightSpeed> S <servoAngle>
```

### UART Configuration
| Parameter | Value |
|------------|--------|
| Baud Rate | 9600 bps |
| Data Bits | 8 |
| Stop Bits | 1 |
| Parity | None |

### Pin Configuration
| Signal | MCU Pin | Function |
|---------|----------|-----------|
| UART_TX | PD8 | USART3_TX |
| UART_RX | PD9 | USART3_RX |
| Bluetooth VCC | 5V | Power |
| Bluetooth GND | GND | Ground |

---

## Motor and Servo Control

### Description
Two **DC motors** provide forward and reverse drive, controlled through an **L293D H-bridge**.  
A **Micro Servo (FS90)** handles front-wheel steering via a PWM output from the STM32.

### Pin Configuration
| Component | MCU Pin | Function |
|------------|----------|-----------|
| Left Motor | PB0, PB1 | Direction + PWM |
| Right Motor | PB4, PB5 | Direction + PWM |
| Servo | PA6 | TIM3_CH1 (PWM Output) |

### Circuit Diagram
```
                STM32F767
             ┌───────────────────┐
  HC-05_TX ─┤ PD9 (USART3_RX)    │
  HC-05_RX ─┤ PD8 (USART3_TX)    │
  L293D_IN1 ─┤ PB0                │
  L293D_IN2 ─┤ PB1                │
  L293D_IN3 ─┤ PB4                │
  L293D_IN4 ─┤ PB5                │
  SERVO ─────┤ PA6 (PWM)          │
             └───────────────────┘
```

---

## Python Controller Interface

### Description
The **PS4 controller** is connected to the PC via Bluetooth and read using the `pygame` library.  
Joystick and button values are converted into UART commands that are sent to the STM32.

### Example Command Output
```
Left joystick: -0.4 | Right joystick: 0.6 | Servo: 85°
→ Sent: M -40 60 S 85
```

### Command Flow
1. Read PS4 controller input  
2. Translate input to motor speeds and servo angle  
3. Send formatted UART command to STM32  
4. STM32 updates motor PWM and servo position  

---

## Testing and Results

### Procedure
- Verified UART commands with **Serial Bluetooth Terminal (Android)**  
- Tested Python controller communication  
- Mounted components on a 3D-printed car body  

### Observations
- Stable Bluetooth connection  
- Responsive motor and servo control  
- Servo required tuning after repeated use  
- Needed to adjust jumper to use VIN pin for power  

### Outcome
System operated successfully — the car could be driven wirelessly using a PS4 controller.

---

## Demo Video
[![RC Car Demo](https://img.youtube.com/vi/dQw4w9WgXcQ/0.jpg)](https://github.com/h597236/ELE201RCBil)

---

### Repository
Full source code and documentation available at:  
👉 [https://github.com/h597236/ELE201RCBil](https://github.com/h597236/ELE201RCBil)
