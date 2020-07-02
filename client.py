from important import *
from module import *
from setup_args import *
from list_def import *
from list_help import *
from info_commands import *

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
        texts = removeCmd(text)
        textfix = texts.lower()
        helpMessage = helpmessage()
        helpDictionary = helpdictionary()
        helpUtility = helputility()
        helpAvataredit = helpavataredit()
        helpMemegen = helpmemegen()
        key = setKey.title()
        results = f'  {str(helpMessage)}\nUsage : \n\t{key}help [Media_Command_Name]\n\tEx : {key}help dictionary'
        if cmd == 'menu' or cmd == 'help':
            client.sendReplyMessage(msg_id, to, results)
        elif textfix.startswith('dictionary'):
          try:
            client.sendReplyMessage(msg_id, to, str(helpDictionary)+f"\n\nFor Info Using : \n\t{key}Info [command_name]\n\tExample : {key}Info Antonym")
          except:client.sendReplyMessage(msg_id, to, f"# Failed.")
        elif textfix.startswith('utility'):
          try:
            client.sendReplyMessage(msg_id, to, str(helpUtility)+f"\n\nFor Info Using : \n\t{key}Info [command_name]\n\tExample : {key}Info Apod")
          except:client.sendReplyMessage(msg_id, to, f"# Failed.")
        elif textfix.startswith('avataredit') or textfix.startswith('avataredits'):
          try:
            client.sendReplyMessage(msg_id, to, str(helpAvataredit)+f"\nExample : \n\t{key}Recolor @Mention")
          except:client.sendReplyMessage(msg_id, to, f"# Failed.")
        elif textfix.startswith('memetemplate') or textfix.startswith('templatememe'):
          try:
            client.sendReplyMessage(msg_id, to, str(helpMemegen)+f"\nExample : \n\t{key}Meme/[template_name]/[text1]/[text2]")
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
        isi = f"> Profile Info"
        isi += "\n\tYour Mid : " + paramz.mid
        isi += "\n\tYour Name : " + paramz.displayName
        isi += "\n\tYour Bio : " + paramz.statusMessage
        client.sendReplyMessage(msg_id,to, isi)
        #client.sendImageWithURL(to, f"http://dl.profile.line-cdn.net/{paramz.pictureStatus}")

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
        client.sendImageWithURL(to, f"https://res.cloudinary.com/demo/image/fetch/w_200,o_30/http://dl.profile.line-cdn.net/{contact.pictureStatus}")

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
        except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")

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
        except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")

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
        except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")

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
        except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")

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
        except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")

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
          client.sendReplyMessage(msg_id,to, f"> Error {error}")

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
      except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")

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
      except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")

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
          except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")
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
          except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")
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
          except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")
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
                except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")
          except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")
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
          except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")


    # UTILITY

    # GITHUB
    elif cmd.startswith('github'):
        textt = removeCmd(text, setKey)
        texttl = textt.lower()
        param1 = sender
        client.findAndAddContactsByMid(param1)
        results = ' > Github'
        results += '\nMax Search : 30'
        results += '\nUsage : '
        results += '\n\t{key}Github Profile (Username)'
        results += '\n\t{key}Github Followers (Username)'
        results += '\n\t{key}Github Following (Username)'
        results += '\n\t{key}Github Repositories (Username)'
        results += '\n\t{key}Github Starred (Username)'
        results += '\n\t{key}Github Subscriptions (Username)'
        results += '\n\t{key}Github Events (Username)'
        if cmd == 'github':
            client.sendReplyMessage(msg_id, to, results.format_map(SafeDict(key=setKey.title())))
        elif texttl.startswith('profile '):
          try:
            texts = textt[8:]
            textsl = texts.lower()
            r = json.loads(requests.get(f"https://api.github.com/users/{ordered}").text)
            results = f" > Github Profile Info `{ordered.capitalize()}`"
            results += f"\n\tUsername : {r['login']}"
            results += f"\n\tID : {int(r['id'])}"
            results += f"\n\tType : {r['type']}"
            results += f"\n\tName : {r['name']}"
            results += f"\n\tEmail : {r['email']}"
            results += f"\n\tHireable : {r['hireable']}"
            results += f"\n\tBio : {r['bio']}"
            results += f"\n\tRepository : {int(r['public_repos'])}"
            results += f"\n\tFollowers : {int(r['followers'])}"
            results += f"\n\tFollowing : {int(r['following'])}"
            results += f"\n\tCreated At : {r['created_at']}"
            client.sendImageWithURL(to, f"{r['avatar_url']}")
            client.sendReplyMessage(msg_id,to, results)
          except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")
        elif texttl.startswith('followers '):
          try:
            texts = textt[10:]
            textsl = texts.lower()
            key = setKey.title()
            sep = textsl.split(" ")
            query =  textsl.replace(sep[0]+" ","")
            cond = query.split("-")
            search = str(cond[0])
            req = requests.get(f"https://api.github.com/users/{search}/followers")
            data = req.text
            data = json.loads(data)
            if len(cond) == 1:
                no = 0
                result = f"> Github {textsl.capitalize()} Followers // Founds : {len(data)}\n"
                for reighpuy in data:
                    no += 1
                    result += f'\n   ({str(no)}). {reighpuy["login"]}'
                result += f"\n\nFor Info Using :\n\t`{key}Github Followers {textsl.capitalize()}-[number]`"
                client.sendReplyMessage(msg_id, to, result)
            elif len(cond) == 2:
                try:
                    num = int(cond[1])
                    if num <= len(data):
                        searchs = data[num - 1]
                        result = f" > Github {search.capitalize()} Followers"
                        result += f"\n\tUsername : {searchs['login']}"
                        result += f"\n\tID : {int(searchs['id'])}"
                        result += f"\n\tType : {searchs['type']}"
                        client.sendImageWithURL(to, f"{searchs['avatar_url']}")
                        client.sendReplyMessage(msg_id,to, result)
                except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")
          except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")
        elif texttl.startswith('following '):
          try:
            texts = textt[10:]
            textsl = texts.lower()
            key = setKey.title()
            sep = textsl.split(" ")
            query =  textsl.replace(sep[0]+" ","")
            cond = query.split("-")
            search = str(cond[0])
            req = requests.get(f"https://api.github.com/users/{search}/following")
            data = req.text
            data = json.loads(data)
            if len(cond) == 1:
                no = 0
                result = f"> Github {textsl.capitalize()} Following // Founds : {len(data)}\n"
                for reighpuy in data:
                    no += 1
                    result += f'\n   ({str(no)}). {reighpuy["login"]}'
                result += f"\n\nFor Info Using :\n\t`{key}Github Following {textsl.capitalize()}-[number]`"
                client.sendReplyMessage(msg_id, to, result)
            elif len(cond) == 2:
                try:
                    num = int(cond[1])
                    if num <= len(data):
                        searchs = data[num - 1]
                        result = f" > Github {search.capitalize()} Following"
                        result += f"\n\tUsername : {searchs['login']}"
                        result += f"\n\tID : {int(searchs['id'])}"
                        result += f"\n\tType : {searchs['type']}"
                        client.sendImageWithURL(to, f"{searchs['avatar_url']}")
                        client.sendReplyMessage(msg_id,to, result)
                except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")
          except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")
        elif texttl.startswith('repositories '):
          try:
            texts = textt[13:]
            textsl = texts.lower()
            key = setKey.title()
            sep = textsl.split(" ")
            query =  textsl.replace(sep[0]+" ","")
            cond = query.split("-")
            search = str(cond[0])
            req = requests.get(f"https://api.github.com/users/{search}/repos")
            data = req.text
            data = json.loads(data)
            if len(cond) == 1:
                no = 0
                result = f"> Github {textsl.capitalize()} Repositories // Founds : {len(data)}\n"
                for reighpuy in data:
                    no += 1
                    result += f'\n   ({str(no)}). {reighpuy["name"]}'
                result += f"\n\nFor Info Using :\n\t`{key}Github Repositories {textsl.capitalize()}-[number]`"
                client.sendReplyMessage(msg_id, to, result)
            elif len(cond) == 2:
                try:
                    num = int(cond[1])
                    if num <= len(data):
                        search = data[num - 1]
                        result = f" > Github Repository Info"
                        result += f"\n\tName : {search['name']}"
                        result += f"\n\tID : {int(search['id'])}"
                        result += f"\n\tFull Name : {search['full_name']}"
                        result += f"\n\tDescription : {search['description']}"
                        result += f"\n\tPrivate? : {search['private']}"
                        result += f"\n\tDefault Branch : {search['default_branch']}"
                        result += f"\n\tSize : {int(search['size'])}"
                        result += f"\n\tLanguage : {search['language']}"
                        result += f"\n\tForks Count : {int(search['forks_count'])}"
                        result += f"\n\tWatchers : {int(search['watchers'])}"
                        result += f"\n\tLicense : {search['license']}"
                        result += f"\n\tCreated At : {search['created_at']}"
                        result += f"\n\tPushed At : {search['pushed_at']}"
                        result += f"\n\tVisit : https://github.com/{search['full_name']}"
                        client.sendReplyMessage(msg_id,to, result)
                except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")
          except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")
        elif texttl.startswith('starred '):
          try:
            texts = textt[8:]
            textsl = texts.lower()
            key = setKey.title()
            sep = textsl.split(" ")
            query =  textsl.replace(sep[0]+" ","")
            cond = query.split("-")
            search = str(cond[0])
            req = requests.get(f"https://api.github.com/users/{search}/starred")
            data = req.text
            data = json.loads(data)
            if len(cond) == 1:
                no = 0
                result = f"> Github {textsl.capitalize()} Starred // Founds : {len(data)}\n"
                for reighpuy in data:
                    no += 1
                    result += f'\n   ({str(no)}). {reighpuy["name"]}'
                result += f"\n\nFor Info Using :\n\t`{key}Github Starred {textsl.capitalize()}-[number]`"
                client.sendReplyMessage(msg_id, to, result)
            elif len(cond) == 2:
                try:
                    num = int(cond[1])
                    if num <= len(data):
                        searchs = data[num - 1]
                        result = f" > Github {search.capitalize()} Starred"
                        result += f"\n\tName : {searchs['name']}"
                        result += f"\n\tID : {int(searchs['id'])}"
                        result += f"\n\tFull Name : {searchs['full_name']}"
                        result += f"\n\tDescription : {searchs['description']}"
                        result += f"\n\tPrivate? : {searchs['private']}"
                        result += f"\n\tDefault Branch : {searchs['default_branch']}"
                        result += f"\n\tSize : {int(searchs['size'])}"
                        result += f"\n\tLanguage : {searchs['language']}"
                        result += f"\n\tForks Count : {int(searchs['forks_count'])}"
                        result += f"\n\tWatchers : {int(searchs['watchers'])}"
                        result += f"\n\tLicense : {searchs['license']}"
                        result += f"\n\tCreated At : {searchs['created_at']}"
                        result += f"\n\tPushed At : {searchs['pushed_at']}"
                        result += f"\n\tVisit : https://github.com/{searchs['full_name']}"
                        client.sendReplyMessage(msg_id,to, result)
                except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")
          except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")
        elif texttl.startswith('subscriptions '):
          try:
            texts = textt[14:]
            textsl = texts.lower()
            key = setKey.title()
            sep = textsl.split(" ")
            query =  textsl.replace(sep[0]+" ","")
            cond = query.split("-")
            search = str(cond[0])
            req = requests.get(f"https://api.github.com/users/{search}/subscriptions")
            data = req.text
            data = json.loads(data)
            if len(cond) == 1:
                no = 0
                result = f"> Github {textsl.capitalize()} Subscriptions // Founds : {len(data)}\n"
                for reighpuy in data:
                    no += 1
                    result += f'\n   ({str(no)}). {reighpuy["name"]}'
                result += f"\n\nFor Info Using :\n\t`{key}Github Subscriptions {textsl.capitalize()}-[number]`"
                client.sendReplyMessage(msg_id, to, result)
            elif len(cond) == 2:
                try:
                    num = int(cond[1])
                    if num <= len(data):
                        searchs = data[num - 1]
                        result = f" > Github {search.capitalize()} Subscriptions"
                        result += f"\n\tName : {searchs['name']}"
                        result += f"\n\tID : {int(searchs['id'])}"
                        result += f"\n\tFull Name : {searchs['full_name']}"
                        result += f"\n\tDescription : {searchs['description']}"
                        result += f"\n\tPrivate? : {searchs['private']}"
                        result += f"\n\tDefault Branch : {searchs['default_branch']}"
                        result += f"\n\tSize : {int(searchs['size'])}"
                        result += f"\n\tLanguage : {searchs['language']}"
                        result += f"\n\tForks Count : {int(searchs['forks_count'])}"
                        result += f"\n\tWatchers : {int(searchs['watchers'])}"
                        result += f"\n\tLicense : {searchs['license']}"
                        result += f"\n\tCreated At : {searchs['created_at']}"
                        result += f"\n\tPushed At : {searchs['pushed_at']}"
                        result += f"\n\tVisit : https://github.com/{searchs['full_name']}"
                        client.sendReplyMessage(msg_id,to, result)
                except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")
          except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")
        elif texttl.startswith('events '):
          try:
            texts = textt[7:]
            textsl = texts.lower()
            key = setKey.title()
            sep = textsl.split(" ")
            query =  textsl.replace(sep[0]+" ","")
            cond = query.split("-")
            search = str(cond[0])
            req = requests.get(f"https://api.github.com/users/{search}/events")
            data = req.text
            data = json.loads(data)
            if len(cond) == 1:
                no = 0
                result = f"> Github {textsl.capitalize()} Events // Founds : {len(data)}\n"
                for reighpuy in data:
                    no += 1
                    result += f'\n   ({str(no)}). {reighpuy["id"]}'
                result += f"\n\nFor Info Using :\n\t`{key}Github Events {textsl.capitalize()}-[number]`"
                client.sendReplyMessage(msg_id, to, result)
            elif len(cond) == 2:
                try:
                    num = int(cond[1])
                    if num <= len(data):
                        searchs = data[num - 1]
                        result = f" > Github {search.capitalize()} Events"
                        result += f"\n\tType : {searchs['type']}"
                        result += f"\n\tID : {searchs['id']}"
                        result += f"\n\tRepo : {searchs['repo']['name']}"
                        result += f"\n\tActor : {searchs['actor']['login']}"
                        result += f"\n\tPayload Size : {searchs['payload']['size']}"
                        result += f"\n\tPayload Ref : {searchs['payload']['ref']}"
                        result += f"\n\tPayload Head : {searchs['payload']['head']}"
                        result += f"\n\tPayload Before : {searchs['payload']['before']}"
                        result += f"\n\tPublic? : {searchs['public']}"
                        result += f"\n\tCreated At : {searchs['created_at']}"
                        client.sendReplyMessage(msg_id,to, result)
                except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")
          except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")

    # get Country Info
    elif cmd.startswith("countryinfo "):
        try:
            key = setKey.title()
            sep = msg.text.split(" ")
            query =  msg.text.replace(sep[0]+" ","")
            cond = query.split("-")
            search = str(cond[0])
            r = requests.get(f"http://countryapi.gear.host/v1/Country/getCountries?pName={str(search)}")
            data = r.text
            data = json.loads(data)
            if len(cond) == 1:
                no = 0
                result = f"> {query.capitalize()} // {len(data['Response'])} Found"
                for reighpuy in data["Response"]:
                    no += 1
                    result += "\n   ({}). {} [{}]".format(str(no), reighpuy["Name"], reighpuy["Alpha2Code"])
                result += f"\nFor Info Using :\n\t`{key}Countryinfo {query}-[num]`"
                client.sendReplyMessage(msg_id,to, result)
            elif len(cond) == 2:
                try:
                    num = int(cond[1])
                    if num <= len(data["Response"]):
                        search = data["Response"][num - 1]
                        result = f"Name : {search['Name']}"
                        result += f"\n\tCode 2 : {search['Alpha2Code']}"
                        result += f"\n\tCode 3 : {search['Alpha3Code']}"
                        result += f"\n\tRegion : {search['Region']}"
                        result += f"\n\tSub Region : {search['SubRegion']}"
                        result += f"\n\tNative Name : {search['NativeName']}"
                        result += f"\n\tLatitude : {search['Latitude']}"
                        result += f"\n\tLongitude : {search['Longitude']}"
                        result += f"\n\tArea : {search['Area']}"
                        result += f"\n\tNumeric Code : {search['NumericCode']}"
                        result += f"\n\tNative Language : {search['Longitude']}"
                        result += f"\n\tCurrency Code : {search['CurrencyCode']}"
                        result += f"\n\tCurrency Name : {search['CurrencyName']}"
                        result += f"\n\tCurrency Symbol : {search['CurrencySymbol']}"
                        client.sendImageWithURL(to, f"{search['FlagPng']}")
                        client.sendReplyMessage(msg_id,to, result)
                except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")
        except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")

    # Capital of Country
    elif cmd.startswith("capital "):
      try:
        process = msg.text.split(" ")
        ordered = msg.text.replace(process[0] + " ","")
        data = json.loads(requests.get(f"https://restcountries.eu/rest/v2/alpha/{ordered}").text)
        client.sendReplyMessage(msg_id,to, f"Capital of `{data['name']}` is `{data['capital']}`")
      except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")

    # Region of Country
    elif cmd.startswith("region "):
      try:
        process = msg.text.split(" ")
        ordered = msg.text.replace(process[0] + " ","")
        data = json.loads(requests.get(f"https://restcountries.eu/rest/v2/alpha/{ordered}").text)
        client.sendReplyMessage(msg_id,to, f"Region of `{data['name']}` is `{data['region']}`")
      except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")

    # Subregion of Country
    elif cmd.startswith("subregion "):
      try:
        process = msg.text.split(" ")
        ordered = msg.text.replace(process[0] + " ","")
        data = json.loads(requests.get(f"https://restcountries.eu/rest/v2/alpha/{ordered}").text)
        client.sendReplyMessage(msg_id,to, f"Subregion of `{data['name']}` is `{data['subregion']}`")
      except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")

    # Timezones of Country
    elif cmd.startswith("timezone "):
      try:
        process = msg.text.split(" ")
        ordered = msg.text.replace(process[0] + " ","")
        data = json.loads(requests.get(f"https://restcountries.eu/rest/v2/alpha/{ordered}").text)
        client.sendReplyMessage(msg_id,to, f"Timezone of `{data['name']}` is `{data['timezones']}`")
      except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")

    # Native Name of Country
    elif cmd.startswith("nativename "):
      try:
        process = msg.text.split(" ")
        ordered = msg.text.replace(process[0] + " ","")
        data = json.loads(requests.get(f"https://restcountries.eu/rest/v2/alpha/{ordered}").text)
        client.sendReplyMessage(msg_id,to, f"Nativename of `{data['name']}` is `{data['nativeName']}`")
      except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")

    # Numberic Code of Country
    elif cmd.startswith("numericcode "):
      try:
        process = msg.text.split(" ")
        ordered = msg.text.replace(process[0] + " ","")
        data = json.loads(requests.get(f"https://restcountries.eu/rest/v2/alpha/{ordered}").text)
        client.sendReplyMessage(msg_id,to, f"Numericcode of `{data['name']}` is `{data['numericCode']}`")
      except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")

    # Population of Country
    elif cmd.startswith("population "):
      try:
        process = msg.text.split(" ")
        ordered = msg.text.replace(process[0] + " ","")
        data = json.loads(requests.get(f"https://restcountries.eu/rest/v2/alpha/{ordered}").text)
        client.sendReplyMessage(msg_id,to, f"Population of `{data['name']}` is `{data['population']}`")
      except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")

    # Callingcode of Country
    elif cmd.startswith("callingcode "):
      try:
        process = msg.text.split(" ")
        ordered = msg.text.replace(process[0] + " ","")
        data = json.loads(requests.get(f"https://restcountries.eu/rest/v2/alpha/{ordered}").text)
        client.sendReplyMessage(msg_id,to, f"callingcode of `{data['name']}` is `{data['callingCodes']}`")
      except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")

    # Currencies Name of Country
    elif cmd.startswith("currenciesname "):
      try:
        process = msg.text.split(" ")
        ordered = msg.text.replace(process[0] + " ","")
        data = json.loads(requests.get(f"https://restcountries.eu/rest/v2/alpha/{ordered}").text)
        client.sendReplyMessage(msg_id,to, f"Currencies Name of `{data['name']}` is `{data['currencies'][0]['name']}`")
      except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")

    # Currencies Code of Country
    elif cmd.startswith("currenciescode "):
      try:
        process = msg.text.split(" ")
        ordered = msg.text.replace(process[0] + " ","")
        data = json.loads(requests.get(f"https://restcountries.eu/rest/v2/alpha/{ordered}").text)
        client.sendReplyMessage(msg_id,to, f"Currencies Code of `{data['name']}` is `{data['currencies'][0]['code']}`")
      except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")

    # Currencies Symbol of Country
    elif cmd.startswith("currenciessymbol "):
      try:
        process = msg.text.split(" ")
        ordered = msg.text.replace(process[0] + " ","")
        data = json.loads(requests.get(f"https://restcountries.eu/rest/v2/alpha/{ordered}").text)
        client.sendReplyMessage(msg_id,to, f"Currencies Symbol of `{data['name']}` is `{data['currencies'][0]['symbol']}`")
      except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")

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
                result += f"\nFor Info Using :\n\t`{key}Playstore {query.capitalize()}-[number]`"
                client.sendReplyMessage(msg_id,to, result)
            elif len(cond) == 2:
                try:
                    num = int(cond[1])
                    if num <= len(data["result"]):
                        search = data["result"][num - 1]
                        result = "> Playstore"
                        result += f"\n\tTitle : {search['title']}"
                        result += f"\n\tDescription : {search['desc']}"
                        result += f"\n\tURL : {search['url']}"
                        client.sendImageWithURL(to, f"{search['image']}")
                        client.sendReplyMessage(msg_id,to, result)
                except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")
        except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")

    # Loker
    elif cmd.startswith("loker "):
        try:
            key = setKey.title()
            sep = msg.text.split(" ")
            query =  msg.text.replace(sep[0]+" ","")
            cond = query.split("-")
            search = str(cond[0])
            r = requests.get(f"http://dolphinapi.herokuapp.com/api/indeed?city={search}")
            data = r.text
            data = json.loads(data)
            if len(cond) == 1:
                no = 0
                result = f"> Lowongan Kerja - {query.capitalize()}"
                for reighpuy in data["result"]:
                    no += 1
                    result += f"\n   ({str(no)}). {reighpuy['title']}"
                result += f"\nFor Info Using :\n\t`{key}Loker {query.capitalize()}-[number]`"
                client.sendReplyMessage(msg_id,to, result)
            elif len(cond) == 2:
                try:
                    num = int(cond[1])
                    if num <= len(data["result"]):
                        search = data["result"][num - 1]
                        result = "> Lowongan Kerja"
                        result += f"\n\tTitle : {search['title']}"
                        result += f"\n\tDate : {search['date']}"
                        result += f"\n\tLocation : {search['location']}"
                        result += f"\n\tURL : {search['url']}"
                        client.sendReplyMessage(msg_id,to, result)
                except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")
        except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")

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
        except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")

    # Tv Channel
    elif cmd.startswith("tvchannel "):
        try:
            key = setKey.title()
            sep = msg.text.split(" ")
            query =  msg.text.replace(sep[0]+" ","")
            data = json.loads(requests.get(f"http://dolphinapi.herokuapp.com/api/television?channel={str(query)}").text)
            no = 0
            result = f"> TV Channel - {query.upper()}"
            for reighpuy in data["result"]:
                no += 1
                result += "\n   ({}). {} | {}".format(str(no), reighpuy["title"], reighpuy["date"])
            #result += f"\nFor Info Using :\n\t`{key}Tvchannel {query}-[num]`"
            client.sendReplyMessage(msg_id,to, result)
        except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")

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
      except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")

    # Astronomy
    elif cmd.startswith('astronomy'):
        textt = removeCmd(text, setKey)
        texttl = textt.lower()
        param1 = sender
        client.findAndAddContactsByMid(param1)
        results = ' > Astronomy'
        results += '\n\nUsage : '
        results += '\n\t{key}Astronomy Today'
        results += '\n\t{key}Astronomy Random'
        if cmd == 'astronomy':
            client.sendReplyMessage(msg_id, to, results.format_map(SafeDict(key=setKey.title())))
        elif texttl.startswith('today'):
          try:
            data = json.loads(requests.get("https://apodapi.herokuapp.com/api").text)
            results = f" > Astronomy Info"
            results += f"\n\tTitle : {data['title']}"
            results += f"\n\tDate : {data['date']}"
            results += f"\n\tMedia Type : {data['media_type']}"
            results += f"\n\tURL : {data['url']}"
            results += f"\n\tCopyright : {data['copyright']}"
            results += f"\n\tDescription : {data['description']}"
            client.sendReplyMessage(msg_id,to, results)
          except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")
        elif texttl.startswith('random'):
          try:
            data = json.loads(requests.get("https://apodapi.herokuapp.com/api?count=1").text)
            results = f" > Astronomy Info"
            results += f"\n\tTitle : {data[0]['title']}"
            results += f"\n\tDate : {data[0]['date']}"
            results += f"\n\tMedia Type : {data[0]['media_type']}"
            results += f"\n\tURL : {data[0]['url']}"
            results += f"\n\tCopyright : {data[0]['copyright']}"
            results += f"\n\tDescription : {data[0]['description']}"
            client.sendReplyMessage(msg_id,to, results)
          except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")

    # Quotes
    elif cmd.startswith('quotes'):
        textt = removeCmd(text, setKey)
        texttl = textt.lower()
        param1 = sender
        client.findAndAddContactsByMid(param1)
        results = ' > Quotes'
        results += '\n\nUsage : '
        results += '\n\t{key}Quotes Breakingbad'
        results += '\n\t{key}Quotes Random'
        results += '\n\t{key}Quotes Swanson'
        results += '\n\t{key}Quotes Trump'
        if cmd == 'quotes':
            client.sendReplyMessage(msg_id, to, results.format_map(SafeDict(key=setKey.title())))
        elif texttl.startswith('random'):
          try:
            data = json.loads(requests.get("https://quote-garden.herokuapp.com/api/v2/quotes/random").text)
            results = f"> Quotes - Random"
            results += f"\n\tAuthor : {data['quote']['quoteAuthor']}"
            results += f"\n\tQuote : {data['quote']['quoteText']}"
            client.sendReplyMessage(msg_id,to, results)
          except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")
        elif texttl.startswith('breakingbad'):
          try:
            data = json.loads(requests.get("https://breaking-bad-quotes.herokuapp.com/v1/quotes").text)
            results = f"> Quotes - BreakingBad"
            results += f"\n\tAuthor : {data[0]['author']}"
            results += f"\n\tQuote : {data[0]['quote']}"
            client.sendReplyMessage(msg_id,to, results)
          except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")
        elif texttl.startswith('swanson'):
          try:
            data = json.loads(requests.get("http://ron-swanson-quotes.herokuapp.com/v2/quotes/").text)
            results = f"> Quotes - Swanson"
            results += f"\n\tQuote : {data[0]}"
            client.sendReplyMessage(msg_id,to, results)
          except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")
        elif texttl.startswith('trump'):
          try:
            data = json.loads(requests.get("https://www.tronalddump.io/random/quote").text)
            results = f"> Quotes - Trump"
            results += f"\n\tAuthor : {data['_embedded']['author'][0]['name']}"
            results += f"\n\tQuote : {data['value']}"
            client.sendReplyMessage(msg_id,to, results)
          except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")

    # TRANSLATE TO ID
    elif cmd.startswith("tr-id "):
        process = msg.text.split(" ")
        ordered = msg.text.replace(process[0] + " ","")
        r = requests.get(f"https://guarded-lowlands-57340.herokuapp.com/index.php?to=id&text={ordered}")
        data = r.text
        result = "> Translate to ID"
        result += f"\nText : \n\t{ordered}"
        result += f"\n\nTranslated : \n\t{data}"
        client.sendReplyMessage(msg_id,to, result)

    # TONGUE TWISTER
    elif cmd.startswith("tonguetwister"):
        choice = ["en","id"]
        data = json.loads(requests.get(f"https://api.haipbis.xyz/randomtonguetwister/{random.choice(choice)}").text)
        client.sendReplyMessage(msg_id,to, data["text"])

    # CREATE QR CODE
    elif cmd.startswith("createqr "):
      try:
         process = msg.text.split(" ")
         ordered = msg.text.replace(process[0] + " ","")
         client.sendImageWithURL(to, f"https://api.qrserver.com/v1/create-qr-code/?data={ordered}&size=400x400")
      except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")

    # Postcode
    elif cmd.startswith("postcode "):
      try:
         process = msg.text.split(" ")
         ordered = msg.text.replace(process[0] + " ","")
         client.sendReplyMessage(msg_id,to, f"http://api.zippopotam.us/us/{int(ordered)}")
      except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")

    # CREATE CODE IMAGE
    elif cmd.startswith("createcode "):
      try:
         process = msg.text.split(" ")
         ordered = msg.text.replace(process[0] + " ","")
         data = json.loads(requests.get(f"http://rayenking.herokuapp.com/sscode?code={ordered}").text)
         client.sendImageWithURL(to, f"{data['result']}")
      except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")

    # SEARCH SONG LYRICS
    elif cmd.startswith("searchlyrics ") or cmd.startswith("searchlyric "):
      try:
         process = msg.text.split(" ")
         ordered = msg.text.replace(process[0] + " ","")
         r = json.loads(requests.get(f"http://dolphinapi.herokuapp.com/api/lyric?query={ordered}").text)
         client.sendReplyMessage(msg_id, to, f"> Song Title : {r['result']['title']}\n\n{r['result']['lyric']}")
      except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")

    # Random Number Story
    elif cmd.startswith("numberinfo "):
      try:
         process = msg.text.split(" ")
         ordered = msg.text.replace(process[0] + " ","")
         req = requests.get(f"http://numbersapi.com/{str(ordered)}?json")
         data = req.text
         data = json.loads(data)
         client.sendReplyMessage(msg_id, to, data["text"])
      except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")
    # RANDOM DATE
    elif cmd == 'random date':
      try:
         req = requests.get("http://numbersapi.com/random/date?json")
         data = req.text
         data = json.loads(data)
         client.sendReplyMessage(msg_id,to, data["text"])
      except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")
    # RANDOM YEARS
    elif cmd == 'random year':
      try:
         req = requests.get("http://numbersapi.com/random/year?json")
         data = req.text
         data = json.loads(data)
         client.sendReplyMessage(msg_id,to, data["text"])
      except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")

    # Soccer Livestream
    elif cmd.startswith("footballstreams") or cmd.startswith("footballstream"):
        try:
            key = setKey.title()
            sep = msg.text.split(" ")
            query =  msg.text.replace(sep[0]+" ","")
            cond = query.split("-")
            r = json.loads(requests.get(f"https://www.scorebat.com/video-api/v1/").text)
            if len(cond) == 1:
                no = 0
                result = "> Football Livestreams"
                for reighpuy in r:
                    no += 1
                    result += f"\n   ({str(no)}). {reighpuy['title']}"
                result += f"\nFor More Info Using :\n\t`{key}Footballstream-[number]`"
                client.sendReplyMessage(msg_id,to, result)
            elif len(cond) == 2:
                try:
                    num = int(cond[1])
                    if num <= len(r):
                        search = r[num - 1]
                        result = "> Football Livestreams Info"
                        result += f"\n\t{search['title']}"
                        result += f"\n\tDate : {search['date']}"
                        result += f"\n\tCompetition Name : {search['competition']['name']}"
                        result += f"\n\tCompetition URL : {search['competition']['url']}"
                        result += f"\n\tLiveStream URL : {search['url']}"
                        client.sendImageWithURL(to, f"{search['thumbnail']}")
                        client.sendReplyMessage(msg_id,to, result)
                except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")
        except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")

    # Hex Color
    elif cmd.startswith("hexcolor "):
      try:
        process = msg.text.split(" ")
        ordered = msg.text.replace(process[0] + " ","")
        data = json.loads(requests.get(f"https://www.thecolorapi.com/id?hex={ordered}&format=json").text)
        #client.sendImageWithURL(to, f"{data['image']['named']}")
        result = f"> Hex {data['hex']['value']}"
        result += f"\n\tColor Name : {data['name']['value']}"
        result += f"\n\tRGB : {data['rgb']['value']}"
        result += f"\n\tHSL : {data['hsl']['value']}"
        result += f"\n\tHSV : {data['hsv']['value']}"
        result += f"\n\tCMYK : {data['cmyk']['value']}"
        result += f"\n\tXYZ : {data['XYZ']['value']}"
        client.sendReplyMessage(msg_id,to, result)
      except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")

    # IP Info
    elif cmd.startswith("ipinfo "):
      try:
        process = msg.text.split(" ")
        ordered = msg.text.replace(process[0] + " ","")
        data = json.loads(requests.get(f"http://ip-api.com/json/{ordered}?fields=status,message,continent,continentCode,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,offset,currency,isp,org,as,asname,reverse,mobile,proxy,hosting,query").text)
        result = f"> IP Info {data['query']}"
        result += f"\n\tCountry : {data['country']}"
        result += f"\n\tCountry Code : {data['countryCode']}"
        result += f"\n\tRegion : {data['region']}"
        result += f"\n\tRegion Name : {data['regionName']}"
        result += f"\n\tCity : {data['city']}"
        result += f"\n\tLatitude : {data['lat']}"
        result += f"\n\tLongtitude : {data['lon']}"
        result += f"\n\tTimezone : {data['timezone']}"
        result += f"\n\tIsp : {data['isp']}"
        result += f"\n\tOrg : {data['org']}"
        result += f"\n\tOffset : {data['offset']}"
        result += f"\n\tCurrency : {data['currency']}"
        result += f"\n\tAsname : {data['asname']}"
        result += f"\n\tPeverse : {data['reverse']}"
        result += f"\n\tMobile : {data['mobile']}"
        result += f"\n\tProxy : {data['proxy']}"
        result += f"\n\tHosting : {data['hosting']}"
        client.sendReplyMessage(msg_id,to, result)
      except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")

    # Domain Info
    elif cmd.startswith("domaininfo "):
        try:
            key = setKey.title()
            sep = msg.text.split(" ")
            query =  msg.text.replace(sep[0]+" ","")
            cond = query.split("-")
            search = str(cond[0])
            r = requests.get(f"https://api.domainsdb.info/v1/domains/search?domain={search}&zone=com")
            data = r.text
            data = json.loads(data)
            if len(cond) == 1:
                no = 0
                result = f"> {query.capitalize()}"
                for reighpuy in data["domains"]:
                    no += 1
                    result += "\n   ({}). {}".format(str(no), reighpuy["domain"])
                result += f"\nFor Info Using :\n\t`{key}Domaininfo {query}-[number]`"
                client.sendReplyMessage(msg_id,to, result)
            elif len(cond) == 2:
                try:
                    num = int(cond[1])
                    if num <= len(data["domains"]):
                        search = data["domains"][num - 1]
                        result = f"> Domain : {search['domain']}"
                        result += f"\n\tCountry : {search['country']}"
                        result += f"\n\tActive? : {search['isDead']}"
                        result += f"\n\tA : {search['A']}"
                        result += f"\n\tNS : {search['NS']}"
                        result += f"\n\tCNAME : {search['CNAME']}"
                        result += f"\n\tMX : {search['MX']}"
                        result += f"\n\tTXT : {search['TXT']}"
                        result += f"\n\tCreate Date : {search['create_date']}"
                        result += f"\n\tUpdate Date : {search['update_date']}"
                        client.sendReplyMessage(msg_id,to, result)
                except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")
        except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")

    # Newton
    elif cmd.startswith("newton"):
      try:
        process = msg.text.split(" ")
        ordered = msg.text.replace(process[0] + " ","")
        data = json.loads(requests.get(f"https://newton.now.sh/factor/{ordered}").text)
        result = f"> Newton : {ordered}"
        result += f"\n\tOperation : {data['operation']}"
        result += f"\n\tExpression : {data['expression']}"
        result += f"\n\tResult : {data['result']}"
        client.sendReplyMessage(msg_id,to, result)
      except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")

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
                    result += "\n   ({}). {}".format(str(no), reighpuy["title"])
                result += f"\nFor Get the Link Using :\n\t`{key}Trendtwitter-[number]`"
                client.sendReplyMessage(msg_id,to, result)
            elif len(cond) == 2:
                try:
                    num = int(cond[1])
                    if num <= len(data["result"]):
                        search = data["result"][num - 1]
                        result = "> Twitter Trending Hashtag"
                        result += f"\n\tTitle : {search['title']}"
                        result += f"\n\tTweet Count : {search['count']}"
                        result += f"\n\tURL : {search['link']}"
                        client.sendReplyMessage(msg_id,to, result)
                except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")
        except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")

    # Upcoming Concert
    elif cmd.startswith("upcomingconcert") or cmd.startswith("upcomingconcerts"):
        try:
            key = setKey.title()
            sep = msg.text.split(" ")
            query =  msg.text.replace(sep[0]+" ","")
            cond = query.split("-")
            r = json.loads(requests.get(f"https://api.haipbis.xyz/upcomingconcerts").text)
            if len(cond) == 1:
                no = 0
                result = "> Upcoming Concerts"
                for reighpuy in r:
                    no += 1
                    result += "\n   ({}). {}".format(str(no), reighpuy["name"])
                result += f"\nFor More Info Using :\n\t`{key}Upcomingconcert-[number]`"
                client.sendReplyMessage(msg_id,to, result)
            elif len(cond) == 2:
                try:
                    num = int(cond[1])
                    if num <= len(r):
                        search = r[num - 1]
                        result = "> Upcoming Concert"
                        result += f"\n\tName : {search['name']}"
                        result += f"\n\tDate : {search['date']}"
                        result += f"\n\tLocation : {search['location']}"
                        result += f"\n\tLineUp : {search['lineUp']}"
                        result += f"\n\tURL : {search['link']}"
                        client.sendReplyMessage(msg_id,to, result)
                except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")
        except Exception as error:client.sendReplyMessage(msg_id,to, f"> Error : {error}")

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
        results += '\n\t{key}Error Clear'
        results += '\n\t{key}Error Look [error id]'
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
            results = '> Error Logs'
            results += '\nList :'
            parsed_len = len(errors)//200+1
            no = 0
            for point in range(parsed_len):
                for error in errors[point*200:(point+1)*200]:
                    if not error: continue
                    no += 1
                    results += '\n\t %i. %s' % (no, error)
                    if error == errors[-1]:
                        results += '\n'
                if results:
                    if results.startswith(''): results = results[1:]
                    client.sendReplyMessage(msg_id, to, results)
                results = ''
        elif cond[0].lower() == 'clear':
            filee = open('errorLog.txt', 'w')
            filee.write('')
            filee.close()
            shutil.rmtree('tmp/errors/', ignore_errors=True)
            os.system('mkdir tmp/errors')
            client.sendReplyMessage(msg_id, to, 'Error Logs is Now Clean!')
        elif cond[0].lower() == 'look':
            if len(cond) < 2:
                return client.sendReplyMessage(msg_id, to, results.format_map(SafeDict(key=setKey.title())))
            errid = cond[1]
            if os.path.exists('tmp/errors/%s.txt' % errid):
                with open('tmp/errors/%s.txt' % errid, 'r') as f:
                    client.sendReplyMessage(msg_id, to, f.read())
            else:
                return client.sendReplyMessage(msg_id, to, 'Invalid Error ID')
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

    elif cmd.startswith("info "):
        try:
            process = msg.text.split(" ")
            ordered = msg.text.replace(process[0] + " ","")
            if ordered == "antonym" or ordered == "Antonym":
                client.sendReplyMessage(msg_id,to, antonym)
            else:pass
            if ordered == "kbbi" or ordered == "Kbbi":
                client.sendReplyMessage(msg_id,to, kbbi)
            else:pass
            if ordered == "kindof" or ordered == "Kindof":
                client.sendReplyMessage(msg_id,to, kindof)
            else:pass
            if ordered == "meanslike" or ordered == "Meanslike":
                client.sendReplyMessage(msg_id,to, meanslike)
            else:pass
            if ordered == "popularnouns" or ordered == "Popularnouns":
                client.sendReplyMessage(msg_id,to, popularnouns)
            else:pass
            if ordered == "popularadjective" or ordered == "Popularadjective":
                client.sendReplyMessage(msg_id,to, popularadjective)
            else:pass
            if ordered == "synonym" or ordered == "Synonym":
                client.sendReplyMessage(msg_id,to, synonym)
            else:pass
            if ordered == "urbandict" or ordered == "Urbandict":
                client.sendReplyMessage(msg_id,to, urbandict)
            else:pass
            if ordered == "loker" or ordered == "loker":
                client.sendReplyMessage(msg_id,to, loker)
            else:pass
            if ordered == "wikipedia" or ordered == "Wikipedia":
                client.sendReplyMessage(msg_id,to, wikipedia)
            else:pass
            if ordered == "catfacts" or ordered == "Catfacts":
                client.sendReplyMessage(msg_id,to, catfacts)
            else:pass
            if ordered == "createcode" or ordered == "Createcode":
                client.sendReplyMessage(msg_id,to, createcode)
            else:pass
            if ordered == "createqr" or ordered == "Createqr":
                client.sendReplyMessage(msg_id,to, createqr)
            else:pass
            if ordered == "countryinfo" or ordered == "Countryinfo":
                client.sendReplyMessage(msg_id,to, countryinfo)
            else:pass
            if ordered == "astronomy" or ordered == "Astronomy":
                client.sendReplyMessage(msg_id,to, astronomy)
            else:pass
            if ordered == "meme" or ordered == "Meme":
                client.sendReplyMessage(msg_id,to, meme)
            else:pass
            if ordered == "searchlyrics" or ordered == "Searchlyrics":
                client.sendReplyMessage(msg_id,to, searchlyrics)
            else:pass
            if ordered == "trendtwitter" or ordered == "Trendtwitter":
                client.sendReplyMessage(msg_id,to, trendtwitter)
            else:pass
            if ordered == "upcomingconcert" or ordered == "Upcomingconcert":
                client.sendReplyMessage(msg_id,to, upcomingconcert)
            else:pass
            if ordered == "numberinfo" or ordered == "Numberinfo":
                client.sendReplyMessage(msg_id,to, numberinfo)
            else:pass
            if ordered == "randomdate" or ordered == "Randomdate":
                client.sendReplyMessage(msg_id,to, randomdate)
            else:pass
            if ordered == "randomquote" or ordered == "Randomquote":
                client.sendReplyMessage(msg_id,to, randomquote)
            else:pass
            if ordered == "randomyear" or ordered == "Randomyear":
                client.sendReplyMessage(msg_id,to, randomyear)
            else:pass
            if ordered == "translate" or ordered == "translate":
                client.sendReplyMessage(msg_id,to, translate)
            else:pass
            if ordered == "surah" or ordered == "Surah":
                client.sendReplyMessage(msg_id,to, surah)
            else:pass
            if ordered == "ytsearch" or ordered == "Ytsearch":
                client.sendReplyMessage(msg_id,to, ytsearch)
            else:pass
            if ordered == "github" or ordered == "Github":
                client.sendReplyMessage(msg_id,to, github)
            else:pass
            if ordered == "quotes" or ordered == "quotes":
                client.sendReplyMessage(msg_id,to, quotes)
            else:pass
            if ordered == "playstore" or ordered == "Playstore":
                client.sendReplyMessage(msg_id,to, playstore)
            else:pass
            if ordered == "tvchannel" or ordered == "Tvchannel":
                client.sendReplyMessage(msg_id,to, tvchannel)
            else:pass
            if ordered == "postcode" or ordered == "postcode":
                client.sendReplyMessage(msg_id,to, postcode)
            else:pass
            if ordered == "foximage" or ordered == "Foximage":
                client.sendReplyMessage(msg_id,to, foximage)
            else:pass
            if ordered == "catimage" or ordered == "Catimage":
                client.sendReplyMessage(msg_id,to, catimage)
            else:pass
            if ordered == "dogimage" or ordered == "Dogimage":
                client.sendReplyMessage(msg_id,to, dogimage)
            else:pass
            if ordered == "footballstreams" or ordered == "Footballstreams":
                client.sendReplyMessage(msg_id,to, footballstreams)
            else:pass
            if ordered == "hexcolor" or ordered == "Hexcolor":
                client.sendReplyMessage(msg_id,to, hexcolor)
            else:pass
            if ordered == "ipinfo" or ordered == "Ipinfo":
                client.sendReplyMessage(msg_id,to, ipinfo)
            else:pass
            if ordered == "newton" or ordered == "Newton":
                client.sendReplyMessage(msg_id,to, newton)
            else:pass
        except Exception as error:client.sendReplyMessage(msg_id,to, error)

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
    print ('[ System Message : *PROGRAM HAS BEEN STARTED.\n______________________________\n')
    runningProgram()
