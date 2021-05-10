#!/usr/bin/python
#CHO @ LIS

import getpass, imaplib, re, email
 
p = re.compile('\d+')

#Optionen setzen 
IMAP_SERVER='imap.gmail.com'
IMAP_PORT=993
IMAP_USERNAME=''
IMAP_PASS=''
QUOTA = 0.9


#funktion check_quota definieren
def check_quota():
 quotaStr = mbox.getquotaroot("INBOX")[1][1][0]
 r = p.findall(quotaStr)
 if float(r[0]) / float(r[1]) >= QUOTA:
  return 0
 else:
  return 1

#wenn kein passwort definiert ist, danach fragen
try:
 IMAP_PASS
except NameError: 
 IMAP_PASS = getpass.getpass()

#verbindung mit dem imap-server
mbox = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
mbox.login(IMAP_USERNAME,IMAP_PASS)

#erstes ueberpruefen der mailbox-quota
quotaStr = mbox.getquotaroot("INBOX")[1][1][0]
r = p.findall(quotaStr)
if r == []:
 print "Unlimited Quota Account"
 r.append(0)
 r.append(0)
print 'Allotted: %f MB'%(float(r[1])/1024)
print 'Used: %f MB'%(float(r[0])/1024)
print "Limit: " + "{:.0%}".format(QUOTA)
percentage_used = float(r[0])/float(r[1])
print "{0:.0f}%".format(percentage_used) + " used"

#wenn mehr in gebrauch sind, als das quota vorgibt
if percentage_used >= QUOTA:
 print "Quota used..."

#inbox auswaehlen
 mbox.select("INBOX")

#in der inbox nach allen nachrichten suchen
 result, data = mbox.uid('search',None,'ALL')
 ids = data[0]
 id_list = ids.split()

#alle message uids durcharbeiten
 for num in id_list:
  result, data = mbox.uid('fetch',num,'(RFC822)')
  rawmail = data[0][1]
  message = email.message_from_string(rawmail)

#aufraeumarbeiten, solange quota erfuellt ist
  if check_quota() == 0:
   print "deleting message no. " + num + " from " + message['Date']
   mbox.uid('STORE',num,'+FLAGS','\\Deleted')
   mbox.expunge()

#ausloggen aus dem imap server 
mbox.logout()



