#from cmath import inf
import json
from opcode import hasconst
import telnetlib
import time
from datetime import datetime


#from .const import LOGGER
import logging

#from config_flow import CannotConnect

_LOGGER = logging.getLogger(__name__)

class Spa:
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._timeout = 10

    def connect(self):
        try:
            result = self.get_device_info()
        except Exception as e:
            raise ConnectionResetError

        return result
        #return True


    def command(self, msg_data, msg_type = 1):
        try:
            sid = datetime.utcnow().strftime('%s%f')[:-3]
            command = {
                "data": msg_data,
                #"sid": str(int(time.time())) + "001",
                "sid": sid,
                "type": msg_type
            }

            command = json.dumps(command)
            
            telnet = telnetlib.Telnet(self._host, self._port)
            telnet.write(command.encode("ASCII") + b"\r")
            response = telnet.read_until(b"\n", timeout=self._timeout)
            
            _LOGGER.debug("telnet response: %s", response.decode("ASCII").strip())
            result = json.loads(response.decode("ASCII").strip())

            if result["sid"] != sid:
                _LOGGER.error("sid in response differs from sid in request")
                raise ConnectionRefusedError
                return None
            return result
        except ConnectionResetError as error:
            _LOGGER.info(
                'Command "%s" failed with exception: %s', command, repr(error)
            )
            raise ConnectionResetError
            return None
        except OSError as error:
            _LOGGER.error(
                'Command "%s" failed with exception: %s', command, repr(error)
            )
            return None

    def get_update(self):
        #response = json.dumps(command.encode("ASCII"))
        #result = json.loads(response.decode("ASCII").strip())

        response = self.command("8888060FEE0F01DA")
        if response["result"] != "ok":
            return None
        return response["data"]

    def get_device_info(self):
        response = self.command("1654467840319", 3)
        data = json.loads(response['data'])
        info = {
            'ip': data['ip'],
            'dtype': data['dtype'],
            'uid': data['uid'],
            'model': 'Unknown SPA',
            'type': '0000'
        }

        #wild guess here, original app says, my spa is "Bubble SPA V28062"
        #end of my uid string is 2000008062
        if data['dtype'] == 'spa':
            if len(data['uid']) == 26:
                info["type"] = type = data['uid'][22:26:1]
                #https://community.home-assistant.io/t/intex-pure-spa-wifi-control/323591/25
                if  type == "8062":
                    info['model'] = 'Bubble SPA V2' + type
                #https://community.home-assistant.io/t/intex-pure-spa-wifi-control/323591/26
                elif type == "2448":
                    info['model'] = 'Bubble SPA ' + type

        return info


#
#class SpaAsync:
#    def __init__(self, hass, config_entry):
#        self.hass = hass
#        self.config_entry = config_entry
#        self.spa = None
#
#    async def async_setup(self):
#        self.spa = await get_spa(self.hass, self.config_entry.data['host'], self.config_entry.data['port'])

#async def get_spa(hass, host, port):
#    spa = Spa(host, port)
#    try:
#        spa.connect()
#    except:
#        raise CannotConnect
#        
#    return spa
