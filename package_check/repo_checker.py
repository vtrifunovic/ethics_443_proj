import re
import requests
import time
from bs4 import BeautifulSoup
from checker_utils.pycolors import printc

class RepoCheck:
    def __init__(self):
        pass

    def _handle_response_codes(self, response, url):
        if response.status_code == 200:
            printc("[  OK  ]", fore="black", back="green")
            return 1
        if response.status_code == 429:
            printc("[ WAIT ]", fore="black", back="yellow", end=" ")
            time.sleep(int(response.headers["Retry-After"]))
            return self.check_repo(url)
        if response.status_code > 500:
            printc("[ERROR!]", fore="black", back="red")
            raise RuntimeError(f"Server for repo {url} is down")
        if response.status_code > 400:
            printc("[ FAIL ]", fore="black", back="red")
            return None
        return None

    def _check_host(self, url):
        url = re.sub(r"https*://", "", url)
        url = url.split("/")[0]
        if url == "github.com":
            return 0
        return 1
    
    def _handle_inner_avoids(self, avoid, action, license, url):
        for a in avoid:
            if re.search(a, license):
                if action == "warn":
                    printc("[WARNING!]", fore="black", back="yellow", style="invert", end=" ")
                    print(f"{url} is under {license}")
                if action == "error":
                    raise TypeError(f"{url} is under {license}")


    def check_repo(self, url, avoid=None, action="warn"):
        response = requests.get(url)
        print(f"Checking:", end=" ")
        printc(url[:50], fore="pink", end=" "*(51-len(url)) )
        if not self._handle_response_codes(response, url):
            return "Check url again"
        soup = BeautifulSoup(response.text, "html.parser")
        # i know these aren't divs anymore, but that was my original
        # search and the variable name stayed
        divs = []
        if self._check_host(url):
            divs = soup.find_all("span", {"class":"project-stat-value"})
        else:
            divs = soup.find_all("a", {"data-analytics-event":"""{"category":"Repository Overview","action":"click","label":"location:sidebar;file:license"}"""})
        if len(divs) < 1:
            return None
        div = divs[0].text.strip()
        if avoid:
            self._handle_inner_avoids(avoid, action, div, url)
        if div == "LICENSE": 
            return "Custom"
        if div == "View license":
            return "Custom"
        return div

    def _clean_url(self, url):
        url = re.sub(r"https*://", "", url)
        return url.split("/", 1)[1]
    
    def check_repos(self, url_list, avoid=None, action="warn"):
        repo_dict = {}
        for url in url_list:
            repo_name = self._clean_url(url)
            repo_dict[repo_name] = self.check_repo(url, avoid=avoid, action=action)
        return repo_dict
    
    def display_licenses(self, repo_dict, avoid=None):
        for k, v in repo_dict.items():
            print(k[:40], end=" "*(41-len(k)))
            issue = 0
            if avoid:
                for a in avoid:
                    if v and re.findall(a, v, flags=re.I):
                        issue += 1
                    if not v:
                        issue -= 1
                if issue > 0:
                    printc(v, fore="red")
                elif issue < 0:
                    printc(v, fore="yellow")
                elif v == "Check url again" or v == "Custom":
                    printc(v, fore="yellow")
                else:
                    printc(v, fore="green")
            else:
                print(v)

if __name__ == "__main__":
    avoid = ["GPL", "GNU General Public", "LGPL", "Lesser GNU"]
    rc = RepoCheck()
    f = open("urls.txt", "r")
    urls = f.readlines()
    urls = [u.strip() for u in urls]
    f.close()
    val = rc.check_repos(urls)
    # Uncomment below line to see how it would handle if imported as a class
    #val = rc.check_repos(urls, avoid=avoid, action="warn")
    rc.display_licenses(val, avoid=avoid)