import base64,hashlib,gzip,urllib.request as urllib2,random,zlib,time
from itertools import cycle

u = "getGJUsers20"
ui = "getGJUserInfo20"
ufr = "uploadFriendRequest20"
msg = "uploadGJMessage20"
com = "uploadGJComment21"
delcom = "deleteGJComment20"
dlvl = "downloadGJLevel22"
chist = "getGJCommentHistory"
r = "accounts/registerGJAccount"
l = "uploadGJLevel21"
log = "accounts/loginGJAccount"
s = "updateGJUserScore22"
li = "likeGJItem211"
def urlopen(url,p):
	t = urllib2.Request(url,p)
	ip = ".".join(str(random.randint(0, 255)) for _ in range(4))
	t.add_header('X-FORWARDED-FOR', ip)
	t.add_header('CLIENT-IP',ip)
	return urllib2.urlopen(t)
    
def Post(url,params):
    if "/" in url:
        return urlopen("http://162.216.16.96/database/"+url+".php",str(params+"&secret=Wmfv3899gc9").encode()).read().decode()
    return urlopen("http://162.216.16.96/database/"+url+".php",str("gameVersion=21&binaryVersion=35&gdw=0&"+params+"&secret=Wmfd2893gb7").encode()).read().decode()

def xor(data,key):
    return base(''.join(chr(ord(x) ^ ord(y)) for (x,y) in zip(data, cycle(key))))

def ungjp(d):
        return unxor(d,"37526")

def unxor(d,k):
        return decodeb64(xor(str(decodeb64(d).decode("iso-8859-1")),k)).decode("iso-8859-1")
def base(data):
    return base64.b64encode(data.encode()).decode()
    
def convertinfo(type1,type2,value1):
    if type2=="n":
        r=1
    elif type2=="a":
        r=21
    elif type2=="u":
        r=3
    if type1=="n" or type1=="u":
        h=u
        p="str=%s&total=0&page=0"
    else:
        h=ui
        p="accountID=0&gjp=&targetAccountID=%s"
    return Post(h,p % (value1)).split(":")[r]

def decodeb64(data):
    missing_padding = len(data) % 4
    if missing_padding != 0:
        data += '='* (4 - missing_padding)
    return base64.b64decode(data,"-_")

def makechk(data, key):
    return xor(hashlib.sha1(data.encode()).hexdigest(), key)

def friendreq(user,password,dest,comment):
    return Post(ufr, "accountID=%s&gjp=%s&toAccountID=%s&comment=%s" % (convertinfo("n","a",user),xor(password,"37526"),convertinfo("n","a",dest),base(comment)))

def sendmsg(user,password,dest,subject,body):
    return Post(msg, "accountID=%s&gjp=%s&toAccountID=%s&subject=%s&body=%s" % (convertinfo("n","a",user),xor(password,"37526"),convertinfo("n","a",dest),base(subject),xor(body,"14251")))

def postcomment(user,password,comment,levelid,percent):
    return Post(com, "accountID=%s&gjp=%s&userName=%s&comment=%s&levelID=%s&percent=%s&chk=%s" % (convertinfo("n","a",user),xor(password,"37526"),user,base(comment),levelid,percent,makechk("%s%s%s%s0xPT6iUrtws0J"%(user,base(comment),levelid,percent),"29481")))

def postcommentaccid(accid,user,password,comment,levelid,percent):
    return Post(com, "accountID=%s&gjp=%s&userName=%s&comment=%s&levelID=%s&percent=%s&chk=%s" % (accid,xor(password,"37526"),user,base(comment),levelid,percent,makechk("%s%s%s%s0xPT6iUrtws0J"%(user,base(comment),levelid,percent),"29481")))

def decodelvl(lvl):
    return gzip.decompress(decodeb64(lvl)) if lvl[0:3] == "H4s" else zlib.decompress(decodeb64(lvl))

def downloadlevel(levelid):
    str1 = decodelvl(Post(dlvl, "accountID=0&gjp=&udid=S15212864471883312752224026790081311001&uuid=0&levelID=%s&inc=1&extras=0&rs=wuss&chk=%s"%(levelid,makechk("%s1wuss08D78541C-A4A1-48E6-A2C6-C148F4B615340xI25fpAapCQg"%(str(levelid)),"41274"))).split(":")[7].replace("-","+").replace("_","/"))
    open('output.txt', 'wb').write(str1)
    return 1

