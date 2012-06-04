import os.path

basename = os.path.basename
exists = os.path.exists
join = os.path.join

try:
    rPath = os.path.realpath #@UndefinedVariable
except:
    # jython does not support os.path.realpath
    # realpath is a no-op on systems without islink support
    rPath = os.path.abspath


DEBUG_CLIENT_SERVER_TRANSLATION = False

#caches filled as requested during the debug session
NORM_FILENAME_CONTAINER = {}
NORM_FILENAME_AND_BASE_CONTAINER = {}
NORM_FILENAME_TO_SERVER_CONTAINER = {}
NORM_FILENAME_TO_CLIENT_CONTAINER = {}


pycharm_os = None

def normcase(file):
    return os.path.normcase(file)


def _NormFile(filename):
    try:
        return NORM_FILENAME_CONTAINER[filename]
    except KeyError:
        r = normcase(rPath(filename))
        #cache it for fast access later
        NORM_FILENAME_CONTAINER[filename] = r
        return r

ZIP_SEARCH_CACHE = {}
def exists(file):
    if os.path.exists(file):
        return True

    ind = file.find('.zip')
    if ind == -1:
        ind = file.find('.egg')

    if ind != -1:
        ind+=4
        zip_path = file[:ind]
        inner_path = file[ind+1:]
        try:
            zip = ZIP_SEARCH_CACHE[zip_path]
        except KeyError:
            try:
                import zipfile
                zip = zipfile.ZipFile(zip_path, 'r')
                ZIP_SEARCH_CACHE[zip_path] = zip
            except :
                return False

        try:
            info = zip.getinfo(inner_path)
            return True
        except KeyError:
            return False
    return False

def GetFileNameAndBaseFromFile(f):
    try:
        return NORM_FILENAME_AND_BASE_CONTAINER[f]
    except KeyError:
        filename = _NormFile(f)
        base = basename(filename)
        NORM_FILENAME_AND_BASE_CONTAINER[f] = filename, base
        return filename, base


def GetFilenameAndBase(frame):
    #This one is just internal (so, does not need any kind of client-server translation)
    f = frame.f_code.co_filename
    return GetFileNameAndBaseFromFile(f)


try:
    import org.python.core.PyDictionary #@UnresolvedImport @UnusedImport -- just to check if it could be valid

    def DictContains(d, key):
        return d.has_key(key)
except:
    try:
        #Py3k does not have has_key anymore, and older versions don't have __contains__
        DictContains = dict.__contains__
    except:
        try:
            DictContains = dict.has_key
        except NameError:
            def DictContains(d, key):
                return d.has_key(key)
