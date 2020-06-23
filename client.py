from important import *
from module import *
from setup_args import *
from list_def import *
import asyncio

# Login Client
listAppType = ['DESKTOPWIN', 'DESKTOPMAC', 'IOSIPAD', 'CHROMEOS']
try:
    print ('[ System Message ] - *Klien Masuk.')
    client = None
    if args.apptype:
        tokenPath = Path('authToken.txt')
        if tokenPath.exists():
            tokenFile = tokenPath.open('r')
        else:
            tokenFile = tokenPath.open('w+')
        savedAuthToken = tokenFile.read().strip()
        authToken = savedAuthToken if savedAuthToken and not args.token else args.token
        idOrToken = authToken if authToken else print("# No one Qr was readed, Lets Scan New QR.")
        try:
            client = LINE(idOrToken, appType=args.apptype, systemName=args.systemname, channelId=args.channelid, showQr=args.showqr)
            tokenFile.close()
            tokenFile = tokenPath.open('w+')
            tokenFile.write(client.authToken)
            tokenFile.close()
        except TalkException as talk_error:
            if args.traceback: traceback.print_tb(talk_error.__traceback__)
            sys.exit('(+) Error : %s' % talk_error.reason.replace('_', ' '))
        except Exception as error:
            if args.traceback: traceback.print_tb(error.__traceback__)
            sys.exit('(+) Error : %s' % str(error))
    else:
        for appType in listAppType:
            tokenPath = Path('authToken.txt')
            if tokenPath.exists():
                tokenFile = tokenPath.open('r')
            else:
                tokenFile = tokenPath.open('w+')
            savedAuthToken = tokenFile.read().strip()
            authToken = savedAuthToken if savedAuthToken and not args.token else args.token
            idOrToken = authToken if authToken else print("# No one Qr was readed, Lets Scan New QR.")
            try:
                client = LINE(idOrToken, appType=appType, systemName=args.systemname, channelId=args.channelid, showQr=args.showqr)
                tokenFile.close()
                tokenFile = tokenPath.open('w+')
                tokenFile.write(client.authToken)
                tokenFile.close()
                break
            except TalkException as talk_error:
                print ('(+) Error : %s' % talk_error.reason.replace('_', ' '))
                if args.traceback: traceback.print_tb(talk_error.__traceback__)
                if talk_error.code == 1:
                    continue
                sys.exit(1)
            except Exception as error:
                print ('(+) Error : %s' % str(error))
                if args.traceback: traceback.print_tb(error.__traceback__)
                sys.exit(1)
except Exception as error:
    print ('[ System Message ] - Error : %s' % str(error))
    if args.traceback: traceback.print_tb(error.__traceback__)
    sys.exit(1)

if client:
    print ('\n[ Your Auth Token ] -> %s' % client.authToken)
    print ('\n[ Your Timeline Token ] -> %s' % client.tl.channelAccessToken)
    print ('\n[ System Message ] - Berhasil Masuk.')
else:
    sys.exit('[ System Message ] - Gagal Masuk.')

myMid = client.profile.mid
admin = "uac8e3eaf1eb2a55770bf10c3b2357c33"
programStart = time.time()
oepoll = OEPoll(client)
tmp_text = []

settings = livejson.File('setting.json', True, False, 4)

bool_dict = {
    True: ['Yes', 'Aktif', 'Sukses', 'Open', 'On'],
    False: ['No', 'Tidak Aktif', 'Gagal', 'Close', 'Off']
}

#DEFFTEMPLATE
def sendTemplate(to, data):
    helloworld = LiffChatContext(to)
    helloworld = LiffContext(chat=helloworld)
    view = LiffViewRequest('1654177568-wL8RdxDk', helloworld)
    token = client.liff.issueLiffView(view)
    url = 'https://api.line.me/message/v3/share'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer %s' % token.accessToken
    }
    data = {"messages":[data]}
    requests.post(url, headers=headers, data=json.dumps(data))

def helpmessage():
    if settings['setKey']['status'] == True:
        key = settings['setKey']['key'].title()
    else:
        key = ''
    helpMessage ="╭─「 Umum 」─── " + "\n" + \
                    "│ Prefix : " + key + "\n" + \
                    "│ " + key + "Me" + "\n" + \
                    "│ " + key + "Author" + "\n" + \
                    "╰────────────" + "\n" + \
                    "╭─「 Media 」─" + "\n" + \
                    "│ " + key + "Antonym" + "\n" + \
                    "│ " + key + "Apod" + "\n" + \
                    "│ " + key + "Catfacts" + "\n" + \
                    "│ " + key + "Countryinfo" + "\n" + \
                    "│ " + key + "Harrypotter" + "\n" + \
                    "│ " + key + "Ipcheck" + "\n" + \
                    "│ " + key + "Kbbi" + "\n" + \
                    "│ " + key + "Meanslike" + "\n" + \
                    "│ " + key + "Number" + "\n" + \
                    "│ " + key + "Playstore" + "\n" + \
                    "│ " + key + "RandomDate" + "\n" + \
                    "│ " + key + "RandomQuote" + "\n" + \
                    "│ " + key + "RandomYear" + "\n" + \
                    "│ " + key + "Superhero" + "\n" + \
                    "│ " + key + "Surah" + "\n" + \
                    "│ " + key + "Tvchannel" + "\n" + \
                    "│ " + key + "Urbandict" + "\n" + \
                    "│ " + key + "Wikipedia" + "\n" + \
                    "│ " + key + "Ytsearch" + "\n" + \
                    "╰────────────"
    return helpMessage

