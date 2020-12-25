import requests
import os
from bs4 import BeautifulSoup

URL = "https://codeforces.com"
DIR = './solution'
visited = [0 for i in range(100)]
problem = {}
solution = {}
sess = requests.Session()

def visitPage(url):
    sourceCode = requests.get(url)
    text = sourceCode.text
    soup = BeautifulSoup(text, features="html.parser")
    for link in soup.findAll("a"):
        # print(link)
        href = link.get('href')
        comp = href.split('/')
        if 'page' in comp:
            continue
            pageNo = int(comp[-1])
            if visited[pageNo] == 0:    
                visited[pageNo] = 1
                # print(URL + href)
                visitPage(URL + href)
        elif len(comp) == 5 and comp[2] == 'problem':
            continue
            try: 
                x = problem[href]
            except KeyError:
                problem[href] = 1
                getProblem(URL + href)
        elif len(comp) == 6 and comp[-2] == 'problem':
            try:
                x = solution[href]
            except KeyError:
                solution[href] = 1
                getSolution(URL + href)

def getProblem(url):
    '''eg: url = https://codeforces.com/problemset/problem/1464/F'''
    f = open('crawler.out', "w")
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
        if not i.has_attr('class'):
            content = ' '.join(content.split()[:10])
        f.write(getContent(i) + '\n')

    # text = soup.get_text()
    # lines = (line.strip() for line in text.splitlines())
    # chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # text = '\n'.join(chunk for chunk in chunks if chunk and '\u2192' not in chunk)
    # res = ""
    # for i in text:
    #     if i == '/':
    #         res += '//'
    #     else:
    #         res += i 
    # f.write(res)

    # tag_list = [i.contents[0] for i in soup.findAll('span', {'class' : 'tag-box'})]
    # for i in range(len(tag_list)):
    #     tag_list[i] = getContent(tag_list[i])
    # f.write("Tag: " + ' '.join(tag_list) + '\n')
    # f.write('\n')

    # problem = soup.find('div', {'class' : 'problem-statement'})
    # print("Crawling problem:", url)

    # title = "".join(problem.find('div', {'class' : 'title'}).contents)
    # f.write(title + '\n')
    # f.write('\n')

    # time_limit = problem.find('div', {'class' : 'time-limit'}).contents[-1]
    # f.write("Time limit: " + time_limit + '\n')
    # mem_limit = problem.find('div', {'class' : 'memory-limit'}).contents[-1]
    # f.write("Memory limit: " + mem_limit + '\n')
    # input_file = problem.find('div', {'class' : 'input-file'}).contents[-1]
    # f.write("Input: " + input_file + '\n')
    # output_file = problem.find('div', {'class' : 'output-file'}).contents[-1]
    # f.write("Output: " + output_file + '\n')
    # f.write('\n')

def getSolution(url):
    '''eg: url = https://codeforces.com/problemset/status/1464/problem/F'''
    print("visiting", url)
    source = requests.get(url)
    text = source.text
    soup = BeautifulSoup(text, features = 'html.parser')
    soup = soup.find('a', {'class' : 'view-source'})
    soup = requests.get(URL + soup.get('href'))
    soup = soup.text 
    soup = BeautifulSoup(soup, features = 'html.parser')
    soup = soup.find('pre')
    store_code(soup.get_text(), url)

def store_code(text, url, extension = '.txt'):
    tmp = list(url.split('/'))
    tmp = '/' + tmp[-3] + tmp[-1]
    f = open(DIR + tmp + '.txt', "w")
    f.write(text)

def getContent(soup):
    text = soup.get_text()
    lines = (line.strip() for line in text.split('\n'))
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk and '\u2192' not in chunk)
    text = "".join((i if i != '/' else '//') for i in text)
    text = ''.join(i for i in text if ord(i) < 128)
    # text = ' '.join(text.split()[:20])
    return text
        
if __name__ == "__main__":
    if not os.path.exists(DIR):
        os.makedirs(DIR)
    visitPage(URL + '/problemset')
    # crawl("https://codeforces.com/problemset/problem/1444/C")
    # getSolution('https://codeforces.com/problemset/status/1464/problem/F')
    # [print(i, end = ',') for i in range(1, 67) if visited[i] == 0]
