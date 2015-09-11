import argparse
import os
import json
import sys

from lxml import etree

tests = {}

def process_file(name, out_dir):
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

    with open(os.path.join(out_dir, new), "wb") as fp:
        fp.write(etree.tostring(test_xml[0][0], encoding="utf-8"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert XPath tests.')
    parser.add_argument('in_dir', metavar='IN', help='path to presto-testo XPath tests')
    parser.add_argument('out_dir', metavar='OUT', default="new",
                        help='path to output new XPath tests')

    args = parser.parse_args()

    d = args.in_dir
    files = os.listdir(d)
    for f in files:
        if f.endswith(".xml") and f != "ref.xml":
            process_file(os.path.join(d, f), args.out_dir)

    with open(os.path.join(args.out_dir, "tests.json"), "w") as fp:
        json.dump(tests, fp, indent=4)
