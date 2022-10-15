import urllib.request 
def give_region():
    data = urllib.request.urlopen('https://ipinfo.io').read().decode()
    for i in range(len(data)):
        if data[i:i+8] == '"region"':
            cur_idex = i + 11
            region = ''
            while data[cur_idex] != '"':
                region += data[cur_idex]
                cur_idex += 1
            return region
