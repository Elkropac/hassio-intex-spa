import json
import telnetlib
import time
from datetime import datetime


#from .const import LOGGER
import logging

_LOGGER = logging.getLogger(__name__)

class Spa:
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._timeout = 10

    def connect(self):
        try:
            #self.command('{"data":"8888060FEE0F01DA","sid":"1630705186378","type":1}')
            #self.command('8888060FEE0F01DA')
            _LOGGER.info('ok')
        except ConnectionResetError as error:
            raise ConnectionResetError


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
        result = {
            "sid":"1630705186378",
            "data":"FFFF110F0101001D000000008080801E000021",
            "result":"ok",
            "type":2
        }
        #response = json.dumps(command.encode("ASCII"))
        #result = json.loads(response.decode("ASCII").strip())
        return result

    def get_device_info(self):
        response = self.command("1654467840319", 3)
        data = json.loads(response['data'])
        info = {
            'ip': data['ip'],
            'dtype': data['dtype'],
            'uid': data['uid'],
            'name': ''
        }

        #wild guess here, original app says, my spa is "Bubble SPA V28062"
        #end of my uid string is 2000008062
        if data['dtype'] == 'spa':
            info['name'] = 'Bubble SPA '
        if len(data['uid']) == 26:
            if data['uid'][16:17:1] == '2':
                info['name'] += 'V2'
            info['name'] += data['uid'][22:26:1]

        return info