def delcomment(user,password,commentid):
    return Post(delcom,"accountID=%s&gjp=%s&commentID=%s" % (convertinfo("n","a",user),xor(password,"37526"),commentid))

##TODO: make this function work
##def getusercomments(user):
##    r = Post(chist,"page=0&total=0&mode=0&userID=%s" % (convertinfo("n", "u", user)))
##    count = r.count("|")
##    strid = ""
##    while count != 0:
##        strid+=r.split("|")[count-(count-1)].split("~")[13].split(":")[0]+"|"+decodeb64(str(r.split("|")[count-(count-1)].split("~")[1]))
##        count-=1
##    return strid

def getDaily():
    return Post(dlvl,"accountID=0&gjp=&udid=8D78541C-A4A1-48E6-A2C6-C148F4B61534&uuid=89485612&levelID=-1&inc=1&extras=0","&rs=7ggVP27IhQ&chk=UgFRUgwFUwIGAVVVCgNQUgcAVVZVBwJVBlEGClMCAggBUw1XAlEEAw==").split(":")[1]

def register(user,password,email):
    return Post(r,"userName=%s&password=%s&email=%s"%(user,password,email))

def uploadlevel(username,password,lvlname,description,levelstring):
    data = base64.b64encode(gzip.compress(levelstring.encode(),compresslevel=6),b"-_")
    levelstring = data.replace(data[4:13],b"AAAAAAAAC").decode()
    seed2=""
    if len(levelstring)< 49:
        seed2 = levelstring
    else:
        for i in range(50):
            seed2 += str(levelstring[int(len(levelstring) // 50 * i)])
    print(seed2)
    print(hashlib.sha1(seed2.encode()+b"xI25fpAapCQg").hexdigest())
    seed2 = xor(hashlib.sha1(seed2.encode()+b"xI25fpAapCQg").hexdigest(),"41274")
    return Post(l,"accountID=%s&gjp=%s&userName=%s&levelID=0&levelName=%s&levelDesc=%s&levelVersion=0&levelLength=0&audioTrack=-1&auto=0&password=&original=0&twoPlayer=0&songID=0&objects=33000&coins=0&requestedStars=0&unlisted=0&wt=24&wt2=0&extraString=0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0&seed=gUmgKRJgsU&seed2=%s&levelString=%s&levelInfo=H4sIAAAAAAAACzPUMzW1NrAGAB3_mUYHAAAA"%(convertinfo("n","a",username),xor(password,"37526"),username,lvlname,base(description),seed2,levelstring))

def login(username,password):
    return Post(log,"udid=335D6026-4E64-41C9-8D2F-3DDC42F2B348&userName=%s&password=%s&sID=76561197960267366"%(username,password))

def stathack(user,password,stars,demons,diamonds,coins,usercoins):
    p=str("accountID=%s&gjp=%s&userName=%s&stars=%s&demons=%s&diamonds=%s&icon=1&color1=0&color2=3&iconType=0&coins=%s&userCoins=%s&special=0&gameVersion=21"%(convertinfo("n","a",user),xor(password,"37526"),user,stars,demons,diamonds,coins,usercoins))
    return Post(s,p+str("&accIcon=1&accShip=1&accBall=1&accBird=1&accDart=1&accRobot=1&accGlow=0&accSpider=1&accExplosion=1&seed=%s&seed2=%s"%("niggerfaggot",makechk(str("%s%s%s%s%s01%s111111011xI35fsAapCRg"%(convertinfo("n","a",user),usercoins,demons,stars,coins,diamonds)),"85271"))))

##TODO: more testing
def likeitem(accountid,uuid,itemid,level,udid,password,like,ty,special):
        try:
            return Post(li,"accountID=%s&gjp=%s&udid=%s&uuid=%s&itemID=%s&like=%s&type=%s&special=%s&rs=FlEaPuoMPO&chk=%s"%(accountid,xor(password,"37526"),udid,uuid,itemid,like,ty,special,makechk(str(level+itemid+like+"2FlEaPuoMPO0"+udid+uuid+"ysg6pUrtjn0J"),"58281")))
        except Exception as e:
            print(e)
