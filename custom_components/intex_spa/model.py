
from .const import ATTR_MANUFACTURER, DOMAIN

from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

class IntexSpaEntity(CoordinatorEntity):
    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.info['unique_id'])},
            "name": ATTR_MANUFACTURER+" "+self.info['model'],
            "manufacturer": ATTR_MANUFACTURER,
            "model": self.info['model'],
        }
