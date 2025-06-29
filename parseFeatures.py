import re
import socket
import requests
from datetime import datetime
from urllib.parse import urlparse
import whois
import pandas as pd
from bs4 import BeautifulSoup

class ParseFeatures:
    def __init__(self, url):
        self.url = url
        self.parsed_url = urlparse(url)
        self.domain = self.parsed_url.netloc
        self.hostname = self.parsed_url.hostname

    def get_html(self):
        try:
            response = requests.get(self.url, timeout=5)
            return response.text
        except:
            return ""

    def having_ip_address(self):
        match = re.search(r'\d+\.\d+\.\d+\.\d+', self.url)
        return 1 if match else -1

    def url_length(self):
        return -1 if len(self.url) >= 75 else 1

    def shortening_service(self):
        pattern = re.compile(r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.ly|cutt\.ly|u\.to")
        return -1 if re.search(pattern, self.url) else 1

    def having_at_symbol(self):
        return -1 if "@" in self.url else 1

    def double_slash_redirecting(self):
        return -1 if self.url.find('//', 7) != -1 else 1

    def prefix_suffix(self):
        return -1 if '-' in self.domain else 1

    def having_sub_domain(self):
        domain = self.domain
        if domain.startswith("www."):
            domain = domain[4:]
        dots = domain.count('.')
        return -1 if dots > 2 else (0 if dots == 2 else 1)

    def ssl_final_state(self):
        return 1 if self.url.startswith("https") else -1

    def domain_registration_length(self):
        try:
            w = whois.whois(self.domain)
            exp = w.expiration_date
            create = w.creation_date
            if isinstance(exp, list): exp = exp[0]
            if isinstance(create, list): create = create[0]
            if exp and create:
                days = (exp - create).days
                return 1 if days > 365 else -1
        except:
            pass
        return -1

    def favicon(self):
        html = self.get_html()
        return 1 if "favicon" in html else -1

    def port(self):
        try:
            socket.create_connection((self.domain, 80), timeout=2)
            return 1
        except:
            return -1

    def https_token(self):
        return -1 if "https" in self.domain.replace("https", "") else 1

    def request_url(self):
        html = self.get_html()
        soup = BeautifulSoup(html, 'html.parser')
        total = len(soup.find_all('img')) + len(soup.find_all('video')) + len(soup.find_all('audio'))
        external = 0
        for tag in soup.find_all(['img', 'video', 'audio']):
            src = tag.get('src')
            if src and not self.domain in src:
                external += 1
        return -1 if total != 0 and external / total >= 0.61 else 1

    def url_of_anchor(self):
        html = self.get_html()
        soup = BeautifulSoup(html, 'html.parser')
        anchors = soup.find_all('a')
        unsafe = 0
        total = len(anchors)
        for tag in anchors:
            href = tag.get('href')
            if href and not self.domain in href:
                unsafe += 1
        return -1 if total != 0 and unsafe / total >= 0.67 else 1

    def links_in_tags(self):
        html = self.get_html()
        soup = BeautifulSoup(html, 'html.parser')
        metas = soup.find_all('meta')
        links = soup.find_all('link')
        scripts = soup.find_all('script')
        total = len(metas) + len(links) + len(scripts)
        unsafe = 0
        for tag in links + metas + scripts:
            src = tag.get('src') or tag.get('href')
            if src and not self.domain in src:
                unsafe += 1
        if total == 0:
            return 0
        return -1 if unsafe / total >= 0.61 else 1

    def sfh(self):
        html = self.get_html()
        soup = BeautifulSoup(html, 'html.parser')
        forms = soup.find_all('form')
        for form in forms:
            action = form.get('action')
            if action == "" or action == "about:blank" or (action and not self.domain in action):
                return -1
        return 1

    def submitting_to_email(self):
        html = self.get_html()
        return -1 if re.search(r"mailto:", html) else 1

    def abnormal_url(self):
        try:
            w = whois.whois(self.url)
            if isinstance(w.domain_name, list):
                return 1 if self.hostname in w.domain_name else -1
            else:
                return 1 if w.domain_name and self.hostname in w.domain_name else -1
        except:
            return -1

    def redirect(self):
        try:
            r = requests.get(self.url, timeout=5)
            return 1 if len(r.history) <= 1 else 0
        except:
            return -1

    def on_mouseover(self):
        html = self.get_html()
        return -1 if re.search("onmouseover", html, re.IGNORECASE) else 1

    def right_click(self):
        html = self.get_html()
        return -1 if re.search("event.button ?== ?2", html) else 1

    def popup_window(self):
        html = self.get_html()
        return -1 if re.search("alert\(", html) else 1

    def iframe(self):
        html = self.get_html()
        return -1 if "<iframe" in html.lower() else 1

    def age_of_domain(self):
        try:
            w = whois.whois(self.url)
            created = w.creation_date
            if isinstance(created, list):
                created = created[0]
            age = (datetime.now() - created).days
            return 1 if age > 180 else -1
        except:
            return -1

    def dns_record(self):
        try:
            socket.gethostbyname(self.domain)
            return 1
        except:
            return -1

    def web_traffic(self):
        try:
            response = requests.get(f"https://www.similarweb.com/website/{self.domain}", headers={"User-Agent": "Mozilla/5.0"})
            return 1 if response.status_code == 200 else -1
        except:
            return -1

    def page_rank(self):
        return -1  # Still requires reliable API

    def google_index(self):
        try:
            response = requests.get(f"https://www.google.com/search?q=site:{self.url}", headers={"User-Agent": "Mozilla/5.0"})
            return 1 if "did not match any documents" not in response.text else -1
        except:
            return -1

    def links_pointing_to_page(self):
        return -1  # Placeholder (no reliable public API)

    def statistical_report(self):
        try:
            blacklist = ["phishtank.com", "spamhaus.org", "malwaredomainlist.com"]
            for bl in blacklist:
                if bl in self.url:
                    return -1
            return 1
        except:
            return 1

    def extract_all(self):
        features = [
            self.having_ip_address(),
            self.url_length(),
            self.shortening_service(),
            self.having_at_symbol(),
            self.double_slash_redirecting(),
            self.prefix_suffix(),
            self.having_sub_domain(),
            self.ssl_final_state(),
            self.domain_registration_length(),
            self.favicon(),
            self.port(),
            self.https_token(),
            self.request_url(),
            self.url_of_anchor(),
            self.links_in_tags(),
            self.sfh(),
            self.submitting_to_email(),
            self.abnormal_url(),
            self.redirect(),
            self.on_mouseover(),
            self.right_click(),
            self.popup_window(),
            self.iframe(),
            self.age_of_domain(),
            self.dns_record(),
            self.web_traffic(),
            self.page_rank(),
            self.google_index(),
            self.links_pointing_to_page(),
            self.statistical_report(),
        ]
        return features
