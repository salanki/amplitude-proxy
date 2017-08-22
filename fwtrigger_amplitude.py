"""
Amplitude event tracking emitter.

Version 1.0
"""

# Change these
USER_ID_ATTRIBUTE = "subscriberId"
PROXY_IP = "127.0.0.1"
PROXY_PORT = 41255

import json
import socket

class Trigger(FirewallTrigger):
    def __init__(self):
        FirewallTrigger.__init__(self)  # don't forget this!'

        self.addr = (PROXY_IP, PROXY_PORT)
        self.udpSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def trigger(self):
        event_data = {
            'client_ip': self.client_ip,
            'server_ip': self.server_ip,
            'client_is_local': self.client_is_local,
            'server_is_local': self.server_is_local,
            'server_hostname': self.server_hostname,
        }

        user_properties = {}
        if self.session_context['session']: user_properties.update(self.session_context['session'])
        if self.session_context['subscriber']: user_properties.update(self.session_context['subscriber'])

        if user_properties.pop(USER_ID_ATTRIBUTE) is None:
            print "%s does not exist, skipping" % USER_ID_ATTRIBUTE
            return

        data = {
            'event_type': self.name.replace("Event Log Trigger: ",""),
            'user_id': 1,
            'event_properties': event_data,
            'user_properties': user_properties,
        }

        self.udpSock.sendto(json.dumps(data), self.addr)
