import os
import tempfile
from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree
from lxml.etree import _Element


def update_file(file,z:ZipFile):
    if file.filename.endswith(".html"):
        with z.open(file) as f:
            for l in (lines := f.readlines()):
                if "amzn" in l.decode("utf-8").lower():
                    tree: _Element = etree.fromstringlist(lines)
                    for x in tree.iter():
                        if x.get("data-AmznRemoved"):
                            del x.attrib["data-AmznRemoved"]
                        if x.get("data-AmznRemoved-M8"):
                            del x.attrib["data-AmznRemoved-M8"]

                    return etree.tostring(tree)
    return z.read(file)

def main(zipname):
    # generate a temp file
    tmpfd, tmpname = tempfile.mkstemp(dir=os.path.dirname(zipname))
    os.close(tmpfd)

    # create a temp copy of the archive without filename
    with ZipFile(zipname, 'r') as zin:
        with ZipFile(tmpname, 'w') as zout:
            zout.comment = zin.comment  # preserve the comment
            for item in zin.infolist():
                zout.writestr(item, update_file(item,zin))

    # replace with the temp archive
    os.remove(zipname)
    os.rename(tmpname, zipname)

if __name__ == '__main__':
    main()
