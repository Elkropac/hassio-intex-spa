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


    def command(self, data):
        try:
            sid = datetime.utcnow().strftime('%s%f')[:-3]
            command = {
                "data": data,
                "sid": str(int(time.time())) + "001",
                "type": 1
                "sid": sid,
            }

            command = json.dumps(command)
            
            telnet = telnetlib.Telnet(self._host, self._port)
            telnet.write(command.encode("ASCII") + b"\r")
            response = telnet.read_until(b"\r", timeout=self._timeout)
            _LOGGER.debug("telnet response: %s", response.decode("ASCII").strip())
            result = json.loads(response.decode("ASCII").strip())
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

