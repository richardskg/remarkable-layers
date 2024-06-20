from struct import pack, unpack, calcsize

from ..constants import Pen, Colour, Width
from .base import ByteableList
from .segment import Segment
from math import sqrt
from math import trunc
import logging
import random

logger = logging.getLogger(__name__)

class Stroke(ByteableList):
    __slots__ = ("pen", "colour", "width", "xSegments")

    @classmethod
    def child_type(cls):
        return Segment

    def __init__(
        self,
        pen: Pen = Pen.DEFAULT,
        colour: Colour = Colour.BLACK,
        width: Width = Width.MEDIUM,
        xSegments = [],
    ):
        self.pen = pen
        self.colour = colour
        self.width = width
        self.xSegments = xSegments
        super().__init__()

    def __str__(self):
        return f"Stroke: pen={self.pen.name}, colour={self.colour.name}, width={self.width.name}, nobjs={len(self.objects)} "
        f"width={self.width.name}, nobjs={len(self.objects)}"

    def to_bytes(self, buffer):
        buffer.write(
            pack("<IIIfI", self.pen.value, self.colour.value, 0, self.width.value, 0)
        )
        super().to_bytes(buffer)

    @classmethod
    def from_bytes(cls, buffer):
        fmt = "<IIIfI"
        pen, colour, _, width, _ = unpack(fmt, buffer.read(calcsize(fmt)))
        ins = super().from_bytes(buffer)
        ins.pen = Pen(pen)
        ins.colour = Colour(colour)
        ins.width = Width(width)
        ins.xSegments = []
        return ins

    def to_svg(self, buffer):
        width = self.width.value
        if self.pen == Pen.RUBBER:
            width = width * 20
        elif self.pen != Pen.HIGHLIGHTER:
            width = 18 * width - 32

        buffer.write(
            f'<polyline fill="none" stroke="{self.colour.name.lower()}" '
            f'stroke-width="{width}" points="'
        )
        super().to_svg(buffer)
        buffer.write('"></polyline>')

    
    def init_children(self, time):
        r = trunc(random.random() * 10000)
        # x, y, speed = [], [], []
        # for obj in self.objects:
        #     x1, y1, s1 = obj.get_x_y_speed()
        #     x.append(x1)
        #     y.append(y1)
        #     speed.append(s1)
        #     self.xSegments.append(x1)
            # logger.debug('stroke adding x: %s', x1)

        # time = 0
        # logger.debug('stroke init_children len(x): %s, r: %s, x[1]: %s', len(x), r, x[1])
        # for i in range(0,len(x)):
            # dx = x[i]-x[i-1]
            # dy = y[i]-y[i-1]
            # d = sqrt(dx*dx + dy*dy)
            # s = speed[i]
            # dt = d/s if s != 0.0 else 1.0
            # time += dt
            # self.objects[i].set_distance(d)
            # self.objects[i].set_time(time)

        # for i, obj in enumerate(self.objects, start=1):
        for obj in self.objects:
            time += 1
            obj.set_time(time)
        return time

    def myscriptJSON(self, jsonObject):
        # logger.debug('in Stroke')
        # logger.debug('x.length: %s', len(self.xSegments))
        strokesGroupEntry = {}
        strokesGroupEntry['strokes'] = []
 
        strokeEntry = {}
        strokeEntry['x'] = []
        strokeEntry['y'] = []
        strokeEntry['t'] = []
        strokeEntry['p'] = []
        strokeEntry['pointerType'] = 'PEN' if self.pen != Pen.RUBBER else 'ERASER' # what about highlighter?
        for obj in self.objects:
            strokeEntry['x'].append(obj.get_x())
            strokeEntry['y'].append(obj.get_y())
            strokeEntry['t'].append(obj.get_t())
            strokeEntry['p'].append(obj.get_p())

        strokesGroupEntry['strokes'].append(strokeEntry)
        jsonObject['strokeGroups'].append(strokesGroupEntry)
        return

        





