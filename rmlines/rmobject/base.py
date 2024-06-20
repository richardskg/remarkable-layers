import logging
from struct import pack, unpack
import json

logger = logging.getLogger(__name__)

def obj_dict(obj):
    return obj.__slots__


class ByteableList:
    __slots__ = 'objects', 'jsonObject'

    @classmethod
    def child_type(cls):
        raise NotImplementedError('Must specify child type for reading byte data')

    def __init__(self):
        self.objects = []
        layers = []
        self.jsonObject = []

    def append(self, obj):
        self.objects.append(obj)

    def extend(self, objs):
        self.objects.extend(objs)

    def dump(self):
        logger.debug(self)
        for obj in self.objects:
            obj.dump()
            # logger.debug('dumping obj = ')

    def myscriptJSON(self, jsonObject={}):
        # logger.debug('the json will be here eventually')
        jsonObject['xDPI'] = 96
        jsonObject['yDPI'] = 96
        jsonObject['width'] = 800
        jsonObject['height'] = 1200
        jsonObject['contentType'] = 'Math'

        jsonObject['strokeGroups'] = []
        for obj in self.objects:
            obj.myscriptJSON(jsonObject)            
            
        jsonString = json.dumps(jsonObject)

        debugBreak = 0
        return jsonString

    def to_bytes(self, buffer):
        buffer.write(pack('<I', len(self.objects)))
        for obj in self.objects:
            obj.to_bytes(buffer)

    @classmethod
    def from_bytes(cls, buffer):
        (n_objs,) = unpack('<I', buffer.read(4))
        ins = cls()
        ins.objects = [cls.child_type().from_bytes(buffer) for i in range(n_objs)]
        return ins

    def to_svg(self, buffer):
        for obj in self.objects:
            obj.to_svg(buffer)

    def init_children(self, time):
        for obj in self.objects:
            time = obj.init_children(time)  
        return      
