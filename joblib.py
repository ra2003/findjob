"""

"""

from sukhoi import MinerEHP, core
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.encoders import encode_base64
from smtplib import SMTP, SMTPRecipientsRefused
from os.path import basename
from urllib import parse
from os.path import expanduser, join, exists
import signal
import json
import re


class MailMiner(MinerEHP):
    """
    Get the Desc/Contact.
    """

    def run(self, dom):
        mail = dom.fst('a', ('class', 'reference external'))
        mail = mail.attr['href'].split(':')[-1]

        desc = dom.fst('div', ('class', 'job-description'))
        data = re.split('\n+', desc.text())
        data = (ind.strip().rstrip() for ind in data)
        data = '\n'.join(data)
        self.append(data)
        self.append(parse.unquote(mail))

class JobMiner(MinerEHP):
    def run(self, dom):
        elems = dom.find('span', ('class', 'listing-company-name'))

        for ind in elems:
            self.append(MailMiner(self.geturl(
                ind.fst('a').attr['href']))) 

        next = dom.fst('ul', ('class', 'pagination menu'))
        next = next.fst('li', ('class', 'next'))
        next = next.fst('a', ('class', ''))

        if not next: return
        URL = 'https://www.python.org/jobs/%s'
        self.next(URL % next.attr['href'])

class FJob:
    def __init__(self, server, port, user, password,
        resume, template):

        self.user     = user
        self.server   = server
        self.port     = port
        self.password = password
        self.resume   = resume
        self.template = template
        self.server   = SMTP(self.server, self.port)
        self.server.ehlo()
        self.server.starttls()
        self.server.ehlo()
         
        self.server.login(self.user, self.password)

        home      = expanduser('~')
        filename  = join(home, 'findjob.json')

        if exists(filename):
            self.load_db(filename)
        else:
            self.db = []

        URL       = 'https://www.python.org/jobs/'
        self.jobs = JobMiner(URL)

        # Process the miners.
        core.gear.mainloop()

        # The amount of jobs that were scrapped.
        print('Found %s jobs' % len(self.jobs))

        # When control-c is pressed just save the contents.
        def handler(*args):
            self.save_db(filename)
            exit(0)
        signal.signal(signal.SIGINT, handler)

        for ind in self.jobs:
            if not ind in self.db:
                self.inform(ind[0], ind[1])
        self.save_db(filename)

    def load_db(self, filename):
        fd      = open(filename, 'r')
        self.db = json.load(fd)
        fd.close()

    def save_db(self, filename):
        fd      = open(filename, 'w')
        json.dump(self.db, fd)
        fd.close()

    def fmt_title(self, desc):
        """
        Make the mail title be about 80 chars containing
        part of the job description.
        """

        title = re.sub('\n+', ' ', desc)
        title = '%s ...' % title[:80]
        return title

    def send_mail(self, desc, contact):
        msg            = MIMEMultipart()
        msg['Subject'] = self.fmt_title(desc)
        msg['From']    = self.user
        msg['To']      = contact
        part           = MIMEBase('application', "octet-stream")

        part.set_payload(open(self.resume, "rb").read())
        encode_base64(part)

        msg.attach(MIMEText(self.template, 'plain'))
        
        part.add_header('Content-Disposition', 
        'attachment; filename="%s"' % basename(self.resume))
        msg.attach(part)

        self.server.sendmail(self.user, 
        contact, msg.as_string())
        self.db.append([desc, contact])

    def inform(self, desc, contact):
        print('#' * 80 + '\n%s' % desc)
        rst = input('Yes/No:')

        if 'y' in rst or 'yes' in rst: 
            try:
                self.send_mail(desc, contact)
            except SMTPRecipientsRefused as e:
                print('Failed to send!', e)