def executeCmd(msg, text, txt, cmd, msg_id, receiver, sender, to, setKey):

    # // Logouted Bot Device
    if cmd == '@logout device':
      if sender in admin:
        client.sendReplyMessage(msg_id, to, f'Program has been Stopped!\nStopped by {sender.displayName}')
        sys.exit('##----- PROGRAM STOPPED -----##')

    # // Bot Send His Creator Contact
    if cmd == "author":
        client.sendContact(to,"uac8e3eaf1eb2a55770bf10c3b2357c33")

    # // Checking Speed of Bot Send an Message
    elif cmd == 'ping':
      if sender in admin:
        start = time.time()
        client.sendReplyMessage(msg_id, to, 'Authentication...')
        elapse = time.time() - start
        client.sendReplyMessage(msg_id, to, f'Speed Sending Message {str(elapse)} Seconds')
    
    # // Runtime when Program Started
    elif cmd == "runtime":
      if sender in admin:
        timeNow = time.time()
        runtime = timeNow - programStart
        runtime = timeChange(runtime)
        client.sendReplyMessage(msg_id, to, f"Bot Running Time {str(runtime)}")

    # // Restart the Program
    elif cmd == 'relogin':
      if sender in admin:
        client.sendReplyMessage(msg_id, to, 'Please Wait...')
        settings['restartPoint'] = to
        restartProgram()
    
    # // Sends Bot Menu
    if cmd == "menu":
            helpMessage = helpmessage()
            key = setKey.title()
            mids = "uac8e3eaf1eb2a55770bf10c3b2357c33"
            mantap={
                'type': 'text',
                'text': f'  {str(helpMessage)}\nFor Info Using : \n\t{key}info [commands]',
                'sentBy': {
                    'label': 'Reighpuy',
                    'iconUrl' : "https://pbs.twimg.com/profile_images/1164752786992484354/PyFcqmzG_400x400.jpg",
                    'linkUrl' : 'https://line.me/ti/p/~yapuy'
                }
            }
            sendTemplate(to, mantap)

    # // Bot Send Profile Of Sender
    if cmd == "me":
        paramz = client.getContact(sender)
        isi = "╭───「 Profile Info 」"
        isi += "\n│"
        isi += "\n│ • y'mid : " + paramz.mid
        isi += "\n│ • y'name : " + paramz.displayName
        isi += "\n│ • y'bio : " + paramz.statusMessage
        isi += "\n│"
        isi += "\n╰────────────"
        client.sendReplyMessage(msg_id,to, isi)

                   # // MEDIA STARTING // #

    # KBBI
    elif cmd.startswith("kbbi "):
      try:
        title = removeCmd(text)
        data = KBBI(title)
        result = "╭──[ KBBI ]"
        result += f"\n├ Title : {str(title)}"
        result += "\n╰──────────"
        result += f"\n\n-> Result : \n{str(data.__str__(contoh=False))}"
        client.sendReplyMessage(msg_id, to, str(result))
      except Exception as error:
          client.sendReplyMessage(msg_id, to, "# Failed, {} Not Found.".format(judul))
          logError(error)

    # MEANS LIKE
    elif cmd.startswith("meanslike "):
      try:
         process = msg.text.split(" ")
         ordered = msg.text.replace(process[0] + " ","")
         req = requests.get(f"https://api.datamuse.com/words?ml={str(ordered)}")
         data = req.text
         data = json.loads(data)
         results = f"1) : {str(data[0]['word'])}"
         results += f"\n2) : {str(data[1]['word'])}"
         results += f"\n3) : {str(data[2]['word'])}"
         results += f"\n4) : {str(data[3]['word'])}"
         results += f"\n5) : {str(data[4]['word'])}"
         client.sendReplyMessage(msg_id, to, str(results))
      except:client.sendReplyMessage(msg_id, to, f"# Failed : {ordered} Not Found.")

    # WIKIPEDIA
    elif cmd.startswith('wikipedia'):
        textt = removeCmd(text, setKey)
        texttl = textt.lower()
        param1 = sender
        client.findAndAddContactsByMid(param1)
        results = '╭───「 Wikipedia 」'
        results += '\n├'
        results += '\n├ Language : ID'
        results += '\n├ Usage : '
        results += '\n│ • {key}Wikipedia Summary (query)'
        results += '\n│ • {key}Wikipedia Article (countrycode)'
        results += '\n│ • {key}Wikipedia Medialist (query)'
        results += '\n│ • {key}Wikipedia Related (query)'
        results += '\n│ • {key}Wikipedia Randomsum'
        results += '\n├'
        results += '\n╰───「 Reighpuy @HelloWorld 」'
        if cmd == 'wikipedia':
            client.sendReplyMessage(msg_id, to, parsingRes(results).format_map(SafeDict(key=setKey.title())))
        elif texttl.startswith('article '):
          try:
            texts = textt[8:]
            textsl = texts.lower()
            req = requests.get(f"https://id.wikipedia.org/api/rest_v1/data/recommendation/article/creation/translation/{str(textsl)}")
            data = req.text
            data = json.loads(data)
            results = "╭───[ Wikipedia Lang Article ]"
            results += "\n├"
            results += f"\n├ 1) {str(data['items'][0]['title'])}"
            results += f"\n├ 2) {str(data['items'][1]['title'])}"
            results += f"\n├ 3) {str(data['items'][2]['title'])}"
            results += f"\n├ 4) {str(data['items'][3]['title'])}"
            results += f"\n├ 5) {str(data['items'][4]['title'])}"
            results += f"\n├ 6) {str(data['items'][5]['title'])}"
            results += f"\n├ 7) {str(data['items'][6]['title'])}"
            results += f"\n├ 8) {str(data['items'][7]['title'])}"
            results += f"\n├ 9) {str(data['items'][8]['title'])}"
            results += f"\n├ 10) {str(data['items'][9]['title'])}"
            results += f"\n├ 11) {str(data['items'][10]['title'])}"
            results += f"\n├ 12) {str(data['items'][11]['title'])}"
            results += f"\n├ 13) {str(data['items'][12]['title'])}"
            results += f"\n├ 14) {str(data['items'][13]['title'])}"
            results += f"\n├ 15) {str(data['items'][14]['title'])}"
            results += f"\n├ 16) {str(data['items'][15]['title'])}"
            results += f"\n├ 17) {str(data['items'][16]['title'])}"
            results += f"\n├ 18) {str(data['items'][17]['title'])}"
            results += f"\n├ 19) {str(data['items'][18]['title'])}"
            results += f"\n├ 20) {str(data['items'][19]['title'])}"
            results += f"\n├ 21) {str(data['items'][20]['title'])}"
            results += f"\n├ 22) {str(data['items'][21]['title'])}"
            results += f"\n├ 23) {str(data['items'][22]['title'])}"
            results += f"\n├ 24) {str(data['items'][23]['title'])}"
            results += "\n├"
            results += "\n╰───[ Ended ]"
            client.sendReplyMessage(msg_id, to, results)
          except:client.sendReplyMessage(msg_id, to, f"# Failed, {textsl} is Not Found.")
        elif texttl.startswith('summary '):
          try:
            texts = textt[8:]
            textsl = texts.lower()
            req = requests.get(f"https://id.wikipedia.org/api/rest_v1/page/summary/{str(textsl)}?redirect=false")
            data = req.text
            data = json.loads(data)
            results = "╭───[ Wikipedia Summary ]"
            results += "\n├"
            results += "\n├ Title : {}".format(str(data["title"]))
            results += "\n├ Wikibas_item : {}".format(str(data["wikibase_item"]))
            results += "\n├ Lang : {}".format(str(data["lang"]))
            results += "\n├ Description : {}".format(str(data["description"]))
            results += "\n├"
            results += "\n╰───[ Ended ]"
            results += "\n├ Full Desc : {}".format(str(data["extract"]))
            client.sendReplyMessage(msg_id, to, results)
          except:client.sendReplyMessage(msg_id, to, f"# Failed, {textsl} Not Found.")
        elif texttl.startswith('medialist '):
          try:
            texts = textt[10:]
            textsl = texts.lower()
            req = requests.get(f"https://id.wikipedia.org/api/rest_v1/page/media-list/{str(textsl)}?redirect=false")
            data = req.text
            data = json.loads(data)
            results = "╭───[ Wikipedia Medialist ]"
            results += "\n├"
            results += "\n├ Type : {}".format(str(data["items"][0]["type"]))
            results += "\n├ Title : {}".format(str(data["items"][0]["title"]))
            results += "\n├ Caption : {}".format(str(data["items"][0]["caption"]["text"]))
            results += "\n├"
            results += "\n╰───[ Ended ]"
            client.sendReplyMessage(msg_id, to, results)
          except:client.sendReplyMessage(msg_id, to, f"# Failed, {textsl} Not Found.")
        elif texttl.startswith('related '):
          try:
            texts = textt[8:]
            textsl = texts.lower()
            req = requests.get(f"https://id.wikipedia.org/api/rest_v1/page/related/{str(textsl)}")
            data = req.text
            data = json.loads(data)
            results = "╭───[ Wikipedia Related ]"
            results += "\n├"
            results += "\n├ 1) {}".format(str(data["pages"][0]["title"]))
            results += "\n├ 2) {}".format(str(data["pages"][1]["title"]))
            results += "\n├ 3) {}".format(str(data["pages"][2]["title"]))
            results += "\n├ 4) {}".format(str(data["pages"][3]["title"]))
            results += "\n├ 5) {}".format(str(data["pages"][4]["title"]))
            results += "\n├"
            results += "\n╰───[ Ended ]"
            client.sendReplyMessage(msg_id, to, results)
          except:client.sendReplyMessage(msg_id, to, f"# Failed, {textsl} Not Found.")
        elif texttl.startswith('randomsum'):
          try:
            req = requests.get("https://id.wikipedia.org/api/rest_v1/page/random/summary")
            data = req.text
            data = json.loads(data)
            results = "╭───[ Wikipedia Random Summary ]"
            results += "\n├"
            results += "\n├ Title : {}".format(str(data["title"]))
            results += "\n├ Wikibase_item : {}".format(str(data["wikibase_item"]))
            results += "\n├ PageId : {}".format(str(data["pageid"]))
            results += "\n├ Language : {}".format(str(data["lang"]))
            results += "\n├ Description : {}".format(str(data["description"]))
            results += "\n├"
            results += "\n╰───[ Ended ]"
            results += "\nFull Desc : {}".format(str(data["extract"]))
            client.sendReplyMessage(msg_id, to, results)
          except:client.sendReplyMessage(msg_id, to, "# Failed.")

    # HARRYPOTTER
    elif cmd.startswith('harrypotter'):
        textt = removeCmd(text, setKey)
        texttl = textt.lower()
        param1 = sender
        results = '╭───「 Harrypotter 」'
        results += '\n├'
        results += '\n├ Usage : '
        results += '\n│ • {key}Harrypotter Profile (name)'
        results += '\n│ • {key}Harrypotter Charlist'
        results += '\n├'
        results += '\n╰───「 Ended 」'
        if cmd == 'harrypotter':
            client.sendReplyMessage(msg_id, to, parsingRes(results).format_map(SafeDict(key=setKey.title())))
        elif texttl.startswith("profile "):
          try:
            texts = textt[8:]
            textsl = texts.lower()
            req = requests.get(f"https://www.potterapi.com/v1/characters/?key=$2a$10$cO8xUVqBD2LPqRb6sF.Z1uGpDQ0Xv.L.quEnQh6USoxdyjP7v7g/e&name={str(textsl)}")
            data = req.text
            data = json.loads(data)
            results = "╭──「 HarryPotter - Character 」"
            results += "\n├ "
            results += f"\n├ Name : {(str(data[0]['name']))}"
            results += f"\n├ ID : {(str(data[0]['_id']))}"
            results += f"\n├ House : {(str(data[0]['house']))}"
            results += f"\n├ School : {(str(data[0]['school']))}"
            results += f"\n├ Blood Status : {(str(data[0]['bloodStatus']))}"
            results += f"\n├ Species : {(str(data[0]['species']))}"
            results += "\n├"
            results += "\n╰───「 Ended 」"
            mantap={
                'type': 'text',
                'text': f'{str(results)}',
                'sentBy': {
                    'label': 'Harry Potter Characters',
                    'iconUrl' : "https://2.bp.blogspot.com/-DlE53qq9NtA/VlKJORbZbfI/AAAAAAAAFl8/1Ypt2CW4iRQ/s1600/Harry%2BPotter%2Band%2Bsorcerer%2527s%2Bstone.jpg",
                    'linkUrl' : 'http://line.me/ti/p/~yapuy'
                }
            }
            sendTemplate(to, mantap)
          except:client.sendReplyMessage(msg_id,to, f"Failed, {textsl} Not Found.")
        elif texttl.startswith("charlist"):
            client.sendReplyMessage(msg_id,to, "https://github.com/reighpuy/harry_potter_api/blob/master/characters.txt")
    # SUPERHERO
    elif cmd.startswith('superhero'):
      try:
        textt = removeCmd(text, setKey)
        texttl = textt.lower()
        param1 = sender
        client.findAndAddContactsByMid(param1)
        results = '╭───「 Superhero 」'
        results += '\n├'
        results += '\n├ Max Number of Hero : 731'
        results += '\n├ Usage : '
        results += '\n│ • {key}Superhero List'
        results += '\n│ • {key}Superhero Search (name)'
        results += '\n│ • {key}Superhero Num (no)'
        results += '\n│ • {key}Superhero Powerstats (no)'
        results += '\n│ • {key}Superhero Bio (no)'
        results += '\n│ • {key}Superhero Appearance (no)'
        results += '\n│ • {key}Superhero Work (no)'
        results += '\n│ • {key}Superhero Connections (no)'
        results += '\n│ • {key}Superhero Image (no)'
        results += '\n├'
        results += '\n╰───「 Reighpuy @HelloWorld 」'
        if cmd == 'superhero':
            client.sendReplyMessage(msg_id, to, parsingRes(results).format_map(SafeDict(key=setKey.title())))
        elif texttl.startswith('list'):
            client.sendReplyMessage(msg_id,to, "https://github.com/reighpuy/super_hero/blob/master/daftar_super_hero")
        elif texttl.startswith('num '):
            texts = textt[4:]
            textsl = texts.lower()
            r = requests.get(f"https://www.superheroapi.com/api.php/YOUR_API_KEY/{textsl}")
            data = r.text
            data = json.loads(data)
            client.sendReplyMessage(msg_id, to, data["name"])
        elif texttl.startswith('powerstats '):
            texts = textt[11:]
            textsl = texts.lower()
            r = requests.get(f"https://www.superheroapi.com/api.php/YOUR_API_KEY/{textsl}/powerstats")
            data = r.text
            data = json.loads(data)
            results = f"ID : {str(data['id'])}"
            results += f"\nName : {str(data['name'])}"
            results += f"\nIntelligence : {str(data['intelligence'])}"
            results += f"\nStrength : {str(data['strength'])}"
            results += f"\nSpeed : {str(data['speed'])}"
            results += f"\nDurability : {str(data['durability'])}"
            results += f"\nPower : {str(data['power'])}"
            results += f"\nCombat : {str(data['combat'])}"
            client.sendReplyMessage(msg_id, to, results)
        elif texttl.startswith('bio '):
            texts = textt[4:]
            textsl = texts.lower()
            r = requests.get(f"https://www.superheroapi.com/api.php/YOUR_API_KEY/{textsl}/biography")
            data = r.text
            data = json.loads(data)
            results = f"ID : {str(data['id'])}"
            results += f"\nName : {str(data['name'])}"
            results += f"\nFull name : {str(data['full-name'])}"
            results += f"\nAlter egos : {str(data['alter-egos'])}"
            results += f"\nPlace of birth : {str(data['place-of-birth'])}"
            results += f"\nFirst appearance : {str(data['first-appearance'])}"
            results += f"\nPublisher : {str(data['publisher'])}"
            results += f"\nAlignment : {str(data['alignment'])}"
            client.sendReplyMessage(msg_id, to, results)
        elif texttl.startswith('appearance '):
            texts = textt[11:]
            textsl = texts.lower()
            r = requests.get(f"https://www.superheroapi.com/api.php/YOUR_API_KEY/{textsl}/appearance")
            data = r.text
            data = json.loads(data)
            results = f"ID : {str(data['id'])}"
            results += f"\nName : {str(data['name'])}"
            results += f"\nGender : {str(data['gender'])}"
            results += f"\nRace : {str(data['race'])}"
            results += f"\nHeight : {str(data['height'][1])}"
            results += f"\nWeight : {str(data['weight'][1])}"
            results += f"\nEye-color : {str(data['eye-color'])}"
            results += f"\nHair-color : {str(data['hair-color'])}"
            client.sendReplyMessage(msg_id, to, results)
        elif texttl.startswith('work '):
            texts = textt[5:]
            textsl = texts.lower()
            r = requests.get(f"https://www.superheroapi.com/api.php/YOUR_API_KEY/{textsl}/work")
            data = r.text
            data = json.loads(data)
            results = f"ID : {str(data['id'])}"
            results += f"\nName : {str(data['name'])}"
            results += f"\nOccupation : {str(data['occupation'])}"
            results += f"\nBase : {str(data['base'])}"
            client.sendReplyMessage(msg_id, to, results)
        elif texttl.startswith('connections '):
            texts = textt[12:]
            textsl = texts.lower()
            r = requests.get(f"https://www.superheroapi.com/api.php/YOUR_API_KEY/{textsl}/connections")
            data = r.text
            data = json.loads(data)
            results = f"ID : {str(data['id'])}"
            results += f"\nName : {str(data['name'])}"
            results += f"\nGroup affiliation : {str(data['group-affiliation'])}"
            results += f"\nRelatives : {str(data['relatives'])}"
            client.sendReplyMessage(msg_id, to, results)
        elif texttl.startswith('image '):
            texts = textt[6:]
            textsl = texts.lower()
            r = requests.get("https://www.superheroapi.com/api.php/YOUR_API_KEYtextslimage")
            data = r.text
            data = json.loads(data)
            client.sendImageWithURL(to, data["url"])
        elif texttl.startswith("search "):
            texts = textt[7:]
            textsl = texts.lower()
            r = requests.get(f"https://www.superheroapi.com/api.php/YOUR_API_KEY/search/{textsl}")
            data = r.text
            data = json.loads(data)
            results = "╭───[ Superhero Info ]"
            results += f'\n├'
            results += f'\n├ Nama : {data["results-for"]}'
            results += f'\n├ ID : {data["results"][0]["id"]}'
            results += "\n├"
            results += f'\n├ -> Power stats : '
            results += f'\n├ Intelligence : {data["results"][0]["powerstats"]["intelligence"]}'
            results += f'\n├ Strength : {data["results"][0]["powerstats"]["strength"]}'
            results += f'\n├ Speed : {data["results"][0]["powerstats"]["speed"]}'
            results += f'\n├ Durability : {data["results"][0]["powerstats"]["durability"]}'
            results += f'\n├ Power : {data["results"][0]["powerstats"]["power"]}'
            results += f'\n├ Combat : {data["results"][0]["powerstats"]["combat"]}'
            results += f'\n├'
            results += f'\n├ -> Biography : '
            results += f'\n├ Full Name : {data["results"][0]["biography"]["full-name"]}'
            results += f'\n├ Alter egos : {data["results"][0]["biography"]["alter-egos"]}'
            results += f'\n├ Place of-birth : {data["results"][0]["biography"]["place-of-birth"]}'
            results += f'\n├ First appearance : {data["results"][0]["biography"]["first-appearance"]}'
            results += f'\n├ Publisher : {data["results"][0]["biography"]["publisher"]}'
            results += f'\n├ Alignment : {data["results"][0]["biography"]["alignment"]}'
            results += f'\n├'
            results += f'\n├ -> Appearance : '
            results += f'\n├ Gender : {data["results"][0]["appearance"]["gender"]}'
            results += f'\n├ Race : {data["results"][0]["appearance"]["race"]}'
            results += f'\n├ Height : {data["results"][0]["appearance"]["height"][1]}'
            results += f'\n├ Weight : {data["results"][0]["appearance"]["weight"][1]}'
            results += f'\n├ Eye color : {data["results"][0]["appearance"]["eye-color"]}'
            results += f'\n├ Hair color : {data["results"][0]["appearance"]["hair-color"]}'
            results += f'\n├'
            results += f'\n├ -> Work : '
            results += f'\n├ Occupation : {data["results"][0]["work"]["occupation"]}'
            results += f'\n├ Base : {data["results"][0]["work"]["base"]}'
            results += f'\n├'
            results += f'\n├ -> Connections : '
            results += f'\n├ Group affiliation : {data["results"][0]["connections"]["group-affiliation"]}'
            results += "\n├"
            results += "\n╰───[ Reighpuy @HelloWorld ]"
            client.sendReplyMessage(msg_id,to, results)
      except:client.sendReplyMessage(msg_id,to, f"# Failed, Superehero {textsl} Not Found.")

    # get Country Info
    elif cmd.startswith("countryinfo "):
      try:
            process = msg.text.split(" ")
            ordered = msg.text.replace(process[0] + " ","")
            r = requests.get(f"http://countryapi.gear.host/v1/Country/getCountries?pName={str(ordered)}")
            data = r.text
            data = json.loads(data)
            results = f'Name : {str(data["Response"][0]["Name"])}'
            results += f'\nAlpha 2 Code : {str(data["Response"][0]["Alpha2Code"])}'
            results += f'\nAlpha 3 Code : {str(data["Response"][0]["Alpha3Code"])}'
            results += f'\nNative Name : {str(data["Response"][0]["NativeName"])}'
            results += f'\nRegion : {str(data["Response"][0]["Region"])}'
            results += f'\nSub Region : {str(data["Response"][0]["SubRegion"])}'
            mantap={
                'type': 'text',
                'text': '{}'.format(str(results)),
                'sentBy': {
                    'label': f'{str(data["Response"][0]["Name"])}',
                    'iconUrl' : f'{str(data["Response"][0]["FlagPng"])}',
                    'linkUrl' : 'https://line.me/ti/p/~yapuy'
                }
            }
            sendTemplate(to, mantap)
      except:client.sendReplyMessage(msg_id, to,"# Failed : {} Not Found.".format(ordered))

    # Capital of Country
    elif cmd.startswith("capital "):
      try:
        process = msg.text.split(" ")
        ordered = msg.text.replace(process[0] + " ","")
        r = requests.get(f"https://restcountries.eu/rest/v2/alpha/{ordered}")
        data = r.text
        data = json.loads(data)
        client.sendReplyMessage(msg_id,to, f"Capital of `{data['name']}` is `{data['capital']}`")
      except Exception as error:
        client.sendReplyMessage(msg_id,to, f"> Invalid, {ordered} Not Found.")
        logError(error)

    # Region of Country
    elif cmd.startswith("region "):
      try:
        process = msg.text.split(" ")
        ordered = msg.text.replace(process[0] + " ","")
        r = requests.get(f"https://restcountries.eu/rest/v2/alpha/{ordered}")
        data = r.text
        data = json.loads(data)
        client.sendReplyMessage(msg_id,to, f"Region of `{data['name']}` is `{data['region']}`")
      except Exception as error:
        client.sendReplyMessage(msg_id,to, f"> Invalid, {ordered} Not Found.")
        logError(error)

    # Subregion of Country
    elif cmd.startswith("subregion "):
      try:
        process = msg.text.split(" ")
        ordered = msg.text.replace(process[0] + " ","")
        r = requests.get(f"https://restcountries.eu/rest/v2/alpha/{ordered}")
        data = r.text
        data = json.loads(data)
        client.sendReplyMessage(msg_id,to, f"Subregion of `{data['name']}` is `{data['subregion']}`")
      except Exception as error:
        client.sendReplyMessage(msg_id,to, f"> Invalid, {ordered} Not Found.")
        logError(error)

    # Timezones of Country
    elif cmd.startswith("timezone "):
      try:
        process = msg.text.split(" ")
        ordered = msg.text.replace(process[0] + " ","")
        r = requests.get(f"https://restcountries.eu/rest/v2/alpha/{ordered}")
        data = r.text
        data = json.loads(data)
        client.sendReplyMessage(msg_id,to, f"Timezone of `{data['name']}` is `{data['timezones']}`")
      except Exception as error:
        client.sendReplyMessage(msg_id,to, f"> Invalid, {ordered} Not Found.")
        logError(error)

    # Native Name of Country
    elif cmd.startswith("nativename "):
      try:
        process = msg.text.split(" ")
        ordered = msg.text.replace(process[0] + " ","")
        r = requests.get(f"https://restcountries.eu/rest/v2/alpha/{ordered}")
        data = r.text
        data = json.loads(data)
        client.sendReplyMessage(msg_id,to, f"Nativename of `{data['name']}` is `{data['nativeName']}`")
      except Exception as error:
        client.sendReplyMessage(msg_id,to, f"> Invalid, {ordered} Not Found.")
        logError(error)

    # Numberic Code of Country
    elif cmd.startswith("numericcode "):
      try:
        process = msg.text.split(" ")
        ordered = msg.text.replace(process[0] + " ","")
        r = requests.get(f"https://restcountries.eu/rest/v2/alpha/{ordered}")
        data = r.text
        data = json.loads(data)
        client.sendReplyMessage(msg_id,to, f"Numericcode of `{data['name']}` is `{data['numericCode']}`")
      except Exception as error:
        client.sendReplyMessage(msg_id,to, f"> Invalid, {ordered} Not Found.")
        logError(error)

    # Population of Country
    elif cmd.startswith("population "):
      try:
        process = msg.text.split(" ")
        ordered = msg.text.replace(process[0] + " ","")
        r = requests.get(f"https://restcountries.eu/rest/v2/alpha/{ordered}")
        data = r.text
        data = json.loads(data)
        client.sendReplyMessage(msg_id,to, f"Population of `{data['name']}` is `{data['population']}`")
      except Exception as error:
        client.sendReplyMessage(msg_id,to, f"> Invalid, {ordered} Not Found.")
        logError(error)

    # Callingcode of Country
    elif cmd.startswith("callingcode "):
      try:
        process = msg.text.split(" ")
        ordered = msg.text.replace(process[0] + " ","")
        r = requests.get(f"https://restcountries.eu/rest/v2/alpha/{ordered}")
        data = r.text
        data = json.loads(data)
        client.sendReplyMessage(msg_id,to, f"callingcode of `{data['name']}` is `{data['callingCodes']}`")
      except Exception as error:
        client.sendReplyMessage(msg_id,to, f"> Invalid, {ordered} Not Found.")
        logError(error)

    # Currencies Name of Country
    elif cmd.startswith("currenciesname "):
      try:
        process = msg.text.split(" ")
        ordered = msg.text.replace(process[0] + " ","")
        r = requests.get(f"https://restcountries.eu/rest/v2/alpha/{ordered}")
        data = r.text
        data = json.loads(data)
        client.sendReplyMessage(msg_id,to, f"Currencies Name of `{data['name']}` is `{data['currencies'][0]['name']}`")
      except Exception as error:
        client.sendReplyMessage(msg_id,to, f"> Invalid, {ordered} Not Found.")
        logError(error)

    # Currencies Code of Country
    elif cmd.startswith("currenciescode "):
      try:
        process = msg.text.split(" ")
        ordered = msg.text.replace(process[0] + " ","")
        r = requests.get(f"https://restcountries.eu/rest/v2/alpha/{ordered}")
        data = r.text
        data = json.loads(data)
        client.sendReplyMessage(msg_id,to, f"Currencies Code of `{data['name']}` is `{data['currencies'][0]['code']}`")
      except Exception as error:
        client.sendReplyMessage(msg_id,to, f"> Invalid, {ordered} Not Found.")
        logError(error)

    # Currencies Symbol of Country
    elif cmd.startswith("currenciessymbol "):
      try:
        process = msg.text.split(" ")
        ordered = msg.text.replace(process[0] + " ","")
        r = requests.get(f"https://restcountries.eu/rest/v2/alpha/{ordered}")
        data = r.text
        data = json.loads(data)
        client.sendReplyMessage(msg_id,to, f"Currencies Symbol of `{data['name']}` is `{data['currencies'][0]['symbol']}`")
      except Exception as error:
        client.sendReplyMessage(msg_id,to, f"> Invalid, {ordered} Not Found.")
        logError(error)

    # Playstore
    elif cmd.startswith("playstore "):
        try:
            key = setKey.title()
            sep = msg.text.split(" ")
            query =  msg.text.replace(sep[0]+" ","")
            cond = query.split("-")
            search = str(cond[0])
            r = requests.get(f"http://dolphinapi.herokuapp.com/api/playstore?query={search}")
            data = r.text
            data = json.loads(data)
            if len(cond) == 1:
                no = 0
                result = "> {}".format(query.capitalize())
                for anu in data["result"][0:10]:
                    no += 1
                    result += "\n   ({}). {} [{}]".format(str(no), anu["title"], anu["developer"])
                result += f"\nFor Info Using :\n\t`{key}Playstore {query}-[num]`"
                client.sendReplyMessage(msg_id,to, result)
            elif len(cond) == 2:
                try:
                    num = int(cond[1])
                    if num <= len(data["result"]):
                        search = data["result"][num - 1]
                        result = f"Title : {search['title']}"
                        result += f"\nDescription : {search['desc']}"
                        result += f"\nURL : {search['url']}"
                        client.sendImageWithURL(to, f"{search['image']}")
                        client.sendReplyMessage(msg_id,to, result)
                except:client.sendReplyMessage(msg_id,to, "# Failed.")
        except Exception as error:
            print(error)

    # Youtube Search
    elif cmd.startswith("ytsearch "):
        try:
            key = setKey.title()
            sep = msg.text.split(" ")
            query =  msg.text.replace(sep[0]+" ","")
            r = requests.get(f"http://dolphinapi.herokuapp.com/api/music?query={query}")
            data = r.text
            data = json.loads(data)
            no = 0
            result = "> {}".format(query.capitalize())
            for anu in data["result"][0:10]:
                no += 1
                result += "\n   ({}). {} \n\t  URL -> [{}]".format(str(no), anu["title"], anu["url"])
            result += f"\nFor Info Using :\n\t`{key}Searchmusic {query}-[num]`"
            client.sendReplyMessage(msg_id,to, result)
        except Exception as error:
            print(error)

    # Tv Channel
    elif cmd.startswith("tvchannel "):
        try:
            key = setKey.title()
            sep = msg.text.split(" ")
            query =  msg.text.replace(sep[0]+" ","")
            r = requests.get(f"http://dolphinapi.herokuapp.com/api/television?channel={query}")
            data = r.text
            data = json.loads(data)
            no = 0
            result = "> {}".format(query.capitalize())
            for anu in data["result"][0:10]:
                no += 1
                result += "\n   ({}). `{}` [{}]".format(str(no), anu["title"], anu["date"])
            #result += f"\nFor Info Using :\n\t`{key}Tvchannel {query}-[num]`"
            client.sendReplyMessage(msg_id,to, result)
        except Exception as error:
            print(error)

    # Urban dict
    elif cmd.startswith("urbandict "):
      try:
          process = msg.text.split(" ")
          ordered = msg.text.replace(process[0] + " ","")
          r = requests.get("http://urbanscraper.herokuapp.com/search/{}".format(str(ordered)))
          data = r.text
          data = json.loads(data)
          results = "Term : {}".format(str(data[0]["term"]))
          results += "\nDefinisi : {}".format(str(data[0]["definition"]))
          results += "\nContoh : {}".format(str(data[0]["example"]))
          results += "\nAlamat : {}".format(str(data[0]["url"]))
          client.sendReplyMessage(msg_id,to, results)
      except:
          client.sendReplyMessage(msg_id, to,"# Failed : {} Not Found.".format(ordered))

    # ANTONYM
    elif cmd.startswith("antonym "):
      try:
            process = msg.text.split(" ")
            ordered = msg.text.replace(process[0] + " ","")
            r = requests.get("https://api.datamuse.com/words?rel_ant={}".format(str(ordered)))
            data = r.text
            data = json.loads(data)
            results = f"Antonym of {ordered} is {str(data[0]['word'])}"
            client.sendReplyMessage(msg_id, to, str(results))
      except:client.sendReplyMessage(msg_id, to, f"# Failed : {ordered} Not Found.")

    # SURAH AL'QURAN
    elif cmd.startswith("surah "):
      try:
        process = msg.text.split(" ")
        ordered = msg.text.replace(process[0] + " ","")
        r = requests.get(f"https://api.banghasan.com/quran/format/json/surat/{str(ordered)}")
        data = r.text
        data = json.loads(data)
        results = "╭──[ Info Surah ]"
        results += f'\n├\n├ Nomor Surah : {str(data["hasil"][0]["nomor"])}'
        results += f'\n├ Nama Surah : {str(data["hasil"][0]["nama"])}'
        results += f'\n├ Arti Surah : {str(data["hasil"][0]["arti"])}'
        results += f'\n├ Asma : {str(data["hasil"][0]["asma"])}'
        results += f'\n├ Start : {str(data["hasil"][0]["start"])}'
        results += f'\n├ Ayat : {str(data["hasil"][0]["ayat"])}'
        results += f'\n├ Tipe : {str(data["hasil"][0]["type"])}'
        results += f'\n├ Urut : {str(data["hasil"][0]["urut"])}'
        results += f'\n├ Rukuk : {str(data["hasil"][0]["rukuk"])}'
        results += f'\n├\n╰──[ Reighpuy @HelloWorld ]'
        results += f'\n\nKeterangan : \n{str(data["hasil"][0]["keterangan"])}'
        client.sendReplyMessage(msg_id, to, str(results))
      except:client.sendReplyMessage(msg_id, to, f"# Failed : {ordered} Not Found.")

    # RANDOM NASA
    elif cmd == 'apod':
        req = requests.get("https://api.nasa.gov/planetary/apod?api_key=plx64zHKoYUg03rYVT8FqmJrwy3xcKsUaW7GsfHr")
        data = req.text
        data = json.loads(data)
        results = "╭──[ NASA ]"
        results += f'\n├\n├ Title : {str(data["title"])}'
        results += f'\n├ Media Type : {str(data["media_type"])}'
        results += f'\n├ Date : {str(data["date"])}'
        results += f'\n├ Description : {str(data["explanation"])}'
        results += f'\n├\n╰──[ Reighpuy @HelloWorld ]'
        mantap={
            'type': 'text',
            'text': f'{str(results)}',
            'sentBy': {
                'label': 'NASA',
                'iconUrl' : f'{str(data["url"])}',
                'linkUrl' : f'{str(data["hdurl"])}'
            }
        }
        sendTemplate(to, mantap)

    # IP CHECK
    elif cmd.startswith("ipcheck "):
      try:
         process = msg.text.split(" ")
         ordered = msg.text.replace(process[0] + " ","")
         r = requests.get(f"http://apitrojans.herokuapp.com/checkip?ip={str(ordered)}")
         data = r.text
         data = json.loads(data)
         ret_ = '╭──[ Ip Check ]'
         ret_ += f'\n├ IP : {str(data["result"]["ip"])}'
         ret_ += f'\n├ Desimal : {str(data["result"]["decimal"])}'
         ret_ += f'\n├ Hostname : {str(data["result"]["hostname"])}'
         ret_ += f'\n├ ASN : {str(data["result"]["asn"])}'
         ret_ += f'\n├ ISP : {str(data["result"]["isp"])}'
         ret_ += f'\n├ Organisasi : {str(data["result"]["organization"])}'
         ret_ += f'\n├ Tipe : {str(data["result"]["type"])}'
         ret_ += f'\n├ Benua : {str(data["result"]["continent"])}'
         ret_ += f'\n├ Negara : {str(data["result"]["country"])}'
         ret_ += f'\n├ Wilayah : {str(data["result"]["region"])}'
         ret_ += f'\n├ Kota : {str(data["result"]["city"])}'
         ret_ += f'\n╰──[ Reighpuy @HelloWorld ]'
         client.sendReplyMessage(msg_id, to, str(ret_))
      except:client.sendReplyMessage(msg_id, to,"# Failed : {} Not Found.".format(ordered))

    elif cmd.startswith("random quote"):
        req = requests.get("http://apitrojans.herokuapp.com/quotes")
        data = req.text
        data = json.loads(data)
        client.sendReplyMessage(msg_id,to, data["result"]["quotes"])

    # CAT FACTS
    elif cmd == 'cat facts':
        req = requests.get("https://cat-fact.herokuapp.com/facts")
        data = req.text
        data = json.loads(data)
        yup = data["all"]
        random_index = randint(0, len(yup)-1)
        yup2 = yup[random_index]['text']
        client.sendReplyMessage(msg_id, to, yup2)

    # Random Number Story
    elif cmd.startswith("numberinfo "):
      try:
         process = msg.text.split(" ")
         ordered = msg.text.replace(process[0] + " ","")
         req = requests.get(f"http://numbersapi.com/{str(ordered)}?json")
         data = req.text
         data = json.loads(data)
         client.sendReplyMessage(msg_id, to, data["text"])
      except:client.sendReplyMessage(msg_id, to, f"# Failed : {str(ordered)} Not Found.")
    # RANDOM DATE
    elif cmd == 'random date':
      try:
         req = requests.get("http://numbersapi.com/random/date?json")
         data = req.text
         data = json.loads(data)
         client.sendReplyMessage(msg_id,to, data["text"])
      except:client.sendReplyMessage(msg_id, to,"# Failed.")
    # RANDOM YEARS
    elif cmd == 'random year':
      try:
         req = requests.get("http://numbersapi.com/random/year?json")
         data = req.text
         data = json.loads(data)
         client.sendReplyMessage(msg_id,to, data["text"])
      except:client.sendReplyMessage(msg_id, to,"# Failed.")

                   # // MEDIA ENDED // #

    # // SETTINGS // #
    elif cmd.startswith('error'):
        textt = removeCmd(text, setKey)
        texttl = textt.lower()
        cond = textt.split(' ')
        results = '╭───「 Error 」'
        results += '\n│ Usage : '
        results += '\n│ • {key}Error'
        results += '\n│ • {key}Error Logs'
        results += '\n│ • {key}Error Reset'
        results += '\n│ • {key}Error Detail <errid>'
        results += '\n╰───────────'
        if cmd == 'error':
            client.sendReplyMessage(msg_id, to, parsingRes(results).format_map(SafeDict(key=setKey.title())))
        elif cond[0].lower() == 'logs':
            try:
                filee = open('errorLog.txt', 'r')
            except FileNotFoundError:
                return client.sendReplyMessage(msg_id, to, 'No Error Founds.')
            errors = [err.strip() for err in filee.readlines()]
            filee.close()
            if not errors: return client.sendReplyMessage(msg_id, to, 'No Error Founds.')
            results = '╭───「 Error Logs 」'
            results += '\n├ List :'
            parsed_len = len(errors)//200+1
            no = 0
            for point in range(parsed_len):
                for error in errors[point*200:(point+1)*200]:
                    if not error: continue
                    no += 1
                    results += '\n│ %i. %s' % (no, error)
                    if error == errors[-1]:
                        results += '\n╰──────────'
                if results:
                    if results.startswith('\n'): results = results[1:]
                    client.sendReplyMessage(msg_id, to, results)
                results = ''
        elif cond[0].lower() == 'reset':
            filee = open('errorLog.txt', 'w')
            filee.write('')
            filee.close()
            shutil.rmtree('tmp/errors/', ignore_errors=True)
            os.system('mkdir tmp/errors')
            client.sendReplyMessage(msg_id, to, 'Success Clear error logs')
        elif cond[0].lower() == 'detail':
            if len(cond) < 2:
                return client.sendReplyMessage(msg_id, to, parsingRes(results).format_map(SafeDict(key=setKey.title())))
            errid = cond[1]
            if os.path.exists('tmp/errors/%s.txt' % errid):
                with open('tmp/errors/%s.txt' % errid, 'r') as f:
                    client.sendReplyMessage(msg_id, to, f.read())
            else:
                return client.sendReplyMessage(msg_id, to, 'Failed display details error, errorid not valid')
        else:
            client.sendReplyMessage(msg_id, to, parsingRes(results).format_map(SafeDict(key=setKey.title())))

    elif txt.startswith('setkey'):
        textt = removeCmd(text, setKey)
        texttl = textt.lower()
        res = '╭───「 Setting Key 」'
        res += '\n│ Status : ' + bool_dict[settings['setKey']['status']][1]
        res += '\n│ Key : ' + settings['setKey']['key'].title()
        res += '\n│ Usage : '
        res += '\n│ • Setkey'
        res += '\n│ • Setkey <on/off>'
        res += '\n│ • Setkey <key>'
        res += '\n╰──────────'
        if txt == 'setkey':
            client.sendReplyMessage(msg_id, to, parsingRes(res))
        elif texttl == 'on':
            if settings['setKey']['status']:
                client.sendReplyMessage(msg_id, to, 'Gagal mengaktifkan setkey, setkey sudah aktif')
            else:
                settings['setKey']['status'] = True
                client.sendReplyMessage(msg_id, to, 'Berhasil mengaktifkan Setkey.')
        elif texttl == 'off':
            if not settings['setKey']['status']:
                client.sendReplyMessage(msg_id, to, 'Gagal menonaktifkan setkey, setkey sudah dinonaktifkan')
            else:
                settings['setKey']['status'] = False
                client.sendReplyMessage(msg_id, to, 'Berhasil menonaktifkan Setkey.')
        else:
            settings['setKey']['key'] = texttl
            client.sendReplyMessage(msg_id, to, 'Sukses ubah set kunci ke (%s)' % textt)

            # # # # # INFO COMMANDS # # # # 

    # Antonym
    elif cmd == "info antonym".lower():
        key = setKey.title()
        client.sendReplyMessage(msg_id, to, f"Usage : {key}antonym [word]\n\t  Ex : {key}Antonym Bad\n\tWhos can use this Command? : Admin & Non-Admin")

    # Cat Facts
    elif cmd == "info catfacts".lower():
        key = setKey.title()
        client.sendReplyMessage(msg_id, to, f"Usage : {key}cat facts\n\tWhos can use this Command? : Admin & Non-Admin")

    # Country Info
    elif cmd == "info countryinfo".lower():
        key = setKey.title()
        client.sendReplyMessage(msg_id, to, f"Other Information of Country : \n\tex : {key}Capital id\n\tex : {key}Region id\n\tex : {key}Subregion id\n\tex : {key}Timezone id\n\tex : {key}Nativename id\n\tex : {key}Numericcode id\n\tex : {key}Population id\n\tex : {key}Callingcode id\n\tex : {key}Currenciesname id\n\tex : {key}Currenciescode id\n\tex : {key}currenciessymbol id\n\nUsage : {key}Countryinfo [country_code]\n\t  Ex : {key}Countryinfo id\n\tWhos can use this Command? : Admin & Non-Admin")

    # Daily Nasa
    elif cmd == "info apod".lower():
        key = setKey.title()
        client.sendReplyMessage(msg_id, to, f"Usage : {key}Apod\n\tWhos can use this Command? : Admin & Non-Admin")

    # Harrypotter
    elif cmd == "info harrypotter".lower():
        key = setKey.title()
        client.sendReplyMessage(msg_id, to, f"Usage : {key}Harrypotter\n\tWhos can use this Command? : Admin & Non-Admin")

    # Ipcheck
    elif cmd == "info ipcheck".lower():
        key = setKey.title()
        client.sendReplyMessage(msg_id, to, f"Usage : {key}Ipcheck [IP]\n\tWhos can use this Command? : Admin & Non-Admin")

    # Kbbi
    elif cmd == "info kbbi".lower():
        key = setKey.title()
        client.sendReplyMessage(msg_id, to, f"Usage : {key}Kbbi [kata]\n\t  Ex : {key}Kbbi tidur\n\tWhos can use this Command? : Admin & Non-Admin")

    # Meanslike
    elif cmd == "info meanslike".lower():
        key = setKey.title()
        client.sendReplyMessage(msg_id, to, f"Usage : {key}Meanslike [word]\n\t  Ex : {key}Meanslike rose\n\tWhos can use this Command? : Admin & Non-Admin")

    # Number
    elif cmd == "info numberinfo".lower():
        key = setKey.title()
        client.sendReplyMessage(msg_id, to, f"Usage : {key}Numberinfo [number]\n\t  Ex : {key}Number 18\n\tWhos can use this Command? : Admin & Non-Admin")

    # RandomDate
    elif cmd == "info randomdate".lower():
        key = setKey.title()
        client.sendReplyMessage(msg_id, to, f"Usage : {key}Random date\n\tWhos can use this Command? : Admin & Non-Admin")

    # RandomQuote
    elif cmd == "info randomquote".lower():
        key = setKey.title()
        client.sendReplyMessage(msg_id, to, f"Usage : {key}Random Quote\n\tWhos can use this Command? : Admin & Non-Admin")

    # RandomYear
    elif cmd == "info randomyear".lower():
        key = setKey.title()
        client.sendReplyMessage(msg_id, to, f"Usage : {key}Random Year\n\tWhos can use this Command? : Admin & Non-Admin")

    # Superhero
    elif cmd == "info superhero".lower():
        key = setKey.title()
        client.sendReplyMessage(msg_id, to, f"Usage : {key}Superhero\n\tWhos can use this Command? : Admin & Non-Admin")

    # Surah
    elif cmd == "info surah".lower():
        key = setKey.title()
        client.sendReplyMessage(msg_id, to, f"Usage : {key}Surah [nomor]\n\t  Ex : {key}Surah 18\n\tWhos can use this Command? : Admin & Non-Admin")

    # Urbandict
    elif cmd == "info urbandict".lower():
        key = setKey.title()
        client.sendReplyMessage(msg_id, to, f"Usage : {key}Urbandict [word]\n\tWhos can use this Command? : Admin & Non-Admin")

    # Wikipedia
    elif cmd == "info wikipedia".lower():
        key = setKey.title()
        client.sendReplyMessage(msg_id, to, f"Usage : {key}Wikipedia\n\tWhos can use this Command? : Admin & Non-Admin")

    # Ytsearch
    elif cmd == "info ytsearch".lower():
        key = setKey.title()
        client.sendReplyMessage(msg_id, to, f"Usage : {key}ytsearch\n\t Ex : {key}Ytsearch kekeyi\n\tWhos can use this Command? : Admin & Non-Admin")

    # Playstore
    elif cmd == "info playstore".lower():
        key = setKey.title()
        client.sendReplyMessage(msg_id, to, f"Usage : {key}Wikipedia\n\t Ex : {key}Playstore line\n\tWhos can use this Command? : Admin & Non-Admin")

    # Tvchannel
    elif cmd == "info tvchannel".lower():
        key = setKey.title()
        client.sendReplyMessage(msg_id, to, f"Usage : {key}Wikipedia\n\t Ex : {key}Tvchannel antv\n\tWhos can use this Command? : Admin & Non-Admin")

