from important import *
from module import *
from setup_args import *
from list_def import *

# Login Client
listAppType = ['DESKTOPWIN', 'DESKTOPMAC', 'IOSIPAD', 'CHROMEOS']
try:
    #print ('[ System Message ] - *Logedin.')
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
    print ('\n[ Your Auth Token ] -> %s\n' % client.authToken)
    #print ('\n[ Your Timeline Token ] -> %s' % client.tl.channelAccessToken)
    #print (f'\n[ System Message ] - Success Login with Name.')
else:
    sys.exit('[ System Message ] - Login Failed.')

myMid = client.profile.mid
admin = ["uac8e3eaf1eb2a55770bf10c3b2357c33"] # Insert your Mid
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
    helpMessage ="> General" + "\n" + \
                    "Prefix : ( " + key + " )\n\t" + \
                    " (1). Author" + "\n\n" + \
                    " (2). LiffLink" + "\n\n" + \
                    " (3). Me" + "\n\t" + \
                    "> Media" + "\n\t" + \
                    " (1). Dictionary" + "\n\t" + \
                    " (2). Utility"
    return helpMessage

def helpdictionary():
    if settings['setKey']['status'] == True:
        key = settings['setKey']['key'].title()
    else:
        key = ''
    helpDictionary ="> Dictionary Command List" + "\n" + \
                    "Prefix : ( " + key + " )\n\t" + \
                    " (1). Antonym" + "\n\t" + \
                    " (2). Kbbi" + "\n\t" + \
                    " (3). Kindof" + "\n\t" + \
                    " (4). Meanslike" + "\n\t" + \
                    " (5). Popularnouns" + "\n\t" + \
                    " (6). Popularadjective" + "\n\t" + \
                    " (7). Synonym" + "\n\t" + \
                    " (8). Urbandict" + "\n\t" + \
                    " (9). Wikipedia"
    return helpDictionary

def helputility():
    if settings['setKey']['status'] == True:
        key = settings['setKey']['key'].title()
    else:
        key = ''
    helpUtility ="> Utility Command Lists" + "\n" + \
                    "Prefix : ( " + key + " )\n\t" + \
                    " (1). Apod" + "\n\t" + \
                    " (2). Catimage" + "\n\t" + \
                    " (3). Catfacts" + "\n\t" + \
                    " (4). Countryinfo" + "\n\t" + \
                    " (5). Dogimage" + "\n\t" + \
                    " (6). Foximage" + "\n\t" + \
                    " (7). Number" + "\n\t" + \
                    " (8). Playstore" + "\n\t" + \
                    " (9). RandomDate" + "\n\t" + \
                    " (10). RandomQuote" + "\n\t" + \
                    " (11). RandomYear" + "\n\t" + \
                    " (12). Superhero" + "\n\t" + \
                    " (13). Surah" + "\n\t" + \
                    " (14). Tvchannel" + "\n\t" + \
                    " (15). Ytsearch"
    return helpUtility

