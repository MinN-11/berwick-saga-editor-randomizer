
import BWSEditor
import sys
import shutil

try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO

from pycdlib import PyCdlib


def ModifyData3(source_iso, target_iso, script):
    if target_iso != source_iso:
        shutil.copyfile(source_iso, target_iso)
    iso = PyCdlib()
    iso.open(target_iso, "rb+")
    data3 = BytesIO()
    iso.get_file_from_iso_fp(data3, iso_path='/DATA3.DAT;1')
    buffer = bytearray(data3.getvalue())
    BWSEditor.parse_script(buffer, script)
    iso.modify_file_in_place(BytesIO(buffer), len(buffer), '/DATA3.DAT;1')
    iso.close()


def main():
    if len(sys.argv) < 2:
        pass
    elif len(sys.argv) < 4:
        print("python3 ISOEditor.py BerwickSagaRom.iso Target.iso YOUR_SCRIPT")
    if len(sys.argv) < 4:
        quit()
    _, data, output, script = sys.argv[:4]

    with open(script, "r") as script_file:
        script = script_file.read()

    ModifyData3(data, output, script)


if __name__ == '__main__':
    main()
