# Drone P17 Pro WiFi Controller
This Python script allows you to remote control some drone models (like the P17 Pro) via computer keyboard.


### overview
seems that instead of other drones using 8 byte messages it uses 20 byte messages
his UDP port seems to be 3456 looking into the Wireshark capture

a working example of connection to the drone
```Python
import socket
import time

# Define the message to be sent
#msg = bytearray([0x66, 0x80, 0x80, 0x80, 0x80, 0x01, 0x00, 0x99, 0x0])
#msg = bytes.fromhex('CC 80 80 80 80 00 00 33')
msg = bytearray([0x66, 0x14, 0x00, 0x00, 0x80, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x99])
# Define the destination IP address and port
ip = "192.168.80.1"
port = 3456

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Send the message 100 times
count = 100
while count > 0:
    # Calculate the checksum
    #msg[6] = msg[1] ^ msg[2] ^ msg[3] ^ msg[4] ^ msg[5]

    # Send the message
    sock.sendto(msg, (ip, port))
    print("send.")

    # Decrement the count
    count -= 1

    # Wait for a short time
    time.sleep(0.05)

# Close the socket
sock.close()
```

### Web Resources

 - https://github.com/LukasMaly/wifi-ufo-drone/tree/master
 - https://particolarmente-urgentissimo.blogspot.com/2021/01/sniffaggio-traffico-wifi-drone-1-parte.html?lr=1736665890668
 - https://blog.horner.tj/hacking-chinese-drones-for-fun-and-no-profit/
     - https://github.com/martin-ger/ESP_E58-Drone/blob/main/E58.ino
     - https://github.com/tjhorner/dronelib/tree/master
     - https://web.archive.org/web/20201025060757/https://mehmetburakeker.com/2017/05/01/opencv-ile-nesne-takip-eden-drone-projesi-cx-32w/



###  misc
- network traffic sniffer (ios)
    - https://github.com/gh2o/rvi_capture
- wireshark
    - https://www.iprogrammable.com/2017/11/10/how-to-use-wireshark-to-get-ip-camera-rtsp-url/

    ```((!(_ws.col.protocol == "UDP") && !(_ws.col.protocol == "IPv4")) && (ip.src == 192.168.80.2)) && !(_ws.col.info contains "ACK")```
- chip
    - https://github.com/christian-kramer/JieLi-AC690X-Familiarization
    - https://doc.zh-jieli.com/Apps/iOS/video/zh-cn/master/Development/DeveloperDocument.html
    - https://doc.zh-jieli.com/Apps/iOS/video/zh-cn/master/Development/DeveloperDocument.html#id6
    - https://doc.zh-jieli.com/AC79/zh-cn/master/index.html
    - https://github.com/cxy19880915/buxinyun/tree/6a9c06a3b95de9764339abfaad6084d8c927b432/AC54XX_WIFI_SDK_V0.5.13_2_%E5%8F%8C%E5%BD%95_%E8%B0%B1%E7%A8%8B
- CTP
    - https://www.paperpublications.org/upload/book/Command%20Transfer%20Protocol-733.pdf

    


















## Requirements
 - pygame
 - scapy

## Constants
 - Constants can be edited in [dronecontrol.py](https://github.com/LukasMaly/wifi-ufo-drone/blob/master/wifi_ufo_drone/dronecontrol.py "LukasMaly/dronecontrol.py").
 - Source IP: `192.168.0.2`
 - Network Interface: `en0`
 - Destination IP: `192.168.0.1`
 - TCP Port: `7060`
 - UDP Port: `40000`

## Keyboard Controls
| Key | Control |
| --- | --- |
| Esc | Exit Control |
| Spacebar | Vertical Takeoff/Land |
| Tab | Cycle Speeds |
| W/A/S/D | Pitch Forward/Left/Down/Right |
| ↑ | Throttle Up |
| ↓ | Throttle Down |
| → | Yaw Right |
| ← | Yaw Left |

## License
 - MIT License
