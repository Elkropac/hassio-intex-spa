#from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTR_MANUFACTURER, DOMAIN

class IntexSpaEntity(CoordinatorEntity):
    """Common class"""

    @property
    def device_info(self):
        """Register to device"""
        return {
            "identifiers": {(DOMAIN, self.info['unique_id'])},
            "name": ATTR_MANUFACTURER+" "+self.info['model'],
            "manufacturer": ATTR_MANUFACTURER,
            "model": self.info['model'],
        }
