import glob
from datetime import datetime


import os.path
import warnings
from io import BytesIO

from koala.xml.functions import fromstring, safe_iterator
from koala.unzip import read_archive
from koala.excel import read_named_ranges, read_cells
from koala.ast.tokenizer import ExcelParser

if __name__ == '__main__':

    files = glob.iglob("./data/*.xlsx")
    for file in files:  

        file_name = os.path.abspath(file)
        print file_name
        
        startTime = datetime.now()
        archive = read_archive(file_name)        

        named_range = read_named_ranges(archive)
        print "%s named ranged parsed in %s" % (str(len(named_range)), str(datetime.now() - startTime))

        startTime = datetime.now()
        cells = read_cells(archive)
        
        print "%s cells parsed in %s" % (str(len(cells)), str(datetime.now() - startTime))
        for cell in cells:
            if cell['f'] is not None:
                print "=========="
                print cell['f']
                p = ExcelParser();
                p.parse(cell['f'])
                print p.prettyprint()
