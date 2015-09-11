import csv
import sys
import urllib.parse as urlparse

def convert(fp_in, fp_out):
    reader = csv.reader(fp_in, "excel-tab")
    for row in reader:
        if row:
            converted = convert_row(row)
            fp_out.write(converted + "\n")

def convert_row(row):
    test = row[0]
    ref = row[1]
    test_type = row[2]

    test = rewrite_url(test)
    ref = rewrite_url(ref)

    if test_type == "eq":
        return "== %s %s" % (test, ref)
    elif test_type == "neq":
        return "!= %s %s" % (test, ref)
    else:
        raise Exception("unknown test type %s" % test_type)
    
def rewrite_url(url):
    parsed = urlparse.urlparse(url)
    if parsed.scheme not in ("http", "about"):
        raise Exception("not http, %s" % parsed.scheme)
    if parsed.netloc not in ("t", "t.oslo.opera.com", ""):
        raise Exception("unknown host, %s" % parsed.netloc)

    new = list(parsed)

    if parsed.scheme == "http":
        new[0] = ""
    new[1] = ""
        
    if (parsed.path.startswith("/core/standards/css") or
        parsed.path.startswith("/core/standards/current-style/") or
        parsed.path.startswith("/core/standards/dom2ss/") or
        parsed.path.startswith("/core/standards/hover/") or
        parsed.path.startswith("/core/standards/quotes/") or
        parsed.path.startswith("/core/standards/selectors/")):
        new[2] = "/css/" + parsed.path[16:]

    if parsed.path.startswith("/core/standards/SVG/"):
        new[2] = "/SVG/" + parsed.path[16:]
        
    if parsed.path.startswith("/core/bts/reftest/references/"):
        new[2] = "/references/" + parsed.path[29:]

    if parsed.scheme == "http":
        new[2] = new[2][1:]

    return urlparse.urlunparse(new)

def main():
    if len(sys.argv) < 3:
        raise Exception("too few args")
        return

    with open(sys.argv[1], "r", encoding="utf8") as fp_in:
        with open(sys.argv[2], "w", encoding="utf8") as fp_out:
            convert(fp_in, fp_out)

if __name__ == "__main__":
    main()
