import requests
import os, re
from bs4 import BeautifulSoup

URL = "https://codeforces.com"
SOL = './solution'
PROB = './problem'
visited = [0 for i in range(100)]
problem = {}
solution = {}
sess = requests.Session()

def visitPage(url):
    '''eg: url = https://codeforces.com/problemset'''
    sourceCode = requests.get(url)
    text = sourceCode.text
    soup = BeautifulSoup(text, features="html.parser")
    for link in soup.findAll("a"):
        href = link.get('href')
        comp = href.split('/')
        if 'page' in comp:
            pageNo = int(comp[-1])
            if visited[pageNo] == 0:    
                visited[pageNo] = 1
                visitPage(URL + href)
        elif len(comp) == 5 and comp[2] == 'problem':
            try: 
                problem[href]
            except KeyError:
                problem[href] = 1
                getProblem(URL + href)
        elif len(comp) == 6 and comp[-2] == 'problem':
            try:
                solution[href]
            except KeyError:
                solution[href] = 1
                getSolution(URL + href)

def getProblem(url):
    '''eg: url = https://codeforces.com/problemset/problem/1464/F'''
    tmp = url.split('/')
    tmp = '/' + tmp[-2] + tmp[-1]
    f = open(PROB + tmp + '.txt', "w")
    sourceCode = requests.get(url)
    text = sourceCode.text
    soup = BeautifulSoup(text, features="html.parser")
    soup = soup.find('div', {'class': 'problem-statement'})
    # for script in soup(["script", "style"]):
    #     script.extract()
    allDiv = soup.findAll('div')
    exc = ['input-specification', 'output-specification', 'input', 'output', 'note']
    for i in allDiv:
        if len(i.findAll('div')) > 0:
            if not i.has_attr('class') or i['class'][0] not in exc:
                continue
        content = getContent(i)
        if content not in ['Output\\\\', 'Input\\\\']:
            f.write(content + '\n\n')

def getSolution(url):
    '''eg: url = https://codeforces.com/problemset/status/1464/problem/F'''
    print("visiting", url)
    source = requests.get(url)
    text = source.text
    soup = BeautifulSoup(text, features = 'html.parser')
    soup = soup.find('table', {'class' : 'status-frame-datatable'})
    soup = soup.findAll('tr')[1]
    language = soup.findAll('td')[4].get_text().strip()
    ext = getExtension(language)

    soup = soup.find('a', {'class' : 'view-source'})
    soup = requests.get(URL + soup.get('href'))
    soup = soup.text 
    soup = BeautifulSoup(soup, features = 'html.parser')
    soup = soup.find('pre')
    store_code(soup.get_text(), url, ext)

def getExtension(s):
    if 'C++' in s:
        return '.cpp'
    if 'C#' in s:
        return '.cs'
    if 'Python' in s or 'PyPy' in s:
        return '.py'
    if 'C11' in s:
        return '.c'
    if 'Java' in s:
        return '.java'
    if 'Kotlin' in s:
        return '.kt'
    if 'Ruby' in s:
        return '.rb'
    if 'Rust' in s:
        return '.rs'
    if 'Scala' in s:
        return '.sc'
    return '.txt'

def store_code(text, url, extension = '.txt'):
    '''eg: url = https://codeforces.com/problemset/status/1464/problem/F'''
    tmp = list(url.split('/'))
    tmp = '/' + tmp[-3] + tmp[-1]
    f = open(SOL + tmp + extension, "w")
    f.write(text)

def store_problem(text, url):
    tmp = list(url.split('/'))
    tmp = '/' + tmp[-2] + tmp[-1]
    f = open(PROB + tmp + '.txt', "w")
    f.write(text)

def getContent(soup):
    text = soup.get_text()
    lines = (line.strip() for line in text.split('\n'))
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk and '\u2192' not in chunk)
    text = "".join((i if i != '/' else '//') for i in text)
    text = ''.join(i for i in text if ord(i) < 128)
    text = '$'.join(text.split('$$$'))
    text = '\\\\\n'.join(text.split('\n'))
    text += '\\\\'
    return text
        
if __name__ == "__main__":
    if not os.path.exists(SOL):
        os.makedirs(SOL)
    if not os.path.exists(PROB):
        os.makedirs(PROB)
    
    visitPage(URL + '/problemset')
    # getProblem('https://codeforces.com/problemset/problem/1464/F')
    # getSolution('https://codeforces.com/problemset/status/1468/problem/N')
    # [print(i, end = ',') for i in range(1, 67) if visited[i] == 0]

