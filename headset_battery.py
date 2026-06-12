#!/usr/bin/env python3
import sys, struct, re, time
import hid

VID, PID = 0x10f5, 0x224c

# RACE SGSI request - queries headset status including battery
RACE_SGSI = bytes.fromhex('055a14000299480101000000000000000000610053475349')
HID_OUT = b'\x06' + struct.pack('<H', len(RACE_SGSI)) + RACE_SGSI
HID_OUT = HID_OUT + bytes(64 - len(HID_OUT))

def get_battery():
    try:
        dev = hid.device()
        dev.open(VID, PID)
        dev.set_nonblocking(0)
    except OSError:
        print("Headset dongle not found", file=sys.stderr)
        sys.exit(1)

    # Flush stale buffer
    for _ in range(5):
        dev.get_input_report(0x07, 64)

    dev.write(HID_OUT)

    full_data = b''
    for _ in range(20):
        resp = bytes(dev.get_input_report(0x07, 64))
        length = struct.unpack('<H', resp[1:3])[0]
        if length == 0:
            if len(full_data) > 0 and b'"2a0"' in full_data:
                break
            time.sleep(0.05)
            continue
        full_data += resp[3:3+length]

    dev.close()

    text = full_data.decode('utf-8', errors='replace')
    match = re.search(r'"2a0"\s*:\s*"(\d+)"', text)
    if not match:
        print("Could not read battery", file=sys.stderr)
        sys.exit(1)
    return int(match.group(1))

pct = get_battery()

if '--json' in sys.argv:
    print(f'{{"battery": {pct}}}')
elif '--short' in sys.argv:
    print(f'{pct}%')
else:
    print(f'Stealth 600: {pct}%')