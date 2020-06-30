from important import *
from module import *
from setup_args import *

settings = livejson.File('setting.json', True, False, 4)
bool_dict = {
    True: ['Yes', 'Aktif', 'Sukses', 'Open', 'On'],
    False: ['No', 'Tidak Aktif', 'Gagal', 'Close', 'Off']
}

def helpmessage():
    if settings['setKey']['status'] == True:
        key = settings['setKey']['key'].title()
    else:
        key = ''
    helpMessage ="> General" + "\n" + \
                    "Prefix : ( " + key + " )\n\t" + \
                    " (-). Author" + "\n\t" + \
                    " (-). LiffLink" + "\n\t" + \
                    " (-). Myprofile" + "\n\n" + \
                    "> Media" + "\n\t" + \
                    " (-). Dictionary" + "\n\t" + \
                    " (-). Utility" + "\n\t" + \
                    " (-). Avataredit"
    return helpMessage

def helpdictionary():
    if settings['setKey']['status'] == True:
        key = settings['setKey']['key'].title()
    else:
        key = 'No Prefix'
    helpDictionary ="> Dictionary Command List" + "\n" + \
                    "Prefix : ( " + key + " )\n\t" + \
                    " (-). Antonym" + "\n\t" + \
                    " (-). Kbbi" + "\n\t" + \
                    " (-). Kindof" + "\n\t" + \
                    " (-). Meanslike" + "\n\t" + \
                    " (-). Popularnouns" + "\n\t" + \
                    " (-). Popularadjective" + "\n\t" + \
                    " (-). Synonym" + "\n\t" + \
                    " (-). Urbandict" + "\n\t" + \
                    " (-). Wikipedia"
    return helpDictionary

def helputility():
    if settings['setKey']['status'] == True:
        key = settings['setKey']['key'].title()
    else:
        key = 'No Prefix'
    helpUtility ="> Utility Command Lists" + "\n" + \
                    "Prefix : ( " + key + " )\n\t" + \
                    " (-). Apod" + "\n\t" + \
                    " (-). Catimage" + "\n\t" + \
                    " (-). Catfacts" + "\n\t" + \
                    " (-). Countryinfo" + "\n\t" + \
                    " (-). CreateCode" + "\n\t" + \
                    " (-). CreateQr" + "\n\t" + \
                    " (-). Dogimage" + "\n\t" + \
                    " (-). Foximage" + "\n\t" + \
                    " (-). Github" + "\n\t" + \
                    " (-). Meme" + "\n\t" + \
                    " (-). Number" + "\n\t" + \
                    " (-). Playstore" + "\n\t" + \
                    " (-). RandomDate" + "\n\t" + \
                    " (-). RandomQuote" + "\n\t" + \
                    " (-). RandomYear" + "\n\t" + \
                    " (-). SearchLyrics" + "\n\t" + \
                    " (-). Surah" + "\n\t" + \
                    " (-). TongueTwister" + "\n\t" + \
                    " (-). Trendtwitter" + "\n\t" + \
                    " (-). UpcomingConcert" + "\n\t" + \
                    " (-). Tvchannel" + "\n\t" + \
                    " (-). Ytsearch"
    return helpUtility

def helpavataredit():
    if settings['setKey']['status'] == True:
        key = settings['setKey']['key'].title()
    else:
        key = 'No Prefix'
    helpAvataredit ="> AvatarEdits Command List" + "\n" + \
                    "Prefix : ( " + key + " )\n\t" + \
                    " (-). Adjust" + "\n\t" + \
                    " (-). Blur" + "\n\t" + \
                    " (-). Circular" + "\n\t" + \
                    " (-). Decopacity" + "\n\t" + \
                    " (-). Filter1" + "\n\t" + \
                    " (-). Filter2" + "\n\t" + \
                    " (-). Filter3" + "\n\t" + \
                    " (-). Grayscale" + "\n\t" + \
                    " (-). Outline" + "\n\t" + \
                    " (-). Oilpaint" + "\n\t" + \
                    " (-). Rotate" + "\n\t" + \
                    " (-). Recolor" + "\n\t" + \
                    " (-). Shadow"
    return helpAvataredit

