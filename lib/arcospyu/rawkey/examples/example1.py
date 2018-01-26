#!/usr/bin/env python
from rawkey import Raw_key,Keys, is_key

def main():
    raw_key=Raw_key()
    while True:
        print "new cycle"
        num_chars=raw_key.get_num_chars(None)
        print "got", num_chars
        if is_key(num_chars,Keys.RIGHT_ARROW):
            print "Right arrow"
        if is_key(num_chars,Keys.d):
            print "d"


if __name__=="__main__":
    main()

