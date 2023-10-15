from bs4 import BeautifulSoup
import re

def parse_releases_main_page(html_data):
    tdada = BeautifulSoup(html_data,features="html5lib").table.table
    data = []

    for row in tdada("tr"):
        if len(row('td')) != 8:
            continue

        columns = row('td')
        data.append({
            'url': columns[0].a.get('href'),
            'name': columns[0].a.get('href').replace('/project/',''),
            'description': columns[0].a.string,
            'actual_versions': [{
                'url':v.get('href'),
                'name':v.string,
                'date':d.string.strip(),
                } for v,d in zip(columns[1]('a'),columns[2]('span'))
            ],
            'plan_versions': [{
                'url':v.get('href'),
                'date':d.string.strip(),
                'update':ud.string.strip(),
                } for v,d,ud in zip(columns[3]('a'),columns[4]('span'),columns[5]('span'))
            ],
            'beta_versions': [{
                'url':v.get('href'),
                'name':v.string,
                'date':d.string.strip(),
                } for v,d in zip(columns[6]('a'),columns[7]('span'))
            ],
        })
    
    return data

def parse_project_page(html_data):

    tdada = BeautifulSoup(html_data,features="html5lib").table.table

    data = []

    for row in tdada.tbody('tr'):
        columns = row('td')
        data.append({
            'url': columns[0].a.get('href'),
            'version': columns[0].a.string.strip(),
            'date':columns[1].string.strip(),
            'previous_versions': columns[2].string.strip(),
        })

    return data

def parse_version_files(html_data):

    tdada = BeautifulSoup(html_data,features="html5lib")

    pattern = r"nick=(\S+)&ver=(\d+(?:.\d+)+)(?:&path=.*%5c(.*))?"

    data = []

    for row in tdada.table('tr')[1].div('a')[1:-1]:
        matcher = re.search(pattern,row.get('href'))
        nick = matcher.group(1)
        nick_wo_numbers = re.sub("\d",'',nick)
        version = matcher.group(2)
        filename = matcher.group(3)
        if (filename):
            data.append({
                'url': row.get('href'),
                'name': row.string.strip(),
                'nick': nick,
                'version': version,
                'file': filename,
                'filetype': filename
                    .replace('_'+version.replace('.','_'),'')
                    .replace('_'+version,'')
                    .replace(nick+'_','')
                    .replace(nick_wo_numbers+'_',''),
            })

    return data

def parse_sources(html_data):

    tdada = BeautifulSoup(html_data,features="html5lib")

    data = []

    for row in tdada('div',{"class": "downloadDist"})[0]('a'):
        data.append(row.get('href'))

    return data