def helpmemegen():
    if settings['setKey']['status'] == True:
        key = settings['setKey']['key'].title()
    else:
        key = 'No Prefix'
    helpMemegen ="> Meme Templates" + "\n" + \
                    "10 Guy | name = tenguy" + "\n\t" + \
                    "Afraid to Ask Andy | name = afraid" + "\n\t" + \
                    "Almost Politically Correct Redneck | name = apcr" + "\n\t" + \
                    "An Older Code Sir, But It Checks Out | name = older" + "\n\t" + \
                    "Ancient Aliens Guy | name = aag" + "\n\t" + \
                    "And Then I Said | name = atis" + "\n\t" + \
                    "At Least You Tried | name = tried" + "\n\t" + \
                    "Baby Insanity Wolf | name = biw" + "\n\t" + \
                    "Baby, You've Got a Stew Going | name = stew" + "\n\t" + \
                    "Bad Luck Brian | name = blb" + "\n\t" + \
                    "But It's Honest Work | name = bihw" + "\n\t" + \
                    "But That's None of My Business | name = kermit" + "\n\t" + \
                    "Butthurt Dweller | name = bd" + "\n\t" + \
                    "Captain Hindsight | name = ch" + "\n\t" + \
                    "Comic Book Guy | name = cbg" + "\n\t" + \
                    "Condescending Wonka | name = wonka" + "\n\t" + \
                    "Confession Bear | name = cb" + "\n\t" + \
                    "Confused Gandalf | name = gandalf" + "\n\t" + \
                    "Conspiracy Keanu | name = keanu" + "\n\t" + \
                    "Crying on Floor | name = cryingfloor" + "\n\t" + \
                    "Dating Site Murderer | name = dsm" + "\n\t" + \
                    "Disaster Girl | name = disastergirl" + "\n\t" + \
                    "Do It Live! | name = live" + "\n\t" + \
                    "Do You Want Ants? | name = ants" + "\n\t" + \
                    "Doge | name = doge" + "\n\t" + \
                    "Donald Trump | name = trump" + "\n\t" + \
                    "Drakeposting | name = drake" + "\n\t" + \
                    "Ermahgerd | name = ermg" + "\n\t" + \
                    "Facepalm | name = facepalm" + "\n\t" + \
                    "Feels Good | name = feelsgood" + "\n\t" + \
                    "First Try! | name = firsttry" + "\n\t" + \
                    "First World Problems | name = fwp" + "\n\t" + \
                    "Forever Alone | name = fa" + "\n\t" + \
                    "Foul Bachelor Frog | name = fbf" + "\n\t" + \
                    "Fuck Me, Right? | name = fmr" + "\n\t" + \
                    "Futurama Fry | name = fry" + "\n\t" + \
                    "Good Guy Greg | name = ggg" + "\n\t" + \
                    "Grumpy Cat | name = grumpycat" + "\n\t" + \
                    "Hide the Pain Harold | name = harold" + "\n\t" + \
                    "Hipster Barista | name = hipster" + "\n\t" + \
                    "I Can Has Cheezburger? | name = icanhas" + "\n\t" + \
                    "I Feel Like I'm Taking Crazy Pills | name = crazypills" + "\n\t" + \
                    "I Guarantee It | name = mw" + "\n\t" + \
                    "I Have No Idea What I'm Doing | name = noidea" + "\n\t" + \
                    "I Immediately Regret This Decision! | name = regret" + "\n\t" + \
                    "I Should Buy a Boat Cat | name = boat" + "\n\t" + \
                    "I Should Not Have Said That | name = hagrid" + "\n\t" + \
                    "I Would Be So Happy | name = sohappy" + "\n\t" + \
                    "I am the Captain Now | name = captain" + "\n\t" + \
                    "I'm Going to Build My Own Theme Park | name = bender" + "\n\t" + \
                    "Inigo Montoya | name = inigo" + "\n\t" + \
                    "Insanity Wolf | name = iw" + "\n\t" + \
                    "It's A Trap! | name = ackbar" + "\n\t" + \
                    "It's Happening | name = happening" + "\n\t" + \
                    "It's Simple, Kill the Batman | name = joker" + "\n\t" + \
                    "Jony Ive Redesigns Things | name = ive" + "\n\t" + \
                    "Joseph Ducreux / Archaic Rap | name = jd" + "\n\t" + \
                    "Laughing Lizard | name = ll" + "\n\t" + \
                    "Laundry Room Viking | name = lrv" + "\n\t" + \
                    "Leo Strutting | name = leo" + "\n\t" + \
                    "Life... Finds a Way | name = away" + "\n\t" + \
                    "Matrix Morpheus | name = morpheus" + "\n\t" + \
                    "Member Berries | name = mb" + "\n\t" + \
                    "Milk Was a Bad Choice | name = badchoice" + "\n\t" + \
                    "Mini Keanu Reeves | name = mini-keanu" + "\n\t" + \
                    "Minor Mistake Marvin | name = mmm" + "\n\t" + \
                    "Mocking Spongebob | name = spongebob" + "\n\t" + \
                    "No Soup for You / Soup Nazi | name = soup-nazi" + "\n\t" + \
                    "Nothing To Do Here | name = jetpack" + "\n\t" + \
                    "Oh, I'm Sorry, I Thought This Was America | name = imsorry" + "\n\t" + \
                    "Oh, Is That What We're Going to Do Today? | name = red" + "\n\t" + \
                    "One Does Not Simply Walk into Mordor | name = mordor" + "\n\t" + \
                    "Oprah You Get a Car | name = oprah" + "\n\t" + \
                    "Overly Attached Girlfriend | name = oag" + "\n\t" + \
                    "Pepperidge Farm Remembers | name = remembers" + "\n\t" + \
                    "Persian Cat Room Guardian | name = persian" + "\n\t" + \
                    "Philosoraptor | name = philosoraptor" + "\n\t" + \
                    "Probably Not a Good Idea | name = jw" + "\n\t" + \
                    "Push it somewhere else Patrick | name = patrick" + "\n\t" + \
                    "Roll Safe | name = rollsafe" + "\n\t" + \
                    "Sad Barack Obama | name = sad-obama" + "\n\t" + \
                    "Sad Bill Clinton | name = sad-clinton" + "\n\t" + \
                    "Sad Frog / Feels Bad Man | name = sadfrog" + "\n\t" + \
                    "Sad George Bush | name = sad-bush" + "\n\t" + \
                    "Sad Joe Biden | name = sad-biden" + "\n\t" + \
                    "Sad John Boehner | name = sad-boehner" + "\n\t" + \
                    "Salt Bae | name = saltbae" + "\n\t" + \
                    "Sarcastic Bear | name = sarcasticbear" + "\n\t" + \
                    "Schrute Facts | name = dwight" + "\n\t" + \
                    "Scumbag Brain | name = sb" + "\n\t" + \
                    "Scumbag Steve | name = ss" + "\n\t" + \
                    "Seal of Approval | name = soa" + "\n\t" + \
                    "Sealed Fate | name = sf" + "\n\t" + \
                    "See? Nobody Cares | name = dodgson" + "\n\t" + \
                    "Shut Up and Take My Money! | name = money" + "\n\t" + \
                    "Skeptical Snake | name = snek" + "\n\t" + \
                    "Skeptical Third World Kid | name = sk" + "\n\t" + \
                    "So Hot Right Now | name = sohot" + "\n\t" + \
                    "So I Got That Goin' For Me, Which is Nice | name = nice" + "\n\t" + \
                    "Socially Awesome Awkward Penguin | name = awesome-awkward" + "\n\t" + \
                    "Socially Awesome Penguin | name = awesome" + "\n\t" + \
                    "Socially Awkward Awesome Penguin | name = awkward-awesome" + "\n\t" + \
                    "Socially Awkward Penguin | name = awkward" + "\n\t" + \
                    "Stop It, Get Some Help | name = stop-it" + "\n\t" + \
                    "Stop Trying to Make Fetch Happen | name = fetch" + "\n\t" + \
                    "Success Kid | name = success" + "\n\t" + \
                    "Sudden Clarity Clarence | name = scc" + "\n\t" + \
                    "Super Cool Ski Instructor | name = ski" + "\n\t" + \
                    "Sweet Brown / Ain't Nobody Got Time For That | name = aint-got-time" + "\n\t" + \
                    "That Would Be Great | name = officespace" + "\n\t" + \
                    "The Most Interesting Man in the World | name = interesting" + "\n\t" + \
                    "The Rent Is Too Damn High | name = toohigh" + "\n\t" + \
                    "This is Bull, Shark | name = bs" + "\n\t" + \
                    "This is Fine | name = fine" + "\n\t" + \
                    "This is Sparta! | name = sparta" + "\n\t" + \
                    "Ugandan Knuckles | name = ugandanknuck" + "\n\t" + \
                    "Unpopular opinion puffin | name = puffin" + "\n\t" + \
                    "What Year Is It? | name = whatyear" + "\n\t" + \
                    "What is this, a Center for Ants?! | name = center" + "\n\t" + \
                    "Why Not Both? | name = both" + "\n\t" + \
                    "Winter is coming | name = winter" + "\n\t" + \
                    "X all the Y | name = xy" + "\n\t" + \
                    "X, X Everywhere | name = buzz" + "\n\t" + \
                    "Xzibit Yo Dawg | name = yodawg" + "\n\t" + \
                    "Y U NO Guy | name = yuno" + "\n\t" + \
                    "Y'all Got Any More of Them | name = yallgot" + "\n\t" + \
                    "You Know What Really Grinds My Gears? | name = gears" + "\n\t" + \
                    "You Should Feel Bad | name = bad" + "\n\t" + \
                    "You Sit on a Throne of Lies | name = elf" + "\n\t" + \
                    "You Were the Chosen One! | name = chosen"
    return helpMemegen
