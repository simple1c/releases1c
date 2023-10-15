import click
from releases1c.request1c import Request1C
from releases1c.secrets import credentials
from releases1c import parsing
import os

releasesURL = "https://releases.1c.ru"

def safe_list_get (l, idx, default):
    try:
        return l[idx]
    except IndexError:
        return default

@click.group()
def cli():
    pass

@cli.command(short_help='Get information about projects, versions and files')
@click.option('-f','--flush-cookie',type=bool,is_flag=True,default=False, show_default=True,help="Flush the cookie")
@click.argument('parameters',nargs=-1,metavar='[PROJECT] | [PROJECT VERSION] | [PROJECT VERSION FILETYPE]')
def info(parameters,flush_cookie) -> None:
    '''Get information for project and verison and filetype'''

    settings = prepare_executors(parameters,flush_cookie)

    #print('>> DEBUG >>',settings['url'](parameters))

    print_info(settings, flush_cookie)


def print_info(settings, flush_cookie):
    
    data = get_data(settings['url'],flush_cookie)

    print('Getting data from URL:',settings['url'])
    
    #print(data)
    for row in data:
        settings['display'](row)

def prepare_executors(parameters,flush_cookie):

    lpr = len(parameters)
    is_file_list = False

    if lpr == 0:
        url = f"{releasesURL}/total"
        display = lambda product: print('-',product.get('name'),'-',product.get('description'),[v['name'] for v in product.get('actual_versions')])
    elif lpr == 1:
        url = f"{releasesURL}/project/{parameters[0]}?allUpdates=true"
        display = lambda v: print('-',v.get('version'),'-',v.get('date'),v.get('previous_versions'))
    elif lpr == 2:
        url = f"{releasesURL}/version_files?nick={parameters[0]}&ver={parameters[1]}"
        display = lambda f: print('-',f['filetype'],'-',f['file'],'-',f['name'])
    elif lpr == 3:
        __file_list = [x for x in get_data(releasesURL+f"/version_files?nick={parameters[0]}&ver={parameters[1]}",flush_cookie) if x.get('filetype')==parameters[2]]
        if len(__file_list) == 0:
            print("Wrong filetype:",parameters[2])
            return prepare_executors(parameters[:2],flush_cookie)
        else:
            url = f"{releasesURL}{__file_list[0].get('url')}"
            display = lambda f: print('-',f)
            is_file_list = True
    else:
        print("Unsupported parameters:", parameters[2:])
    
    return {'url':url, 'display':display, 'is_file_list':is_file_list}

def get_data(url,flush_cookie):
    r1c = Request1C(**credentials,flush_cookie=flush_cookie)
    return r1c.get(url)

@cli.command()
#@click.option('paths', '--path', envvar='PATHS', type=click.File())
#@click.argument('project')
#@click.argument('version')
#@click.argument('filetype')
@click.argument('parameters',nargs=3,metavar='PROJECT VERSION FILETYPE')
@click.argument('filepath',type=click.Path(exists=False,writable=True))
def download(parameters,filepath):
    '''Download file for project and version'''
    #print('filepath',filepath,os.path.isfile(filepath),os.path.isdir(filepath))
    settings = prepare_executors(parameters, False)
    if settings['is_file_list']:
        file_list = get_data(settings['url'], False)
        
        print('File list:', file_list)

        r1c = Request1C(**credentials,flush_cookie=False)
        return r1c.download(file_list[0],dest=filepath)
    else:
        print_info('ERROR >>>',settings, False)

if __name__ == "__main__":
    cli(auto_envvar_prefix='RELEASES1C')