import urllib
import urllib2
import json
import time

### Cooops key
# AIzaSyBQLYjFS54lmPrIl2P0mCZ2h21pSdXBivI

### My key
# AIzaSyBDMRlHkKNzsVMVUUcsajKgU6K3URJfu3k

### Dotun Key
# AIzaSyCSH3RvIURBhOBJJBrorm5Lc8AjsiNu2Q8
params = {
        'q': 'GUNTER SCHLIERKAMP',
        'num': 10, # range 1 to 8
        'start': 1,
        'key' : "AIzaSyBDMRlHkKNzsVMVUUcsajKgU6K3URJfu3k",
        'cx' : '014326078567566203289:jbmph5cj2ue',
        'searchType': 'image',
        "imgColorType": 'color'
}

BASE_URL = "https://www.googleapis.com/customsearch/v1?"

seenUrls = set()
with open("urls.txt","r") as seenFile:
    seenUrls = set(seenFile.readlines())
print("# seen urls",len(seenUrls))

searchTerms = ["Arnold Schwarzenegger bodybuilding","phil health bodybuilding", \
"franco columbo bodybuilding","Murli Kumar bodybuilding", "Suhas Khamkar bodybuilding","flex wheeler bodybuilding" \
"ronnie coleman bodybuilding", "kevin levrone bodybuilding","jay cutler bodybuilding", "matt ogus bodybuilding"]
searchDepth = 3

for term in searchTerms:
    params['q'] = term
    params['start'] = 1
    for i in range(searchDepth):
        
        SEARCH_URL = BASE_URL+ urllib.urlencode(params)
        print("starting iter:",i)
        imgUrls = []

        def parse(response):
            response = json.load(response)
            # print(type(response))
            # print(response.keys())
            # print("\n \n got response keys \n",response.keys())
            for result in response['items']:
                # print(result)
                imgUrls.append((result["title"],result["link"]))


        response = urllib2.urlopen(SEARCH_URL)
        parse(response)

        print("got images: ",len(imgUrls))

        # Download Images
        count = params['start']
        for title,link in imgUrls:
            if link not in seenUrls:
                savePath = "./buff/"+params["q"].replace(" ","_")+"-"+str(count)+".jpg"
                try:
                    urllib.urlretrieve(link, savePath)
                except Exception as e:
                    print("caught exception",e,"\n \n ")
            count+=1
            print("retrieved: ",count,link)
            seenUrls.add(link)
        params['start'] += params['num']
        time.sleep(.5)

with open("urls.txt","w") as updatedSeen:
    for url in seenUrls:
        updatedSeen.write(url+"\n")

