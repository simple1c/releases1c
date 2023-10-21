from releases1c.request1c import Request1C
from releases1c.secrets import credentials
import os
from releases1c.progress import printProgressBar

releasesURL = "https://releases.1c.ru"

def get_data(url,flush_cookie=False):
    r1c = Request1C(**credentials,flush_cookie=flush_cookie)
    return r1c.get(url)

def get_head(url, flush_cookie=False):
    r1c = Request1C(**credentials,flush_cookie=flush_cookie)
    return r1c.get_head(url)

def get_stream(url, flush_cookie=False):
    r1c = Request1C(**credentials,flush_cookie=flush_cookie)
    return r1c.get_stream(url)

class WrongFiletype(Exception):
    filetype = ''
    matches = []
    def __init__(cls,fyletype,matches=[]):
        super()
        cls.fyletype = fyletype
        cls.matches = matches

def get_download_url_by_filetype(**kwargs):

    __file_list = [x for x in get_data(releasesURL+"/version_files?nick={product}&ver={version}".format(**kwargs),kwargs.get("flush_cookie")) if x.get('filetype')==kwargs.get("filetype")]
    if len(__file_list) == 0:
        raise WrongFiletype(kwargs.get("filetype"))
    elif len(__file_list) == 1:
        url = f"{releasesURL}{__file_list[0].get('url')}"
    else:
        raise WrongFiletype(kwargs.get("filetype"),__file_list)
    
    return url

def __is_dirname(path):
    if (path == '.' or path == '..' or os.path.isdir(path)):
        path = os.path.join(path,'')
    return path[-1] == os.sep

def get_filename_from_url(url):
    resph = get_head(url)

    if (resph.headers.get('content-disposition')):
        filename = [x[1].replace('"','') for x in [k.strip().split('=') for k in resph.headers.get('content-disposition').split(';')] if x[0] == 'filename'][0]
    else:
        filename = resph.url.split('/')[-1]
    return filename

def get_local_filename(url,path):
    if __is_dirname(path):
        filename = get_filename_from_url(url)
        return os.path.join(path,filename)
    else:
        return path

def download(**kwargs):
    url = get_download_url_by_filetype(**kwargs)
    mirrors = get_data(url, kwargs.get('flush_cookie'))
    #print('mirrors',mirrors)
    result = None
    for download_url in mirrors:
        result = download_file(download_url,kwargs.get('dest'))
        if result:
            break
    return result

def download_file(url:str, dest:str):
    file_name = get_local_filename(url,dest)
    print('Downloading to:', file_name)
    r = get_stream(url)
    with open(file_name, "wb") as f:
        total_length = r.headers.get('content-length')
        if total_length is None: # no content length header
            f.write(r.content)
            print('Complete!')
        else:
            dl = 0
            total_length = int(total_length)
            for chunk in r.iter_content(chunk_size=int(total_length/5000)):
                if chunk:
                    f.write(chunk)
                    f.flush()
                dl += len(chunk)
                printProgressBar(dl, total_length, prefix = 'Progress:', suffix = f'Complete ({int(total_length/1024/1024)} Mb)', length = 50)
    
    return {'result':True, 'file_name':file_name}
