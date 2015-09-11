import os
import json
import sys

from lxml import etree

tests = {}

def process_file(name):
    tree = etree.parse(name)
    xpath = tree.xpath("//xsl:when/@test",
                       namespaces={"xsl": "http://www.w3.org/1999/XSL/Transform"})
    test_xml = tree.xpath("/xsl:stylesheet/xsl:template/xsl:if[@test='false()']",
                          namespaces={"xsl": "http://www.w3.org/1999/XSL/Transform"})

    if not xpath:
        print("couldn't find xpath in %s" % name)
        sys.exit(1)
    xpath = xpath[0]
        
    if not (len(test_xml[0]) == 1):
        print("test didn't have single root element, %s" % name)
        print(test_xml)
        sys.exit(1)

    new = os.path.basename(name)
    tests[new] = xpath

    with open("new/" + new, "wb") as fp:
        fp.write(etree.tostring(test_xml[0][0], encoding="utf-8"))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("needs more args")
        sys.exit(2)

    d = sys.argv[1]
    files = os.listdir(d)
    for f in files:
        if f.endswith(".xml") and f != "ref.xml":
            process_file(os.path.join(d, f))

    with open("new/tests.json", "w") as fp:
        json.dump(tests, fp, indent=4)
