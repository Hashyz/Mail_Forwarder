import requests,json

class MailReceiver:
  def __init__(self,name,domainName):
    self.rateLimit = 0
    self.name = name
    self.domainName = domainName

  def getMailID(self):
    url = 'https://www.1secmail.com/api/v1/?action=getMessages&login={}&domain={}'.format(self.name,self.domainName)
    mailID = requests.get(url)
    id = json.loads(mailID.text)
    if id == []:
      self.rateLimit += 1
      if self.rateLimit > 10:
        self.rateLimit = 0
        return False
      return self.getMailID()
    else:
      return id#[0]['id']

  def checkMail(self,confirmId):
    mailUrl = 'https://www.1secmail.com/api/v1/?action=readMessage&login={}&domain={}&id={}'.format(self.name,self.domainName,confirmId)
    confirmCode = requests.get(mailUrl)
    body = json.loads(confirmCode.text)
    html = body['body']
    return html

  def deleteMail(self):
    deleteUrl = "https://www.1secmail.com/mailbox"
    deleteData = {"action": "deleteMailbox",
                  "login": self.name,
                  "domain": self.domainName}

    requests.post(deleteUrl,deleteData)

if __name__ == "__main__":
  tempMail = "xxxxx@1secmail.org"

  name = tempMail.split("@")[0]
  domainName = tempMail.split("@")[1]

  m = MailReceiver(name,domainName)

  lis = m.getMailID()

  res = [i for i in lis if i["from"] == "xxxxx@gmail.com"][0]['id']

  # res = m.getMailID()
  if res != False:
    confirmId = res[0]['id']
    print(confirmId)
    html = m.checkMail(confirmId)
    print(html)
  else:
    print("Mail not found!")

  # m.deleteMail()