def executeOp(op):
    try:
        #print ('Program Operasi : ( %i ) %s' % (op.type, OpType._VALUES_TO_NAMES[op.type].replace('_', ' ')))
        if op.type == 13:
            if settings['autoJoin']['status'] and myMid in op.param3:
                client.acceptGroupInvitation(op.param1)
                if settings['autoJoin']['reply']:
                    if '@!' not in settings['autoJoin']['message']:
                        client.sendMessage(op.param1, settings['autoJoin']['message'])
                    else:
                        client.sendMentionV2(op.param1, settings['autoJoin']['message'], [op.param2])
        if op.type == 26 or op.type == 25:
            msg      = op.message
            text     = str(msg.text)
            msg_id   = msg.id
            receiver = msg.to
            sender   = msg._from
            to       = sender if not msg.toType and sender != myMid else receiver
            txt      = text.lower()
            cmd      = command(text)
            setKey   = settings['setKey']['key'] if settings['setKey']['status'] else ''
            if text in tmp_text:
                return tmp_text.remove(text)
            if msg.contentType == 0: # Content type is text
                if '/ti/g/' in text and settings['autoJoin']['ticket']:
                    regex = re.compile('(?:line\:\/|line\.me\/R)\/ti\/g\/([a-zA-Z0-9_-]+)?')
                    links = regex.findall(text)
                    tickets = []
                    gids = client.getGroupIdsJoined()
                    for link in links:
                        if link not in tickets:
                            tickets.append(link)
                    for ticket in tickets:
                        try:
                            group = client.findGroupByTicket(ticket)
                        except:
                            continue
                        if group.id in gids:
                            client.sendReplyMessage(msg_id, to, 'Sudah di Grup ' + group.name)
                            continue
                        client.acceptGroupInvitationByTicket(group.id, ticket)
                        if settings['autoJoin']['reply']:
                            if '@!' not in settings['autoJoin']['message']:
                                client.sendReplyMessage(msg_id, to, settings['autoJoin']['message'])
                            else:
                                client.sendMentionV2(to, settings['autoJoin']['message'], [sender])
                        client.sendReplyMessage(msg_id, to, 'Sukses Gabung Grup ' + group.name)
                try:
                    executeCmd(msg, text, txt, cmd, msg_id, receiver, sender, to, setKey)
                except TalkException as talk_error:
                    logError(talk_error)
                    if talk_error.code in [7, 8, 20]:
                        sys.exit(1)
                    client.sendReplyMessage(msg_id, to, '# Failed : ' + str(talk_error))
                except Exception as error:
                    logError(error)
                    client.sendReplyMessage(msg_id, to, '# Failed : ' + str(error))
        elif op.type == 25 or op.type == 25:
            msg      = op.message
            text     = str(msg.text)
            msg_id   = msg.id
            receiver = msg.to
            sender   = msg._from
            to       = sender if not msg.toType and sender != myMid else receiver
            txt      = text.lower()
            if msg.contentType == 0: # Content type is text
                if '/ti/g/' in text and settings['autoJoin']['ticket']:
                    regex = re.compile('(?:line\:\/|line\.me\/R)\/ti\/g\/([a-zA-Z0-9_-]+)?')
                    links = regex.findall(text)
                    tickets = []
                    gids = client.getGroupIdsJoined()
                    for link in links:
                        if link not in tickets:
                            tickets.append(link)
                    for ticket in tickets:
                        try:
                            group = client.findGroupByTicket(ticket)
                        except:
                            continue
                        if group.id in gids:
                            client.sendReplyMessage(msg_id, to, 'I\'m aleady on group ' + group.name)
                            continue
                        client.acceptGroupInvitationByTicket(group.id, ticket)
                        if settings['autoJoin']['reply']:
                            if '@!' not in settings['autoJoin']['message']:
                                client.sendReplyMessage(msg_id, to, settings['autoJoin']['message'])
                            else:
                                client.sendMentionV2(to, settings['autoJoin']['message'], [sender])
                        client.sendReplyMessage(msg_id, to, 'Success join to group ' + group.name)
    except TalkException as talk_error:
        logError(talk_error)
        if talk_error.code in [7, 8, 20]:
            sys.exit(1)
    except KeyboardInterrupt:
        sys.exit('Pesan SIstem : *KEYBOARD INTERRUPT.')
    except Exception as error:
        logError(error)

def runningProgram():
    if settings['restartPoint'] is not None:
        try:
            client.sendMessage(settings['restartPoint'], 'Bot is Online!')
        except TalkException:
            pass
        settings['restartPoint'] = None
    while True:
        try:
            ops = oepoll.singleTrace(count=50)
        except TalkException as talk_error:
            logError(talk_error)
            if talk_error.code in [7, 8, 20]:
                sys.exit(1)
            continue
        except KeyboardInterrupt:
            sys.exit('Pesan SIstem : *KEYBOARD INTERRUPT.')
        except Exception as error:
            logError(error)
            continue
        if ops:
            for op in ops:
                executeOp(op)
                oepoll.setRevision(op.revision)

if __name__ == '__main__':
    print ('Pesan SIstem : *RUNNING THE PROGRAM.\n#################################')
    runningProgram()
