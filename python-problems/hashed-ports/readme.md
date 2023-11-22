## Hashed Ports

Packets are sent to different ports on a computer system based on the hash of their packet ID. The value of the hash is as given below: 
```
Hash mod(packet_id, numberOfPorts)
```
where `mod` is the modulus operator and takes the mod of first operand by second operand.

The ports are numbered from 0 to (_number of ports_)-1, and a packet is initially sent to the port that has the port number equal to the hash of its packet ID. Each port requires a time _t_ to send a packet. If a port is currently sending a packet, this packet is then sent to the next port number, and so on. Given that _x_ packets arrive 1 per second, and given the IDs of the packets, find the port at which each packet is finally sent. First packet is sent at time _t=1_.

#### Function Description

Complete the `sentTimes` function. The function must return an integer array denoting the ports at which the packets are sent.

`sentTimes` has the following parameter(s):
- `numberOfPorts`: An integer, the number of ports in the system.
- `transmissionTime`: An integer, the time for a port to send a packet.
- `packetIds`: An integer array, where `packetIds`; describes the IDs of the packets in the order in which they arrive.

#### Constraints

- 1 $\leq$ `numberOfPorts` $\leq$ 2000
- 1 $\leq$ `transmissionTime` $\leq$ 100
- 1 $\leq$ `x` $\leq$ 2000
- 1 $\leq$ `packetIds` $\leq$ 10<sup>5</sup>