def executeCmd(msg, text, txt, cmd, msg_id, receiver, sender, to, setKey):

    # // Logouted Bot Device
    if cmd == '@logout device':
      if sender in admin:
        client.sendReplyMessage(msg_id, to, f'Program has been Stopped!\nStopped by {sender.displayName}')
        sys.exit('__Program has been Stopped__')

    # // Bot Send a Creator Contact
    if cmd == "author":
        client.sendContact(to,"uac8e3eaf1eb2a55770bf10c3b2357c33")

    # // Bot 
    if cmd == "lifflink".lower():
        client.sendReplyMessage(msg_id,to, "https://liff.line.me/1654177568-wL8RdxDk")

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

    # MENU
    elif cmd.startswith('menu') or cmd.startswith('help'):
        textt = removeCmd(text)
        texttl = textt.lower()
        helpMessage = helpmessage()
        helpDictionary = helpdictionary()
        helpUtility = helputility()
        key = setKey.title()
        results = f'  {str(helpMessage)}\nUsage : \n\t{key}help [Media_Command_Name]\n\tEx : {key}help dictionary'
        if cmd == 'menu' or cmd == 'help':
            client.sendReplyMessage(msg_id, to, results)
        elif texttl.startswith('dictionary'):
          try:
            client.sendReplyMessage(msg_id, to, str(helpDictionary)+f"\n\nFor Info Using : \n\t{key}Info [command_name]\n\tExample : {key}Info Antonym")
          except:client.sendReplyMessage(msg_id, to, f"# Failed.")
        elif texttl.startswith('utility'):
          try:
            client.sendReplyMessage(msg_id, to, str(helpUtility)+f"\n\nFor Info Using : \n\t{key}Info [command_name]\n\tExample : {key}Info Apod")
          except:client.sendReplyMessage(msg_id, to, f"# Failed.")

    # # // MENU WITH FOOTER
    # if cmd == "menu" or cmd == "help":
    #         helpMessage = helpmessage()
    #         key = setKey.title()
    #         mids = "uac8e3eaf1eb2a55770bf10c3b2357c33"
    #         mantap={
    #             'type': 'text',
    #             'text': f'  {str(helpMessage)}\nUsage : \n\t{key}detail [commands]\n\tEx : {key}detail dictionary',
    #             'sentBy': {
    #                 'label': 'Reighpuy',
    #                 'iconUrl' : "https://pbs.twimg.com/profile_images/1164752786992484354/PyFcqmzG_400x400.jpg",
    #                 'linkUrl' : 'https://line.me/ti/p/~yapuy'
    #             }
    #         }
    #         sendTemplate(to, mantap)

    # // Bot Send Profile Of Sender
    if cmd == "me" or cmd == "myprofile":
        paramz = client.getContact(sender)
        isi = "╭───「 Profile Info 」"
        isi += "\n│"
        isi += "\n│ • y'mid : " + paramz.mid
        isi += "\n│ • y'name : " + paramz.displayName
        isi += "\n│ • y'bio : " + paramz.statusMessage
        isi += "\n│"
        isi += "\n╰────────────"
        client.sendReplyMessage(msg_id,to, isi)

    # // Bot Send Avatar Of Sender
    if cmd == "myava":
        paramz = client.getContact(sender)
        client.sendImageWithURL(to, f"http://dl.profile.line-cdn.net/{paramz.pictureStatus}")
        print(f"http://dl.profile.line-cdn.net/{paramz.pictureStatus}")

                   # // MEDIA STARTING // #

    # AVATAR / DISPLAY PICTURE EDITS
    elif ("rotate " in msg.text):
        key = eval(msg.contentMetadata["MENTION"])
        target = key["MENTIONEES"][0]["M"]
        contact = client.getContact(target)
        client.sendImageWithURL(to, f"https://res.cloudinary.com/demo/image/fetch/w_200/a_-20/http://dl.profile.line-cdn.net/{contact.pictureStatus}")

    elif ("circular " in msg.text):
        key = eval(msg.contentMetadata["MENTION"])
        target = key["MENTIONEES"][0]["M"]
        contact = client.getContact(target)
        client.sendImageWithURL(to, f"https://res.cloudinary.com/demo/image/fetch/w_200,c_fill,r_max/e_trim/http://dl.profile.line-cdn.net/{contact.pictureStatus}")

    elif ("grayscale " in msg.text):
        key = eval(msg.contentMetadata["MENTION"])
        target = key["MENTIONEES"][0]["M"]
        contact = client.getContact(target)
        client.sendImageWithURL(to, f"https://res.cloudinary.com/demo/image/fetch/w_200,e_grayscale/http://dl.profile.line-cdn.net/{contact.pictureStatus}")

    elif ("blur " in msg.text):
        key = eval(msg.contentMetadata["MENTION"])
        target = key["MENTIONEES"][0]["M"]
        contact = client.getContact(target)
        client.sendImageWithURL(to, f"https://res.cloudinary.com/demo/image/fetch/w_200,e_blur:100/http://dl.profile.line-cdn.net/{contact.pictureStatus}")

    elif ("outline " in msg.text):
        key = eval(msg.contentMetadata["MENTION"])
        target = key["MENTIONEES"][0]["M"]
        contact = client.getContact(target)
        warna = ["co_red", "co_yellow", "co_orange", "co_green", "co_purple", "co_white"]
        warna2 = ["co_red", "co_yellow", "co_orange", "co_green", "co_purple", "co_white"]
        client.sendImageWithURL(to, f"https://res.cloudinary.com/demo/image/fetch/w_200,c_scale/e_outline:20:200,{random.choice(warna)}/e_outline:10:200,{random.choice(warna2)}/http://dl.profile.line-cdn.net/{contact.pictureStatus}")

    elif ("shadow " in msg.text):
        key = eval(msg.contentMetadata["MENTION"])
        target = key["MENTIONEES"][0]["M"]
        contact = client.getContact(target)
        warna = ["000000", "FFFFFF", "800000", "808000", "008000", "800080", "008080", "000080"]
        client.sendImageWithURL(to, f"https://res.cloudinary.com/demo/image/fetch/w_200,co_rgb:{random.choice(warna)},e_shadow:50,x_10,y_10/http://dl.profile.line-cdn.net/{contact.pictureStatus}")

    elif ("adjust " in msg.text):
        key = eval(msg.contentMetadata["MENTION"])
        target = key["MENTIONEES"][0]["M"]
        contact = client.getContact(target)
        client.sendImageWithURL(to, f"https://res.cloudinary.com/demo/image/fetch/w_200,e_tint:equalize:80:red:50p:blue:60p:yellow:40p/http://dl.profile.line-cdn.net/{contact.pictureStatus}")

    elif ("recolor " in msg.text):
        key = eval(msg.contentMetadata["MENTION"])
        target = key["MENTIONEES"][0]["M"]
        contact = client.getContact(target)
        warna = ["blue", "red", "green", "white", "black", "orange", "purple", "yellow"]
        client.sendImageWithURL(to, f"https://res.cloudinary.com/demo/image/fetch/w_200,e_tint:equalize:80:red:50p:blue:60p:{random.choice(warna)}:40p/http://dl.profile.line-cdn.net/{contact.pictureStatus}")

    elif ("decopacity " in msg.text):
        key = eval(msg.contentMetadata["MENTION"])
        target = key["MENTIONEES"][0]["M"]
        contact = client.getContact(target)
        client.sendImageWithURL(to, f"https://res.cloudinary.com/demo/image/fetch/w_200,e_oil_paint:4/http://dl.profile.line-cdn.net/{contact.pictureStatus}")

    elif ("oilpaint " in msg.text):
        key = eval(msg.contentMetadata["MENTION"])
        target = key["MENTIONEES"][0]["M"]
        contact = client.getContact(target)
        client.sendImageWithURL(to, f"https://res.cloudinary.com/demo/image/fetch/w_200,e_oil_paint:4/http://dl.profile.line-cdn.net/{contact.pictureStatus}")

    elif ("filter1 " in msg.text):
        key = eval(msg.contentMetadata["MENTION"])
        target = key["MENTIONEES"][0]["M"]
        contact = client.getContact(target)
        client.sendImageWithURL(to, f"https://res.cloudinary.com/demo/image/fetch/w_200,e_sepia/http://dl.profile.line-cdn.net/{contact.pictureStatus}")

    elif ("filter2 " in msg.text):
        key = eval(msg.contentMetadata["MENTION"])
        target = key["MENTIONEES"][0]["M"]
        contact = client.getContact(target)
        client.sendImageWithURL(to, f"https://res.cloudinary.com/demo/image/fetch/w_200,e_simulate_colorblind/http://dl.profile.line-cdn.net/{contact.pictureStatus}")

    elif ("filter3 " in msg.text):
        key = eval(msg.contentMetadata["MENTION"])
        target = key["MENTIONEES"][0]["M"]
        contact = client.getContact(target)
        client.sendImageWithURL(to, f"https://res.cloudinary.com/demo/image/fetch/w_200,e_hue/http://dl.profile.line-cdn.net/{contact.pictureStatus}")

            ######## DICTIONARY MENUS ########
    # Urban dict
    elif cmd.startswith("urbandict "):
      try:
          process = msg.text.split(" ")
          ordered = msg.text.replace(process[0] + " ","")
          r = requests.get("http://urbanscraper.herokuapp.com/search/{}".format(str(ordered)))
          data = r.text
          data = json.loads(data)
          results = f" > Urbandictionary `{ordered.capitalize()}`"
          results += f"\n\tTerm : {str(data[0]['term'])}"
          results += f"\n\tDefinition : {str(data[0]['definition'])}"
          results += f"\n\tSample : {str(data[0]['example'])}"
          results += f"\n\tURL : {str(data[0]['url'])}"
          client.sendReplyMessage(msg_id,to, results)
      except:
          client.sendReplyMessage(msg_id, to,"# Failed : {} Not Found.".format(ordered))

    # ANTONYM
    elif cmd.startswith("antonym "):
        try:
            process = msg.text.split(" ")
            ordered = msg.text.replace(process[0] + " ","")
            cond = ordered.split("-")
            r = requests.get("https://api.datamuse.com/words?rel_ant={}".format(str(ordered)))
            data = r.text
            data = json.loads(data)
            if len(cond) == 1:
                no = 0
                result = f"> Antonym of `{ordered.capitalize()}` :"
                for reighpuy in data:
                    no += 1
                    result += f'\n   ({str(no)}). {reighpuy["word"]} [{reighpuy["score"]}]'
                client.sendReplyMessage(msg_id,to, result+"\n\nNote :\n\tThe Number is a Point of Antonym.")
        except Exception as error:client.sendReplyMessage(msg_id, to, f"# Failed : {ordered} Not Found.\n\tError : {error}")

    # SYNONYM
    elif cmd.startswith("synonym "):
        try:
            process = msg.text.split(" ")
            ordered = msg.text.replace(process[0] + " ","")
            cond = ordered.split("-")
            r = requests.get("https://api.datamuse.com/words?rel_syn={}".format(str(ordered)))
            data = r.text
            data = json.loads(data)
            if len(cond) == 1:
                no = 0
                result = f"> Synonym of `{ordered.capitalize()}` :"
                for reighpuy in data:
                    no += 1
                    result += f'\n   ({str(no)}). {reighpuy["word"]} [{reighpuy["score"]}]'
                client.sendReplyMessage(msg_id,to, result+"\n\nNote :\n\tThe Number is a Point of Synonym.")
        except Exception as error:client.sendReplyMessage(msg_id, to, f"# Failed : {ordered} Not Found.\n\tError : {error}")

    # KINDOF
    elif cmd.startswith("kindof "):
        try:
            process = msg.text.split(" ")
            ordered = msg.text.replace(process[0] + " ","")
            cond = ordered.split("-")
            r = requests.get("https://api.datamuse.com/words?rel_spc={}".format(str(ordered)))
            data = r.text
            data = json.loads(data)
            if len(cond) == 1:
                no = 0
                result = f"> Kind of `{ordered.capitalize()}` :"
                for reighpuy in data:
                    no += 1
                    result += f'\n   ({str(no)}). {reighpuy["word"]} [{reighpuy["score"]}]'
                client.sendReplyMessage(msg_id,to, result+"\n\nNote :\n\tThe Number is a Point of Kindof.")
        except Exception as error:client.sendReplyMessage(msg_id, to, f"# Failed : {ordered} Not Found.\n\tError : {error}")

    # POPULAR NOUNS
    elif cmd.startswith("popularnouns "):
        try:
            process = msg.text.split(" ")
            ordered = msg.text.replace(process[0] + " ","")
            cond = ordered.split("-")
            r = requests.get("https://api.datamuse.com/words?rel_jja={}".format(str(ordered)))
            data = r.text
            data = json.loads(data)
            if len(cond) == 1:
                no = 0
                result = f"> Kind of `{ordered.capitalize()}` :"
                for reighpuy in data:
                    no += 1
                    result += f'\n   ({str(no)}). {reighpuy["word"]} [{reighpuy["score"]}]'
                client.sendReplyMessage(msg_id,to, result+"\n\nNote :\n\tThe Number is a Point of Popular Nouns.")
        except Exception as error:client.sendReplyMessage(msg_id, to, f"# Failed : {ordered} Not Found.\n\tError : {error}")

    # POPULAR ADJECTIVE
    elif cmd.startswith("populadjective "):
        try:
            process = msg.text.split(" ")
            ordered = msg.text.replace(process[0] + " ","")
            cond = ordered.split("-")
            r = requests.get("https://api.datamuse.com/words?rel_jjb={}".format(str(ordered)))
            data = r.text
            data = json.loads(data)
            if len(cond) == 1:
                no = 0
                result = f"> Kind of `{ordered.capitalize()}` :"
                for reighpuy in data:
                    no += 1
                    result += f'\n   ({str(no)}). {reighpuy["word"]} [{reighpuy["score"]}]'
                client.sendReplyMessage(msg_id,to, result+"\n\nNote :\n\tThe Number is a Point of Popular Adjective.")
        except Exception as error:client.sendReplyMessage(msg_id, to, f"# Failed : {ordered} Not Found.\n\tError : {error}")

    # KBBI
    elif cmd.startswith("kbbi "):
      try:
        title = removeCmd(text)
        data = KBBI(title)
        result = " > KBBI"
        result += f"\n\tJudul : `{str(title).capitalize()}`"
        result += f"\n{str(data.__str__(contoh=False))}"
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
         results = f" > Meanslike {ordered}"
         results += f"\n\t1) : {str(data[0]['word'])}"
         results += f"\n\t2) : {str(data[1]['word'])}"
         results += f"\n\t3) : {str(data[2]['word'])}"
         results += f"\n\t4) : {str(data[3]['word'])}"
         results += f"\n\t5) : {str(data[4]['word'])}"
         client.sendReplyMessage(msg_id, to, str(results))
      except:client.sendReplyMessage(msg_id, to, f"# Failed : {ordered} Not Found.")

    # WIKIPEDIA
    elif cmd.startswith('wikipedia'):
        textt = removeCmd(text, setKey)
        texttl = textt.lower()
        param1 = sender
        client.findAndAddContactsByMid(param1)
        results = ' > Wikipedia'
        results += '\nLanguage : ID'
        results += '\n\nUsage : '
        results += '\n\t{key}Wikipedia Summary (Query)'
        results += '\n\t{key}Wikipedia Article (Country_Code)'
        results += '\n\t{key}Wikipedia Medialist (Query)'
        results += '\n\t{key}Wikipedia Related (Query)'
        results += '\n\t{key}Wikipedia Randomsummary'
        if cmd == 'wikipedia':
            client.sendReplyMessage(msg_id, to, results.format_map(SafeDict(key=setKey.title())))
        elif texttl.startswith('article '): # With Country Code | Example : !wikipedia article id
          try:
            texts = textt[8:]
            textsl = texts.lower()
            key = setKey.title()
            sep = textsl.split(" ")
            query =  textsl.replace(sep[0]+" ","")
            cond = query.split("-")
            search = str(cond[0])
            req = requests.get(f"https://id.wikipedia.org/api/rest_v1/data/recommendation/article/creation/translation/{str(search)}")
            data = req.text
            data = json.loads(data)
            if len(cond) == 1:
                no = 0
                result = f"> Wikipedia Related {textsl.upper()} // Founds : {len(data['items'])}\n"
                for reighpuy in data["items"]:
                    no += 1
                    result += f'\n   ({str(no)}). {reighpuy["title"]} | [{reighpuy["wikidata_id"]}]'
                client.sendReplyMessage(msg_id, to, result)
          except:client.sendReplyMessage(msg_id, to, f"# Failed, {textsl} is Not Found.")
        elif texttl.startswith('summary '):
          try:
            texts = textt[8:]
            textsl = texts.lower()
            req = requests.get(f"https://id.wikipedia.org/api/rest_v1/page/summary/{str(textsl)}?redirect=false")
            data = req.text
            data = json.loads(data)
            result = f" > Wikipedia Summary {textsl.capitalize()}"
            result += f"\n\tTitle : {data['title']}"
            result += f"\n\tType : {data['type']}"
            result += f"\n\tPage ID : {int(data['pageid'])}"
            result += f"\n\tWikibase Item : {data['wikibase_item']}"
            result += f"\n\tLanguage : {data['lang']}"
            result += f"\n\tDescription : {data['extract']}"
            client.sendReplyMessage(msg_id,to, result)
          except:client.sendReplyMessage(msg_id, to, f"# Failed, {textsl} Not Found.")
        elif texttl.startswith('medialist '):
          try:
            texts = textt[10:]
            textsl = texts.lower()
            key = setKey.title()
            sep = textsl.split(" ")
            query =  textsl.replace(sep[0]+" ","")
            cond = query.split("-")
            search = str(cond[0])
            req = requests.get(f"https://id.wikipedia.org/api/rest_v1/page/media-list/{str(search)}?redirect=false")
            data = req.text
            data = json.loads(data)
            if len(cond) == 1:
                no = 0
                result = f"> Wikipedia Medialist {textsl.capitalize()} // Founds : {len(data['items'])}\n"
                for reighpuy in data["items"]:
                    no += 1
                    result += f'\n   ({str(no)}). {reighpuy["title"]}'
                result += f"\n\nFor Info Using :\n\t`{key}Wikipedia Medialist {textsl.capitalize()}-[number]`"
                client.sendReplyMessage(msg_id, to, result)
            elif len(cond) == 2:
                try:
                    num = int(cond[1])
                    if num <= len(data["items"]):
                        search = data["items"][num - 1]
                        result = f" > Wikipedia Medialist {query.capitalize()}"
                        result += f"\n\tTitle : {search['title']}"
                        result += f"\n\tType : {search['type']}"
                        result += f"\n\tDescription : {search['caption']['text']}"
                        #client.sendImageWithURL(to, f"https:{search['srcset'][0]['src']}")
                        client.sendReplyMessage(msg_id,to, result)
                except:client.sendReplyMessage(msg_id,to, "# Failed.")
          except:client.sendReplyMessage(msg_id, to, f"# Failed, {query} Not Found.")
        elif texttl.startswith('related '):
          try:
            texts = textt[8:]
            textsl = texts.lower()
            key = setKey.title()
            sep = textsl.split(" ")
            query =  textsl.replace(sep[0]+" ","")
            cond = query.split("-")
            search = str(cond[0])
            req = requests.get(f"https://id.wikipedia.org/api/rest_v1/page/related/{str(search)}")
            data = req.text
            data = json.loads(data)
            if len(cond) == 1:
                no = 0
                result = f"> Wikipedia Related {textsl.capitalize()} // Founds : {len(data['pages'])}\n"
                for reighpuy in data["pages"]:
                    no += 1
                    result += f'\n   ({str(no)}). {reighpuy["title"]}'
                result += f"\n\nFor Info Using :\n\t`{key}Wikipedia Related {textsl.capitalize()}-[number]`"
                client.sendReplyMessage(msg_id, to, result)
            elif len(cond) == 2:
                try:
                    num = int(cond[1])
                    if num <= len(data["pages"]):
                        search = data["pages"][num - 1]
                        result = f" > Wikipedia Related {query.capitalize()}"
                        result += f"\n\tTitle : {search['title']}"
                        result += f"\n\tPage ID : {int(search['pageid'])}"
                        result += f"\n\tType : {search['type']}"
                        result += f"\n\tLanguage : {search['lang']}"
                        result += f"\n\tWikiBase Item : {search['wikibase_item']}"
                        result += f"\n\tDescription : {search['extract']}"
                        #client.sendImageWithURL(to, f"{search['thumbnail']['source']}")
                        client.sendReplyMessage(msg_id,to, result)
                except:client.sendReplyMessage(msg_id,to, "# Failed.")
          except:client.sendReplyMessage(msg_id, to, f"# Failed, {query} Not Found.")
        elif texttl.startswith('randomsummary'):
          try:
            req = requests.get("https://id.wikipedia.org/api/rest_v1/page/random/summary")
            data = req.text
            data = json.loads(data)
            results = " > Wikipedia Random Summary"
            results += f'\n\tTitle : {str(data["title"])}'
            results += f'\n\tWikibase_item : {str(data["wikibase_item"])}'
            results += f'\n\tPageId : {str(data["pageid"])}'
            results += f'\n\tLanguage : {str(data["lang"])}'
            #results += f'\n\tDescription : {str(data["description"])}'
            results += f'\n\tFull Desc : {str(data["extract"])}'
            client.sendReplyMessage(msg_id, to, results)
          except:client.sendReplyMessage(msg_id, to, "# Failed.")

    # SUPERHERO
    elif cmd.startswith('superhero'):
      try:
        textt = removeCmd(text, setKey)
        texttl = textt.lower()
        param1 = sender
        client.findAndAddContactsByMid(param1)
        results = ' > Superhero'
        results += '\nMax Number of Hero : 731'
        results += '\n\nUsage : '
        results += '\n\t{key}Superhero List'
        results += '\n\t{key}Superhero Search (name)'
        results += '\n\t{key}Superhero Num (no)'
        results += '\n\t{key}Superhero Powerstats (no)'
        results += '\n\t{key}Superhero Bio (no)'
        results += '\n\t{key}Superhero Appearance (no)'
        results += '\n\t{key}Superhero Work (no)'
        results += '\n\t{key}Superhero Connections (no)'
        results += '\n\t{key}Superhero Image (no)'
        if cmd == 'superhero':
            client.sendReplyMessage(msg_id, to, results.format_map(SafeDict(key=setKey.title())))
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
            results = " > Superhero Info"
            results += f'\n\tNama : {data["results-for"]}'
            results += f'\n\tID : {data["results"][0]["id"]}'
            results += f'\n\t-> Power stats : '
            results += f'\n\tIntelligence : {data["results"][0]["powerstats"]["intelligence"]}'
            results += f'\n\tStrength : {data["results"][0]["powerstats"]["strength"]}'
            results += f'\n\tSpeed : {data["results"][0]["powerstats"]["speed"]}'
            results += f'\n\tDurability : {data["results"][0]["powerstats"]["durability"]}'
            results += f'\n\tPower : {data["results"][0]["powerstats"]["power"]}'
            results += f'\n\tCombat : {data["results"][0]["powerstats"]["combat"]}'
            results += f'\n\t-> Biography : '
            results += f'\n\tFull Name : {data["results"][0]["biography"]["full-name"]}'
            results += f'\n\tAlter egos : {data["results"][0]["biography"]["alter-egos"]}'
            results += f'\n\tPlace of-birth : {data["results"][0]["biography"]["place-of-birth"]}'
            results += f'\n\tFirst appearance : {data["results"][0]["biography"]["first-appearance"]}'
            results += f'\n\tPublisher : {data["results"][0]["biography"]["publisher"]}'
            results += f'\n\tAlignment : {data["results"][0]["biography"]["alignment"]}'
            results += f'\n\t-> Appearance : '
            results += f'\n\tGender : {data["results"][0]["appearance"]["gender"]}'
            results += f'\n\tRace : {data["results"][0]["appearance"]["race"]}'
            results += f'\n\tHeight : {data["results"][0]["appearance"]["height"][1]}'
            results += f'\n\tWeight : {data["results"][0]["appearance"]["weight"][1]}'
            results += f'\n\tEye color : {data["results"][0]["appearance"]["eye-color"]}'
            results += f'\n\tHair color : {data["results"][0]["appearance"]["hair-color"]}'
            results += f'\n\t-> Work : '
            results += f'\n\tOccupation : {data["results"][0]["work"]["occupation"]}'
            results += f'\n\tBase : {data["results"][0]["work"]["base"]}'
            results += f'\n\t-> Connections : '
            results += f'\n\tGroup affiliation : {data["results"][0]["connections"]["group-affiliation"]}'
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
            results += f' > Country Info {ordered}'
            results += f'\n\tName : {str(data["Response"][0]["Name"])}'
            results += f'\n\tAlpha 2 Code : {str(data["Response"][0]["Alpha2Code"])}'
            results += f'\n\tAlpha 3 Code : {str(data["Response"][0]["Alpha3Code"])}'
            results += f'\n\tNative Name : {str(data["Response"][0]["NativeName"])}'
            results += f'\n\tRegion : {str(data["Response"][0]["Region"])}'
            results += f'\n\tSub Region : {str(data["Response"][0]["SubRegion"])}'
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
                result = f"> {query.capitalize()}"
                for reighpuy in data["result"][0:10]:
                    no += 1
                    result += "\n   ({}). {} [{}]".format(str(no), reighpuy["title"], reighpuy["developer"])
                result += f"\nFor Info Using :\n\t`{key}Playstore {query}-[num]`"
                client.sendReplyMessage(msg_id,to, result)
            elif len(cond) == 2:
                try:
                    num = int(cond[1])
                    if num <= len(data["result"]):
                        search = data["result"][num - 1]
                        result = f"Title : {search['title']}"
                        result += f"\n\tDescription : {search['desc']}"
                        result += f"\n\tURL : {search['url']}"
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
            for reighpuy in data["result"][0:10]:
                no += 1
                result += "\n   ({}). {} \n\t  URL -> [{}]".format(str(no), reighpuy["title"], reighpuy["url"])
            result += f"\nFor Info Using :\n\t`{key}Ytsearch {query}-[num]`"
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
            for reighpuy in data["result"][0:10]:
                no += 1
                result += "\n   ({}). `{}` [{}]".format(str(no), reighpuy["title"], reighpuy["date"])
            #result += f"\nFor Info Using :\n\t`{key}Tvchannel {query}-[num]`"
            client.sendReplyMessage(msg_id,to, result)
        except Exception as error:
            print(error)

    # CAT FACTS
    elif cmd == 'cat facts':
        data = json.loads(requests.get("https://cat-fact.herokuapp.com/facts").text)
        yup = data["all"]
        random_index = randint(0, len(yup)-1)
        yup2 = yup[random_index]['text']
        client.sendReplyMessage(msg_id, to, yup2)

    # CAT IMAGE
    elif cmd.startswith("catimage"):
      try:
        data = json.loads(requests.get("https://api.thecatapi.com/v1/images/search").text)
        client.sendImageWithURL(to, data[0]['url'])
      except:client.sendReplyMessage(msg_id, to, f"# Failed.")

    # DOG IMAGE
    elif cmd.startswith("dogimage"):
      try:
        data = json.loads(requests.get("https://random.dog/woof.json").text)
        client.sendImageWithURL(to, data['url'])
      except:client.sendReplyMessage(msg_id, to, f"# Failed.")

    # FOX IMAGE
    elif cmd.startswith("foximage"):
      try:
        data = json.loads(requests.get("https://randomfox.ca/floof/").text)
        client.sendImageWithURL(to, data['image'])
      except:client.sendReplyMessage(msg_id, to, f"# Failed.")

    # AL'QURAN SURAH
    elif cmd.startswith("surah "):
      try:
        process = msg.text.split(" ")
        ordered = msg.text.replace(process[0] + " ","")
        r = requests.get(f"https://api.banghasan.com/quran/format/json/surat/{str(ordered)}")
        data = r.text
        data = json.loads(data)
        results = " > Info Surah"
        results += f'\n\tNomor Surah : {str(data["hasil"][0]["nomor"])}'
        results += f'\n\tNama Surah : {str(data["hasil"][0]["nama"])}'
        results += f'\n\tArti Surah : {str(data["hasil"][0]["arti"])}'
        results += f'\n\tAsma : {str(data["hasil"][0]["asma"])}'
        results += f'\n\tStart : {str(data["hasil"][0]["start"])}'
        results += f'\n\tAyat : {str(data["hasil"][0]["ayat"])}'
        results += f'\n\tTipe : {str(data["hasil"][0]["type"])}'
        results += f'\n\tUrut : {str(data["hasil"][0]["urut"])}'
        results += f'\n\tRukuk : {str(data["hasil"][0]["rukuk"])}'
        #results += f'\n\nKeterangan : \n{str(data["hasil"][0]["keterangan"])}'
        client.sendReplyMessage(msg_id, to, str(results))
      except:client.sendReplyMessage(msg_id, to, f"# Failed : {ordered} Not Found.")

    # RANDOM NASA
    elif cmd == 'apod':
        req = requests.get("https://api.nasa.gov/planetary/apod?api_key=plx64zHKoYUg03rYVT8FqmJrwy3xcKsUaW7GsfHr")
        data = req.text
        data = json.loads(data)
        results = " > Apod"
        results += f'\n\tTitle : {str(data["title"])}'
        results += f'\n\tMedia Type : {str(data["media_type"])}'
        results += f'\n\tDate : {str(data["date"])}'
        results += f'\n\tDescription : {str(data["explanation"])}'
        results += f'\n\tURL : {str(data["url"])}'
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

    elif cmd.startswith("random quote"):
        req = requests.get("http://apitrojans.herokuapp.com/quotes")
        data = req.text
        data = json.loads(data)
        client.sendReplyMessage(msg_id,to, data["result"]["quotes"])

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

    # Trending Twitter
    elif cmd.startswith("trendtwitter"):
        try:
            key = setKey.title()
            sep = msg.text.split(" ")
            query =  msg.text.replace(sep[0]+" ","")
            cond = query.split("-")
            #search = str(cond[0])
            r = requests.get(f"https://api.haipbis.xyz/trendingtwitter/id")
            data = r.text
            data = json.loads(data)
            if len(cond) == 1:
                no = 0
                result = "> Twitter Trending Hashtag in Indonesia"
                for reighpuy in data["result"]:
                    no += 1
                    result += "\n   ({}). {} [ {} ]".format(str(no), reighpuy["title"], reighpuy["count"])
                result += f"\nFor Get the Link Using :\n\t`{key}{query}-[num]`"
                client.sendReplyMessage(msg_id,to, result)
            elif len(cond) == 2:
                try:
                    num = int(cond[1])
                    if num <= len(data["result"]):
                        search = data["result"][num - 1]
                        result = f"Title : {search['title']}"
                        result += f"\nTweet Count : {search['count']}"
                        result += f"\nURL : {search['link']}"
                        client.sendReplyMessage(msg_id,to, result)
                except:client.sendReplyMessage(msg_id,to, "# Failed.")
        except Exception as error:
            print(error)

    # MemeGen
    elif cmd.startswith("meme"):
        txt = msg.text.split("/")
        image = ("http://memegen.link/"+txt[1].replace(" ","_")+"/"+txt[2].replace(" ","_")+"/"+txt[3].replace(" ","_")+".jpg?watermark=none")
        client.sendImageWithURL(to, image)

                   # // MEDIA ENDED // #

    # // SETTINGS // #
    elif cmd.startswith('error'):
        textt = removeCmd(text, setKey)
        texttl = textt.lower()
        cond = textt.split(' ')
        results = ' > Error'
        results += '\nUsage : '
        results += '\n\t{key}Error'
        results += '\n\t{key}Error Logs'
        results += '\n\t{key}Error Reset'
        results += '\n\t{key}Error Detail <errid>'
        if cmd == 'error':
            client.sendReplyMessage(msg_id, to, results.format_map(SafeDict(key=setKey.title())))
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
                return client.sendReplyMessage(msg_id, to, results.format_map(SafeDict(key=setKey.title())))
            errid = cond[1]
            if os.path.exists('tmp/errors/%s.txt' % errid):
                with open('tmp/errors/%s.txt' % errid, 'r') as f:
                    client.sendReplyMessage(msg_id, to, f.read())
            else:
                return client.sendReplyMessage(msg_id, to, 'Failed display details error, errorid not valid')
        else:
            client.sendReplyMessage(msg_id, to, results.format_map(SafeDict(key=setKey.title())))

    elif txt.startswith('setkey'):
        textt = removeCmd(text, setKey)
        texttl = textt.lower()
        res = ' > Setting Key'
        res += '\nStatus : ' + bool_dict[settings['setKey']['status']][1]
        res += '\nKey : ' + settings['setKey']['key'].title()
        res += '\nUsage : '
        res += '\n\tSetkey'
        res += '\n\tSetkey <on/off>'
        res += '\n\tSetkey <key>'
        if txt == 'setkey':
            client.sendReplyMessage(msg_id, to, res)
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


    # Dictionary Details
    elif cmd == "detail dictionary".lower() or cmd == "details dictionary".lower():
        key = setKey.title()
        helpDictionary = helpdictionary()
        client.sendReplyMessage(msg_id, to, str(helpDictionary)+f"\n\nFor Info Using : \n\t{key}Info [command_name]\n\tExample : {key}Info Antonym")

    # Utility Details
    elif cmd == "detail utility".lower() or cmd == "details utility".lower():
        key = setKey.title()
        helpUtility = helputility()
        client.sendReplyMessage(msg_id, to, str(helpUtility)+f"\n\nFor Info Using : \n\t{key}Info [command_name]\n\tExample : {key}Info Apod")

    # Antonym
    elif cmd == "info antonym".lower():
        key = setKey.title()
        client.sendReplyMessage(msg_id, to, f"Usage : {key}antonym [word]\n\t  Example : {key}Antonym Bad\n\tWhos can use this Command? : Admin & Non-Admin")

    # Kbbi
    elif cmd == "info kbbi".lower():
        key = setKey.title()
        client.sendReplyMessage(msg_id, to, f"Usage : {key}Kbbi [kata]\n\t  Example : {key}Kbbi tidur\n\tWhos can use this Command? : Admin & Non-Admin")

    # Kindof
    elif cmd == "info kindof".lower():
        key = setKey.title()
        client.sendReplyMessage(msg_id, to, f"Usage : {key}Kindof [word]\n\t  Example : {key}Kindof Cow\n\tWhos can use this Command? : Admin & Non-Admin")

    # Meanslike
    elif cmd == "info meanslike".lower():
        key = setKey.title()
        client.sendReplyMessage(msg_id, to, f"Usage : {key}Meanslike [word]\n\t  Example : {key}Meanslike rose\n\tWhos can use this Command? : Admin & Non-Admin")

    # Popularnouns
    elif cmd == "info popularnouns".lower():
        key = setKey.title()
        client.sendReplyMessage(msg_id, to, f"Usage : {key}Popularnouns [word]\n\t  Example : {key}Popularnouns Cow\n\tWhos can use this Command? : Admin & Non-Admin")

    # Popularadjective
    elif cmd == "info popularadjective".lower():
        key = setKey.title()
        client.sendReplyMessage(msg_id, to, f"Usage : {key}Popularadjective [word]\n\t  Example : {key}Popularadjective Cow\n\tWhos can use this Command? : Admin & Non-Admin")

    # Synonym
    elif cmd == "info synonym".lower():
        key = setKey.title()
        client.sendReplyMessage(msg_id, to, f"Usage : {key}Synonym [word]\n\t  Example : {key}Synonym Cow\n\tWhos can use this Command? : Admin & Non-Admin")

    # Urbandict
    elif cmd == "info urbandict".lower():
        key = setKey.title()
        client.sendReplyMessage(msg_id, to, f"Usage : {key}Urbandict [word]\n\tWhos can use this Command? : Admin & Non-Admin")

    # Wikipedia
    elif cmd == "info wikipedia".lower():
        key = setKey.title()
        client.sendReplyMessage(msg_id, to, f"Usage : {key}Wikipedia\n\tWhos can use this Command? : Admin & Non-Admin")

    # Cat Facts
    elif cmd == "info catfacts".lower():
        key = setKey.title()
        client.sendReplyMessage(msg_id, to, f"Usage : {key}cat facts\n\tWhos can use this Command? : Admin & Non-Admin")

    # Country Info
    elif cmd == "info countryinfo".lower():
        key = setKey.title()
        client.sendReplyMessage(msg_id, to, f"Other Information of Country : \n\tExample : {key}Capital id\n\tExample : {key}Region id\n\tExample : {key}Subregion id\n\tExample : {key}Timezone id\n\tExample : {key}Nativename id\n\tExample : {key}Numericcode id\n\tExample : {key}Population id\n\tExample : {key}Callingcode id\n\tExample : {key}Currenciesname id\n\tExample : {key}Currenciescode id\n\tExample : {key}currenciessymbol id\n\nUsage : {key}Countryinfo [country_code]\n\t  Example : {key}Countryinfo id\n\tWhos can use this Command? : Admin & Non-Admin")

    # Daily Nasa
    elif cmd == "info apod".lower():
        key = setKey.title()
        client.sendReplyMessage(msg_id, to, f"Usage : {key}Apod\n\tWhos can use this Command? : Admin & Non-Admin")

    # Number
    elif cmd == "info numberinfo".lower():
        key = setKey.title()
        client.sendReplyMessage(msg_id, to, f"Usage : {key}Numberinfo [number]\n\t  Example : {key}Number 18\n\tWhos can use this Command? : Admin & Non-Admin")

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
        client.sendReplyMessage(msg_id, to, f"Usage : {key}Surah [nomor]\n\t  Example : {key}Surah 18\n\tWhos can use this Command? : Admin & Non-Admin")

    # Ytsearch
    elif cmd == "info ytsearch".lower():
        key = setKey.title()
        client.sendReplyMessage(msg_id, to, f"Usage : {key}Ytsearch\n\t Example : {key}Ytsearch kekeyi\n\tWhos can use this Command? : Admin & Non-Admin")

    # Playstore
    elif cmd == "info playstore".lower():
        key = setKey.title()
        client.sendReplyMessage(msg_id, to, f"Usage : {key}Playstore\n\t Example : {key}Playstore line\n\tWhos can use this Command? : Admin & Non-Admin")

    # Tvchannel
    elif cmd == "info tvchannel".lower():
        key = setKey.title()
        client.sendReplyMessage(msg_id, to, f"Usage : {key}Tvchannel\n\t Example : {key}Tvchannel antv\n\tWhos can use this Command? : Admin & Non-Admin")

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
                    #client.sendReplyMessage(msg_id, to, '# Failed : ' + str(talk_error))
                    print(str(talk_error))
                except Exception as error:
                    logError(error)
                    #client.sendReplyMessage(msg_id, to, '# Failed : ' + str(error))
                    print(str(error))
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
        sys.exit('[ System Message : *KEYBOARD INTERRUPT.')
    except Exception as error:
        logError(error)

def runningProgram():
    if settings['restartPoint'] is not None:
        try:
            client.sendMessage(settings['restartPoint'], 'Hey, im Back!')
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
            sys.exit('[ System Message : *KEYBOARD INTERRUPT.')
        except Exception as error:
            logError(error)
            continue
        if ops:
            for op in ops:
                executeOp(op)
                oepoll.setRevision(op.revision)

if __name__ == '__main__':
    print ('[ System Message : *PROGRAM HAS BEEN STARTED.\n______________________________')
    runningProgram()
