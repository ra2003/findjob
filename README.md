# findjob

A crawler that retrieves jobs from www.python.com/jobs then sends your resume.

You setup your mail server, add an mail template then it helps you to
send your resumes for www.python.org/jobs positions.

The sent emails have subject as the job title and body as the one defined
in the command line through an argument.

**Obs:** For using google gmail you have to enable less secure apps to send mails.

# Install

This crawler was written on top of the Sukhoi Web Crawler https://github.com/untwisted/sukhoi
In order to have findjob installed it is necessary to install its dependencies.

~~~
pip install -r requirements.txt
~~~

Then

~~~
pip install findjob
~~~

# Usage

~~~
[tau@archlinux projects]$ findjob -h
usage: findjob [-h] [-m [SERVER]] [-p [PORT]] [-u [USER]] [-w [PASSWORD]]
               [-r [RESUME]] [-f [TEMPLATE]]

optional arguments:
  -h, --help            show this help message and exit
  -m [SERVER], --server [SERVER]
                        Smtp server.
  -p [PORT], --port [PORT]
                        Smtp server.
  -u [USER], --user [USER]
                        Mail username
  -w [PASSWORD], --password [PASSWORD]
                        Your password.
  -r [RESUME], --resume [RESUME]
                        Your resume.
  -f [TEMPLATE], --file-template [TEMPLATE]
                        Some message.

[tau@archlinux ~]$ findjob -r resume.pdf -u mail@server.com -w password -f '
> Hello, i got interested in this position, i would like to apply.
> It follows my resume.
> '

~~~

You would see something like:

~~~
################################################################################

Job Title
Some title ...

Job Description
Some desc ...

Requirements
Some reqs  ...

Contact Info

Contact: Some contact ..

E-mail contact: Some email ...

Yes/No: 

~~~

Whenever you say 'yes' it sends an mail to the listed contact with your resume.pdf and email subject
as the job title.

After issuing the command it will ask confirmation for sending
your resume to the job position. The jobs that you have applied are 
stored in a json file in ~/findjob.json.


