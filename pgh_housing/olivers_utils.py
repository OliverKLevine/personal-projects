import sys
import os
from functools import reduce
from operator import getitem
import json

#Easily write output to either the console or a file
class output:
    def __init__(self, output_file = False):
        self.output_file = output_file
    def __enter__(self):
        if self.output_file:
            return open(self.output_file,"w")
        else:
            return console
    def __exit__(self, *args):
        pass

class console:
    def __init__(self):
        pass
    def write(string):
        print(string,end="")

#Parse input args
def olivargs(args, defaults = {}, start_index = 1):
    params = defaults
    arg_len = 1
    #get args into standard format
    functions = {
        "int":int,
        "str":str,
        "memory_format":memory_format,
        "memft":memory_format,
        "abspath":abs_path
    }
    for arg in args:
        if callable(args[arg][-1]): 
            arg_len = 2
            break
        if args[arg][-1] in functions:
            arg_len = 2
            break
    for arg in args:
        if type(args[arg]) == str: 
            if arg_len == 1: args[arg] = [args[arg]]
            else: args[arg] = [args[arg], str]
        else:
            args[arg] = list(args[arg])
            if callable(args[arg][-1]): pass
            elif args[arg][-1] in functions: args[arg][-1] = functions[args[arg][-1]]
            else: args[arg].append(str)
            if len(args[arg]) > 2: args[arg] = [args[arg][:-1],args[arg][-1]]
            if type(args[arg][0]) == str: args[arg][0] = [args[arg][0]]
    
    #parse the args
    unparsed = []
    for index in range(start_index,len(sys.argv)):
        prev = sys.argv[index-1]
        this = sys.argv[index]
        if prev in args:
            value = args[prev][1](this)
            setdict(params,args[prev][0],value)
        elif this in args:
            pass
        else:
            unparsed.append(this)
    
    return params, unparsed

#return decimal value for memory in specified units (default mb)
def memory_format(data, units="mb"):
    inpt = data
    if units == "mb" and type(data) is str:
        data = data.split("=")[-1].lower()
        for unit in ["tb","gb","mb","kb"]:
            if unit in data:
                units = unit
                data = data.replace(unit,"")
    correction = {
        "tb":1000000,
        "gb":1000,
        "mb":1,
        "kb":0.001
    }[units]
    try:
        data = float(data)*correction
        if int(data) == data:
            data = int(data)
        return data
    except:
        raise Exception(f"Unable to interpret memory value {inpt}")

#handle dictionaries with a list of keys
def getdict(dictionary, map_list):
    return reduce(getitem, map_list, dictionary)
    
def setdict(dictionary, map_list, value):
    if type(map_list) is str: map_list = [map_list]
    try:
        getdict(dictionary, map_list[:-1])[map_list[-1]] = value
    except:
        if(len(map_list) > 1): 
            setdict(dictionary, map_list[:-1],{})
            setdict(dictionary, map_list, value)
        else:
            raise Exception

#os.path.abspath, with some defaults
def abs_path(path=False):
    if not path: path = os.getcwd()
    return os.path.abspath(os.path.expanduser(path))

#better/relaxed interpretations of bool values which are passed as string
def relaxed_bool(value):
    if not value:
        return False
    try: 
        if value.lower() != "false":
            return True
    except: pass
    return False

def jprint(object):
    print(json.dumps(object, indent=4))


def download_spreadsheet(key,worksheet="Sheet1",silent=False):
    import gspread
    if not silent: print("Downloading table from google sheets",file=sys.stderr)
    gc = gspread.service_account()
    table = gc.open_by_key(key).worksheet(worksheet).get_values()
    return table

def upload_spreadsheet(key,table,range=None,worksheet="Sheet1",silent=False,reformat=False):
    import gspread
    if type(range) is not str:
        if range is None:
            range = [len(table[0]),len(table)]
        range = get_range(range)

    if not silent: print("Exporting table to google sheets",file=sys.stderr)
    gc = gspread.service_account()
    gc.open_by_key(key).worksheet(worksheet).update(range_name=range,values=table,raw=False)

    if reformat:
        import gspread_formatting
        fmt = gspread_formatting.cellFormat(textFormat=gspread_formatting.textFormat(bold=False))
        worksheet = gc.open_by_key(key).worksheet(worksheet)
        gspread_formatting.format_cell_range(worksheet,range,fmt)


def get_range(coord):
    range_values = [["A",1],["A",1]]
    def letter(num, is_index=False):
        if not is_index: num = num-1
        if num < 27:
            return "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[num]
        if num/26 < 27:
            return "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[int(num)] + "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[num-int(num)]
    method = [letter, int]
    if type(coord[0]) is not list: coord = [[1,1],coord]
    for x in range(2):
        for y in range(2):
            try: range_values[x][y] = method[y](coord[x][y])
            except: 
                try: range_values[x][y] = coord[x][y]
                except: pass
    return ":".join(["".join([str(item) for item in line]) for line in range_values])
