# transmissionTime must be less than numberOfPorts
def sentTimes(numberOfPorts, transmissionTime, packetIds):
    out = []
    # port times left
    dct = {}
    # ultimate destinations
    dests = (p % numberOfPorts for p in packetIds)
    for count, d in enumerate(dests):
        # if current port is busy
        while dct.get(d, 0) > count:
            # try next port
            d = (d + 1) % numberOfPorts
        out.append(d)
        dct[d] = transmissionTime + count
    return out


# driver code
if __name__ == "__main__":
    out = sentTimes(numberOfPorts=3, transmissionTime=2, packetIds=[4, 7, 10, 9])
    print(out)     # [1, 2, 1, 0]
    
    out2 = sentTimes(numberOfPorts=5, transmissionTime=4, packetIds=[*range(1, 12), 13, 12, 14, 15, 18, 16, 17, 20, 19])
    print(out2)    # [1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 3, 2, 4, 0, 3, 1, 2, 0, 4]
