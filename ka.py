from ckanapi import RemoteCKAN
import urllib

filedir = "files-ka"
downloadCsv = False
downloadPdf = False
downloadJson = True
downloadOther = False
downloadBase = "karlsruhe.de"


def loadUrl(p,u):
    """ load file from url, print 404 error or raise"""
    f = filedir + "/" + p + "_" + u[u.rfind("/")+1:]
    try:
        urllib.request.urlretrieve(u,f)
    except urllib.error.HTTPError as err:
        if err.code == 404:
            print("URL not found: ",u)
        else:
            raise

#########

ka = RemoteCKAN('https://transparenz.karlsruhe.de/')
pkgs = ka.action.package_list()
print("Packages:\n",pkgs)

grps = ka.action.group_list()
print("Groups:\n",grps)

for p in pkgs:
    pk = ka.action.package_show(id=p)
    print("\n\nPackage ",p,":\n")
    
    u = pk.get("url")
    if None != u and u != "":
        print("Url:", u)
        
    r = pk.get("resources")
    if None != r:
        for rr in r:
            ru = rr.get("url")
            rm = rr.get("mimetype")
            # check and skip external urls
            if ru.find(downloadBase) < 0:
                print("External url: ",ru,", type ",rm)
                continue

            if None != ru and None != rm  and "csv" in rm.lower():
                print("Resource type ",rm,", url:\n",ru)
                if downloadCsv:
                    loadUrl(p,ru)
            elif None != ru and None != rm  and "json" in rm.lower():
                print("Resource type ",rm,", url:\n",ru)
                if downloadJson:
                    loadUrl(p,ru)
            elif None != ru and None != rm  and "pdf" in rm.lower():
                print("Resource type ",rm,", url:\n",ru)
                if downloadPdf:
                    loadUrl(p,ru)
            elif None != ru:
                print("Other resource url:\n",ru,", type ",rm)
                # check pdf without mimetype
                if ".pdf" == ru[-4:].lower():
                    if downloadPdf:
                        loadUrl(p,ru)
                elif downloadOther:
                    loadUrl(p,ru)

    
