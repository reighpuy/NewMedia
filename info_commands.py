from important import *
from module import *
from setup_args import *

settings = livejson.File('setting.json', True, False, 4)
bool_dict = {
    True: ['Yes', 'Aktif', 'Sukses', 'Open', 'On'],
    False: ['No', 'Tidak Aktif', 'Gagal', 'Close', 'Off']
}
key = settings['setKey']['key'].title()

antonym = f"Usage : {key}antonym [word]\n\t  Example : {key}Antonym Bad\n\tWhos can use this Command? : Admin & Non-Admin"
kbbi = f"Usage : {key}Kbbi [kata]\n\t  Example : {key}Kbbi tidur\n\tWhos can use this Command? : Admin & Non-Admin"
kindof = f"Usage : {key}Kindof [word]\n\t  Example : {key}Kindof Cow\n\tWhos can use this Command? : Admin & Non-Admin"
meanslike = f"Usage : {key}Meanslike [word]\n\t  Example : {key}Meanslike rose\n\tWhos can use this Command? : Admin & Non-Admin"
popularnouns = f"Usage : {key}Popularnouns [word]\n\t  Example : {key}Popularnouns Cow\n\tWhos can use this Command? : Admin & Non-Admin"
popularadjective = f"Usage : {key}Popularadjective [word]\n\t  Example : {key}Popularadjective Cow\n\tWhos can use this Command? : Admin & Non-Admin"
synonym = f"Usage : {key}Synonym [word]\n\t  Example : {key}Synonym Cow\n\tWhos can use this Command? : Admin & Non-Admin"
urbandict = f"Usage : {key}Urbandict [word]\n\tWhos can use this Command? : Admin & Non-Admin"
foximage = f"Usage : {key}Foximage\n\tWhos can use this Command? : Admin & Non-Admin"
catimage = f"Usage : {key}Catimage\n\tWhos can use this Command? : Admin & Non-Admin"
dogimage = f"Usage : {key}Dogimage\n\tWhos can use this Command? : Admin & Non-Admin"
postcode = f"Usage : {key}Postcode [code]\n\t  Example : {key}Postcode 16444\nWhos can use this Command? : Admin & Non-Admin"
translate = f"Usage : {key}Tr-id [Text]\n\t  Example : {key}Tr-id Hello World\nWhos can use this Command? : Admin & Non-Admin"
wikipedia = f"Usage : {key}Wikipedia\n\tWhos can use this Command? : Admin & Non-Admin"
breakingbad = f"Usage : {key}Breakingbad quote\n\tWhos can use this Command? : Admin & Non-Admin"
footballstreams = f"Usage : {key}Footballstreams\n\tWhos can use this Command? : Admin & Non-Admin"
hexcolor = f"Usage : {key}Hexcolor [Code]\n\t  Example : {key}Hexcolor FFFFFF\nWhos can use this Command? : Admin & Non-Admin"
loker = f"Usage : {key}Loker [City/Kota]\n\t  Example : {key}Loker Jakarta\nWhos can use this Command? : Admin & Non-Admin"
ipinfo = f"Usage : {key}IPpinfo [ip]\n\t  Example : {key}Ipinfo 68.68.68.68\nWhos can use this Command? : Admin & Non-Admin"
newton = f"Usage : {key}Newton [factor]\n\t  Example : {key}Newton x^2-1\nWhos can use this Command? : Admin & Non-Admin"
catfacts = f"Usage : {key}cat facts\n\tWhos can use this Command? : Admin & Non-Admin"
createcode = f"Usage : {key}createcode [text]\n\tWhos can use this Command? : Admin & Non-Admin"
createqr = f"Usage : {key}createqr [text]\n\tWhos can use this Command? : Admin & Non-Admin"
countryinfo = f"Other Information of Country : \n\tExample : {key}Capital id\n\tExample : {key}Region id\n\tExample : {key}Subregion id\n\tExample : {key}Timezone id\n\tExample : {key}Nativename id\n\tExample : {key}Numericcode id\n\tExample : {key}Population id\n\tExample : {key}Callingcode id\n\tExample : {key}Currenciesname id\n\tExample : {key}Currenciescode id\n\tExample : {key}currenciessymbol id\n\nUsage : {key}Countryinfo [country_code]\n\t  Example : {key}Countryinfo id\n\tWhos can use this Command? : Admin & Non-Admin"
astronomy = f"Usage : {key}Astronomy\n\tWhos can use this Command? : Admin & Non-Admin"
meme = f"Usage : {key}Meme/[Template_Name]/[text1]/[text2]\n\t  Example : {key}Meme/Live/Hello/World\n\tWhos can use this Command? : Admin & Non-Admin"
searchlyrics = f"Usage : {key}Searchlyrics [songname & artistname]\n\t  Example : {key}Searchlyrics fix you coldplay\n\tWhos can use this Command? : Admin & Non-Admin"
trendtwitter = f"Usage : {key}Trendtwitter\n\tWhos can use this Command? : Admin & Non-Admin"
upcomingconcert = f"Usage : {key}Upcomingconcert\n\tWhos can use this Command? : Admin & Non-Admin"
numberinfo = f"Usage : {key}Numberinfo [number]\n\t  Example : {key}Number 18\n\tWhos can use this Command? : Admin & Non-Admin"
randomdate = f"Usage : {key}Random date\n\tWhos can use this Command? : Admin & Non-Admin"
randomyear = f"Usage : {key}Random Year\n\tWhos can use this Command? : Admin & Non-Admin"
quotes = f"Usage : {key}Quotes\n\tWhos can use this Command? : Admin & Non-Admin"
surah = f"Usage : {key}Surah [nomor]\n\t  Example : {key}Surah 18\n\tWhos can use this Command? : Admin & Non-Admin"
ytsearch = f"Usage : {key}Ytsearch\n\t Example : {key}Ytsearch kekeyi\n\tWhos can use this Command? : Admin & Non-Admin"
github = f"Usage : {key}Github\n\tWhos can use this Command? : Admin & Non-Admin"
playstore = f"Usage : {key}Playstore\n\t Example : {key}Playstore line\n\tWhos can use this Command? : Admin & Non-Admin"
tvchannel = f"Usage : {key}Tvchannel\n\t Example : {key}Tvchannel antv\n\tWhos can use this Command? : Admin & Non-Admin"
