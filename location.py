import urllib.request 
import ssl

def give_region():
    ssl._create_default_https_context = ssl._create_unverified_context
    data = urllib.request.urlopen('https://ipinfo.io').read().decode()
    for i in range(len(data)):
        if data[i:i+8] == '"region"':
            cur_idex = i + 11
            region = ''
            while data[cur_idex] != '"':
                region += data[cur_idex]
                cur_idex += 1
            return region
print(give_region())
