import logging
import random
import threading
import time

from scapy.all import *  # Import all scapy modules
from scapy.layers.inet import IP,TCP,UDP  # Import IP class specifically


UDP_HEARTBEAT_DATA = bytearray([0x63, 0x63, 0x01, 0x00, 0x00, 0x00, 0x00])



FLY_DRONE_DATA = bytearray([0x66, 0x14, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x99])

class DroneControl(object):
    """Base drone control class which handles connecting to the drone
    and sending commands for controlling the drone.
    """

    def __init__(self):
        self._src = '192.168.80.3'
        self._dst = '192.168.80.1'
        #self._iface = 'Realtek RTL8188EU Wireless LAN 802.11n USB 2.0 Network Adapter'
        self._tcp_dport = 3333 # 8080 # 3333 # 8080 # 3333 # 8080
        self._udp_dport = 3456 # 50000 # 3456 # 3456 # 3333
        self._udp_sport = random.randint(32768, 49152)

    def tcp_heartbeat_worker(self):
        """TCP hearbeat"""
        while True:
            time.sleep(0.05)
            sport = random.randint(32768, 49152)
            SYN = TCP(sport=sport, dport=self._tcp_dport, flags='S', seq=0)
            SYNACK = sr1(IP(src=self._src, dst=self._dst, ttl=63)/SYN, 
                         #iface=self._iface, 
                         verbose=0)

    def udp_heartbeat_worker(self):
        """UDP heartbeat"""
        sport = random.randint(32768, 49152)

        # Create the packet template
        packet = (
            IP(dst=self._dst) /
            UDP(dport=self._udp_dport) /
            Raw(FLY_DRONE_DATA)
        )

        #packet = IP(src=self._src, dst=self._dst, id=random.randint(0, 65535), ttl=63) / UDP(sport=sport, dport=self._udp_dport) / raw(UDP_HEARTBEAT_DATA)
        #print(packet)
        #print(packet.show())
        #print(raw(UDP_HEARTBEAT_DATA))
        while True:
            time.sleep(1)
            send(packet,
                 #iface=self._iface,
                    verbose=0)

    def connect(self):
        """Initiates connection on the TCP and UDP ports. This must be run
        before attempting to send control commands to the quadcopter.
        """
        workers = [self.tcp_heartbeat_worker, self.udp_heartbeat_worker]
        for worker in workers:
            t = threading.Thread(target=worker)
            t.start()

    def checksum(self, data):
        """The flight data has to be passed through a checksum.

        Returns:
            the 8 bit xor checksum of the data
        """
        #print(data)
        return_data = (data[0] ^ data[1] ^ data[2] ^ data[3])
        #print(return_data)
        return return_data

    def cmd(self, r=0, p=0, t=0, y=0, m=0):
        """Send the flight command controls.

        Args:
            r (int): 0-255 for the roll of the drone, 128 is the middle (Left/right)
            p (int): 0-255 for the pitch of the drone, 128 is the middle (Forward/backward)
            t (int): 0-255 for the throttle of the drone, 0 is no throttle (Elevation) 
            y (int): 0-255 for the yaw of the drone, 128 is middle (Turning)
            m (int): 0: do nothing, 1: take off, 2: land, 4: stop


            1st byte – Header: 66
            2nd byte – Header: 14
            
            
            R 3rd byte – 00 ⬅⮕ (Left/right)
            P 4th byte – 00 ⬆⬇ (Forward/backward)
            T 5th byte – 80 𖣫 (Elevation)
            Y 6th byte – 80  ↺↻ (Turn)
        """
        droneCmd = FLY_DRONE_DATA[:]
        droneCmd[3] = r
        droneCmd[4] = p
        droneCmd[5] = t
        droneCmd[6] = y
        #droneCmd[7] = m

        droneCmd[19] = self.checksum(droneCmd[2:7])
        #print("droneCmd",droneCmd.hex())
        #packet = IP(src=self._src, dst=self._dst, id=random.randint(0, 65535), ttl=63) / UDP(sport=self._udp_sport, dport=self._udp_dport) / raw(droneCmd)
        
        packet = (
            IP(dst=self._dst) /
            UDP(dport=self._udp_dport) /
            Raw(droneCmd)
        )
        send(packet, 
             #iface=self._iface, 
             verbose=0)

    def take_off(self):
        """Send the takeoff command for the drone.
        """
        logging.info("Taking off...")
        begin_time = time.time()
        while time.time() - begin_time < 1:
            self.cmd(t=255,y=255)
        logging.info("Took off")

    def land(self):
        """Send the land command for the drone.
        """
        logging.info("Landing...")
        begin_time = time.time()
        while time.time() - begin_time < 1:
            self.cmd(m=2)
        logging.info("Landed")

    def stop(self):
        """Send the hard stop for the drone. If it is flying and this is called,
        it will fall down.
        """
        logging.info("Stopping...")
        begin_time = time.time()
        while time.time() - begin_time < 1:
            self.cmd(m=4)
        logging.info("Stopped")


if __name__ == "__main__":
    drone = DroneControl()
    drone.connect()
    #drone.udp_heartbeat_worker()
    time.sleep(3)

    drone.take_off()

    for i in range(20):
        drone.cmd()

    #drone.land()