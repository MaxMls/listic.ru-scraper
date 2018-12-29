# https://listick.ru/share/w****
# class="content-wrap"  


import string, random, threading, sys, string, requests, time, pathvalidate as pv
from bs4 import BeautifulSoup as Soup


if len(sys.argv) < 2:
    sys.exit("\033[37mUsage: python " + sys.argv[0] + " (Number of threads)")
threadAmount = int(sys.argv[1])

alphabet = string.digits + string.ascii_lowercase + string.ascii_uppercase

def convert_base(num, to_base = 10, from_base = 10):
    global alphabet
    if isinstance(num, str):
        n = int(num, from_base)
    else:
        n = int(num)
    if n < to_base:
        return alphabet[n]
    else:
        return convert_base(n // to_base, to_base) + alphabet[n % to_base]
    


n = 0
i = 238328
def scrapePictures():
    global n, alphabet
    while True:
        n += 1

        name = 'w' + ''.join(random.choice(alphabet) for _ in range(4))  # Перебор рандомом

        # name = 'w' + convert_base(i, to_base = 62) # Перебор по порядку
        # i += 1
        # if i > 14776336: return

        url = "https://listick.ru/share/" + name
        response = requests.request("GET", url)
        if response.status_code != 200:
            #print(name + ' not found')
            continue
        print(name)

        soup = Soup(response.content, "html.parser")
        s = soup.find(class_="content-wrap")

        cont = s.find("img")
        if cont != None:
            r = requests.get("https://listick.ru" + cont['src'], stream = True)
            if r.status_code == 200:
                with open(pv.sanitize_filename(name + ' ' + cont['alt'] + '.' + cont['src'].split('.')[-1]), 'wb') as f:
                    for chunk in r.iter_content(1024):
                        f.write(chunk)
            continue

        cont = s.find(class_="file")
        if cont != None:
            cont = cont.find("a")
            f = open(name + ' ' + cont['title'] + '.url', "w")
            f.write("[InternetShortcut]\nURL=" + "https://listick.ru" + cont['href'])
            f.close()
            continue

        cont = s.find(class_="text-wrap")
        if cont != None:
            t = cont.get_text()

            f = open(pv.sanitize_filename(name + ' ' + t[:20]+'.txt'), "w", encoding="utf-8")
            f.write(t)
            f.close()
            continue


tempVar2 = 1
while (tempVar2 <= threadAmount):
    try:
        print ("Starting thread #" + str(tempVar2))
        threading.Thread(target = scrapePictures).start()
    except:
        print ("Error initializing thread....")
    tempVar2 += 1
        

#Make threads never stop
while (True):
    print ("Checked...." + str(n))
    time.sleep(1)