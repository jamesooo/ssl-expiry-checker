## description
this script will send an email to a defined email address when ssl certs enumerated in the domains file are going to expire
## example
`EMAIL_ADDRESS=joneal@x.org SENDGRID_API_KEY=abc123 python ssl_expiry_checker.py`
## note
to run on cron make sure to install pip dependencies globally by running `sudo -H pip install -r {{install path}}/requirements.txt`
