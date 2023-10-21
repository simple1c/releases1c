import click
from releases1c import __version__
from releases1c.request1c import Request1C
from releases1c.secrets import credentials
from releases1c.downloader import get_download_url_by_filetype, WrongFiletype, download
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
        try:
            url = get_download_url_by_filetype(**dict(zip(['product','version','filetype'],parameters)))
        except WrongFiletype as err:
            print("Wrong filetype:",parameters[2])
            return prepare_executors(parameters[:2],flush_cookie)
        else:

            #print('url',url)
            #url = f"{releasesURL}{__file_list[0].get('url')}"
            display = lambda f: print('-',f)
            is_file_list = True
    else:
        print("Unsupported parameters:", parameters[2:])
    
    return {'url':url, 'display':display, 'is_file_list':is_file_list}

def get_data(url,flush_cookie):
    r1c = Request1C(**credentials,flush_cookie=flush_cookie)
    return r1c.get(url)

@cli.command(name='download')
@click.argument('parameters',nargs=3,metavar='PROJECT VERSION FILETYPE')
@click.argument('filepath',type=click.Path(exists=False,writable=True))
@click.pass_context
def download_cmd(ctx,parameters,filepath):
    '''Download file for project and version'''
    #print('filepath',filepath,os.path.isfile(filepath),os.path.isdir(filepath))
    try:
        download(**credentials,**dict(zip(['product','version','filetype'],parameters)),dest=filepath)
    except WrongFiletype as err:
        print("Wrong filetype:",parameters[2])
        ctx.invoke(info(parameters[:2]))

@cli.command()
def version():
    print('Version:',__version__)

if __name__ == "__main__":
    cli(auto_envvar_prefix='RELEASES1C')