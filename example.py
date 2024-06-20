from pathlib import Path
from rmlines import RMLines
import logging
from io import StringIO
import hashlib
import hmac

logging.basicConfig(level="DEBUG")
p = Path("./samples/2.rm")
# p = Path("./samples/03f23a6e-c14b-4dba-836d-828707979356.rm")
rm0 = RMLines.from_bytes(p.open("rb"))
# To reduce logging for some binary types, eg:
# logging.getLogger('rmlines.rmobject.segment').setLevel(logging.INFO)

rm0.init_children(0)
jsonString = rm0.myscriptJSON()
fj = open('rmTempOut.json', 'w')
fj.write(jsonString)
fj.close
# rm0.dump()

sbuffer = StringIO()
rm0.to_svg(sbuffer)
f = open('rmTempOut.svg', 'wb')
f.write(sbuffer.getvalue().encode())
f.close

hmacString = hmac.new(jsonString.encode(), None, hashlib.sha512).hexdigest()
fh = open('rmTempOut.hmac', 'w')
fh.write(hmacString)
fh.close

debugBreak = 0