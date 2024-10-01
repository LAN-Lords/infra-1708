from pysnmp.entity import engine
from pysnmp.carrier.asyncio.dgram import udp
from pysnmp.entity.rfc3413 import ntfrcv
import asyncio

snmp_engine = engine.SnmpEngine()

# Trap handler function
def trap_receiver(snmp_engine, state_reference, context_engine_id, context_name,
                  var_binds, cb_ctx):
    print('Received SNMP Trap:')
    for name, val in var_binds:
        print(f'{name.prettyPrint()} = {val.prettyPrint()}')

# Set up UDP transport
config = udp.UdpTransport().openServerMode(('localhost', 162))
ntfrcv.NotificationReceiver(snmp_engine, trap_receiver)

# Run the SNMP engine to listen for traps
loop = asyncio.get_event_loop()
print("SNMP Trap Receiver is running...")
loop.run_forever()
