from bs4 import BeautifulSoup
import csv
import os
import spacy
from spacy.lang.en import English
from spacy.matcher import PhraseMatcher
nlp = English()

#Inspired by: https://github.com/kheslin0420/kheslin0420.github.io/blob/master/audit-collection-descriptions.py
#Modified from: https://gist.github.com/noahgh221/6aa54bfbcf16b312b56181866fba6631#file-description_audit_ead-py

#Path to DCs
path = 'C:/Users/u6045253/Desktop/Audit Test'
csv_path = 'C:/Users/u6045253/Desktop/Audit Test/test.csv'

nlp = spacy.load('en_core_web_sm')
matcher = PhraseMatcher(nlp.vocab, attr='LOWER')

#HateBase Full English Term List from API: see: https://hatebase.org/about
phrase_list_hatebase = ['Paedo', 'Hodgie', 'sand ape', 'islamization', 'porki', 'halalability', 'halal', 'halalification', 'Muzrat', 'Towelhead', 'osama', 'lobby gay', 'mongoloid', 'sandnigger', 'Bengali', 'rapefugees', 'Girl', 'whitie', 'fish wagon', 'skank', 'gun burglar', 'gun burglars', 'kanaka', 'cracker', 'ABCs', 'ABC', 'rube', 'whoriental', 'whorientals', 'hoosier', 'hooknoses', 'hooknosed', 'hooknose', 'dagowops', 'dagowop', 'chimp-outs', 'bean bandit', 'bean bandits', 'lipstick lesbians', 'libtard', 'jihadi-americans', 'jihadi-american', 'gyppoes', 'gypoes', 'gooky eyes', 'gooklets', 'gooklet', 'gookettes', 'gookette', 'gook eyed', 'ghetto monkeys', 'ghetto monkey', 'filthypinos', 'filthypinoes', 'filthypino', 'deminigger', 'deminiggers', 'seminigger', 'seminiggers', 'canniglets', 'canigglet', 'caniggers', 'canigger', 'cairo coons', 'cairo coon', 'bushniglets', 'bushniglet', 'bushniggers', 'bushnigger', 'bush bandits', 'bush bandit', 'border bandits', 'border banditos', 'border bandit', 'border banditoes', "african't", "african'ts", 'WASPy', 'Uncle Tom', 'jewtarded', 'jigaboo', 'jewtard', 'cunt', 'twat', 'spicks', 'mud ducks', 'mangia cakes', 'lawn jockeys', 'limey', 'limeys', 'honky', 'honkey', 'hebes', 'hillbillies', 'hayseed', 'half breeds', 'greaseball', 'gypped', 'gyp', 'dot heads', 'Paedo', 'Hodgie', 'sand ape', 'islamization', 'porki', 'halalability', 'halal', 'halalification', 'Muzrat', 'Towelhead', 'osama', 'lobby gay', 'mongoloid', 'sandnigger', 'Bengali', 'rapefugees', 'Girl', 'whitie', 'fish wagon', 'skank', 'gun burglar', 'gun burglars', 'kanaka', 'cracker', 'ABCs', 'ABC', 'rube', 'whoriental', 'whorientals', 'hoosier', 'hooknoses', 'hooknosed', 'hooknose', 'dagowops', 'dagowop', 'chimp-outs', 'bean bandit', 'bean bandits', 'lipstick lesbians', 'libtard', 'jihadi-americans', 'jihadi-american', 'gyppoes', 'gypoes', 'gooky eyes', 'gooklets', 'gooklet', 'gookettes', 'gookette', 'gook eyed', 'ghetto monkeys', 'ghetto monkey', 'filthypinos', 'filthypinoes', 'filthypino', 'deminigger', 'deminiggers', 'seminigger', 'seminiggers', 'canniglets', 'canigglet', 'caniggers', 'canigger', 'cairo coons', 'cairo coon', 'bushniglets', 'bushniglet', 'bushniggers', 'bushnigger', 'bush bandits', 'bush bandit', 'border bandits', 'border banditos', 'border bandit', 'border banditoes', "african't", "african'ts", 'WASPy', 'Uncle Tom', 'jewtarded', 'jigaboo', 'jewtard', 'cunt', 'twat', 'spicks', 'mud ducks', 'mangia cakes', 'lawn jockeys', 'limey', 'limeys', 'honky', 'honkey', 'hebes', 'hillbillies', 'hayseed', 'half breeds', 'greaseball', 'gypped', 'gyp', 'dot heads', 'whores', 'whore', 'mammy', 'muslamic', 'gypsy', 'gypsies', 'gyps', 'yokels', 'yokel', 'yellow bone', 'red bone', 'white trash', 'trailer trash', 'trailer park trash', 'shyster', 'shysters', 'sheister', 'sheisters', 'peckerwood', 'sheepfucker', 'niggah', 'nigga', 'niggahs', 'niggas', 'newfies', 'newfie', 'hosers', 'hillbilly', 'eurotrash', 'dyke', 'slut', 'sluts', 'spinks', 'mooks', 'mook', 'krauts', 'jiggs', 'jigg', 'jiggers', 'jigger', 'jiggas', 'jigga', 'hebe', 'half breed', 'eshay', 'eshays', 'Gwats', 'Gwat', 'gub', 'gubs', 'buffies', 'pussy', 'niggers', 'nigger', 'hoser', 'gorillla', 'meatball patriots', 'meatball patriot', 'feminazis', 'feminazi', '6 gorillion', 'mocks', 'injun', 'Anglo Fool', 'boujees', 'boujee', 'floppies', 'floppy', 'nigger-rig', 'half bred', 'gookies', 'gookie', 'goloids', 'goloid', 'ginks', 'gink', 'gas huffers', 'gas huffer', 'featherheads', 'featherhead', 'border bandito', 'boogats', 'boogat', 'dog eaters', 'dog eater', 'alboes', 'albos', 'albo', 'jipsi', 'gypsi', 'Chad Thundercocks', 'Chads', 'Chad Thundercock', 'Chad', 'bimbo', 'himbo', 'machosexual', 'gopniks', 'skeets', 'skeet', 'dresiarz', 'dres', 'gopnik', 'Freḥa', 'arsit', 'arsim', 'ars', 'Sloane Rangers', 'Sloane Ranger', 'Hoorah Henriettas', 'Hoorah Henrietta', 'Hooray Henriettas', 'Hooray Henrietta', 'Hoorah Henries', 'Hoorah Henry', 'Hooray Henries', 'Hooray Henry', 'toffs', 'toff', 'gey', 'yellow cabs', 'yellow cab', 'lipstick lesbian', 'zhidovka', 'zhydovka', 'zhid', 'zhyd', 'virago', 'cock tease', 'Beckies', 'Beckys', 'Becky', 'bull dykes', 'bull dyke', 'lavender mafia', 'velvet mafia', 'gay mafia', 'Homintern', 'batimen', 'batiman', 'battymen', 'battyman', 'chi chi bwoys', 'chi chi bwoy', 'chi chi men', 'chi chi man', 'batty men', 'batty man', 'batty bwoys', 'batty bwoy', 'batty boys', 'batty boy', 'papishers', 'papisher', 'gingettes', 'gingette', 'good goys', 'gheys', 'fruities', 'flipettes', 'flipette', 'fagdicks', 'fagdick', 'fagshits', 'fagshit', 'dinkladies', 'dinklady', 'durka durkas', 'durka durka', 'derka derkas', 'degettes', 'degette', 'dagettes', 'dagette', 'closet dykes', 'closet dyke', 'black dagoes', 'border baby', 'border babies', 'chavettes', 'chavette', 'carrot snaps', 'carrot snap', 'buckrettes', 'buckrette', 'gingies', 'gingie', 'gingy', 'gasher', 'fruity', 'cunter', 'chimp packs', 'Charly', 'Charlies', 'buffy', 'buckers', 'bucker', 'ban and can', 'cans and bans', 'can and ban', 'Annies', 'cohees', 'cohee', 'yellowhammer', 'Okies', 'Okie', 'Massholes', 'Masshole', 'Madrasi', 'JAFAs', 'JAFA', 'jackeens', 'jackeen', 'culchies', 'culchie', 'croweaters', 'croweater', 'Biharis', 'Bihari', 'hatzis', 'hatzi', 'hajjis', 'hajis', 'hadjis', 'hajji', 'haji', 'hadji', 'mussies', 'mussie', 'Fenians', 'Fenian', 'da goyim know', 'the goyim know', 'good goy', 'jigros', 'pickinninys', 'piccaninnys', 'piccaninnies', 'picaninnys', 'pickaninnies', 'pickinninies', 'pickinniny', 'piccaninny', 'picaninnies', 'picaninny', 'Zio', 'tynker', 'tree jumper', 'tinkar', 'tinkere', 'tincker', 'spink', 'spik', 'spig', 'spick', 'spaz', 'smoke jumper', 'slopey', 'slags', 'shit kicker', 'shit heel', 'shant', 'seppo', 'sawney', 'rubes', 'poppadom', 'nitchy', 'nichiwa', 'negro', 'neejee', 'nitchie', 'neechee', 'mong', 'sheeny', 'niggerdick', 'niggerdicks', 'niggerton', 'niggertown', 'niggerville', 'retarded', 'shekelnose', 'lefty', 'kikesberg', 'jigroes', 'jigro', 'hoodrats', 'hoodrat', 'golliwog', 'pisslam', 'Ahab', 'dinks', 'dink', 'bans and cans', 'muslimic', 'gender nigger', 'dot head', 'dogan', 'cripples', 'chinks', 'boojie', 'black dago', 'bitches', 'bitch', 'jit', 'toad', 'khazar', 'Zionazi', 'kike', 'sand niglet', 'sand niglets', 'Zionazis', 'zipperheads', 'zippoheads', 'zips', 'ZOG lovers', 'zebras', 'zigabos', 'ziojews', 'yellow invaders', 'yellows', 'yids', 'yobbos', 'yobs', 'Yanks', 'yard apes', 'yardies', 'yellow bones', 'wogs', 'wops', 'wopspeak', 'Yankees', 'wiggas', 'wiggerettes', 'wiggers', 'winks', 'whiggers', 'white niggers', 'whities', 'WICs', 'wegroes', 'wetbacks', 'wexicans', 'whiggas', 'WASPs', 'uncircumcised baboons', 'Uncle Toms', 'Velcro heads', 'wagon burners', 'tynkers', 'Ubangees', 'Ubangis', 'tyncars', 'tynekeres', 'tynkards', 'tynkares', 'tynkeres', 'tree niggers', 'tunnel diggers', 'twats', 'Twinkies', 'towel heads', 'trannies', 'tree jumpers', 'tinkars', 'tinkeres', 'tinkers', 'Tommies', 'tigers', 'timber niggers', 'tinckers', 'tinkards', 'teapots', 'tenkers', 'tard', 'tarded', 'tards', 'teabaggers', 'suntans', 'taco niggers', 'Taffys', 'tans', 'tar babies', 'squinties', 'steeks', 'stovepipes', 'stump jumpers', 'spivs', 'spooks', 'squareheads', 'squaws', 'spiggotties', 'spigs', 'spikes', 'spiks', 'spicspeak', 'spides', 'spiggers', 'spickish', 'spiclet', 'spics', 'spicish', 'spickaboos', 'spades', 'spear chuckers', 'spergs', 'spice niggers', 'snowflakes', 'soles', 'sooties', 'soup takers', 'Southern fairies', 'smoke jumpers', 'smoked Irishmen', 'snouts', 'slopes', 'slopies', 'smicks', 'slants', 'slaves', 'slits', 'slopeheads', 'Skippies', 'Skips', 'slant eyes', 'sideways vaginas', 'skags', 'skangers', 'skinnie', 'skinnies', 'shit kickers', 'sideways cooters', 'sideways pussies', 'shiners', 'shines', 'shit heels', 'Sheltas', 'shemales', 'sheboons', 'sheenies', 'sheepfuckers', 'sengas', 'seppos', 'septics', 'shades', 'shants', 'scobes', 'scuffers', 'semiholes', 'sawnies', 'scags', 'scallies', 'scangers', 'sand nips', 'sand niggerette', 'sand niggerettes', 'sand niggers', 'Russellites', 'sambos', 'sand monkey', 'sand monkeys', 'rice niggers', 'ricepickers', 'roofuckers', 'roundeyes', 'Rhine monkeys', 'Rhineland bastard', 'Rhineland bastards', 'red niggers', 'rednecks', 'redskins', 'retardeds', 'retards', 'race traitors', 'ragheads', 'red bones', 'quadroons', 'quashies', 'queens', 'queers', 'proddy dogs', 'proddywhoddies', 'proddywoddies', 'prods', 'pussies', 'prairie niggers', 'poms', 'popolos', 'poppadoms', 'porch monkeys', 'powderburns', 'polacks', 'pollos', 'pommie grants', 'pommies', 'pohms', 'pointy heads', 'pineapple niggers', 'ping pangs', 'pintos', 'plastic paddies', 'pogues', 'Pepsis', 'pickaninnys', 'pikers', 'pikeys', 'papists', 'papooses', 'pavement apes', 'peckerwoods', 'Peppers', 'pancake faces', 'pancakes', 'pakis', 'palefaces', 'Orientals', 'oven dodgers', 'paddies', 'Pakiland', 'Orangies', 'Oreos', 'ockers', 'octaroons', 'octroons', 'ofays', 'nips', 'nitchees', 'nitchies', 'Northern monkeys', 'nigras', 'nigres', 'nigs', 'niglette', 'nigors', 'nigguhs', 'niggurs', 'niglets', 'niggerization', 'nigglets', 'niggors', 'niggars', 'niggerettes', 'nigars', 'nigers', 'nigettes', 'niccas', 'nichis', 'nichiwas', 'nidges', 'nig nogs', 'net heads', 'neds', 'neechees', 'neejees', 'nafris', 'neches', 'mutts', 'muzzies', 'muzzpigs', 'muzzrats', 'nachos', 'mullatoes', 'mungs', 'munters', 'munts', 'muks', 'muktuks', 'mulatto', 'mulignans', 'mud persons', 'mud sharks', 'moulinyans', 'moxies', 'MTNs', 'moss eaters', 'mossheads', 'moulies', 'moulignons', 'moolinyan', 'moon crickets', 'Moors', 'mokies', 'mongols', 'mongs', 'monkeys', 'mokes', 'mochs', 'mockeys', 'mockies', 'Mickey Finns', 'mickeys', 'micks', 'mil bags', 'millies', 'Merkins', 'lubras', 'lugans', 'mackerel snappers', 'macks', 'leprechauns', 'ling lings', 'lowlanders', 'Lebbos', 'Lebs', 'lefties', 'lemonheads', 'Kushis', 'Kushites', 'kykes', 'latrinos', 'kunt', 'kikes', 'knackers', 'kneegroes', 'kotiyas', 'khazars', 'jijjiboos', 'Jits', 'jockies', 'jocks', 'jungle bunnys', 'jigs', 'Jihadis', 'jiggaboos', 'jiggabos', 'jigaboos', 'jigaroonis', 'jewbagg', 'jhants', 'Japs', 'Jerries', 'jew-fucked', 'jants', 'japies', 'Japland', 'island niggers', 'ikeys', 'injuns', 'ice monkeys', 'ice niggers', 'idiots', 'ikes', 'ikey mos', 'Huns', 'Hunyaks', 'Hunyocks', 'hymies', 'hos', 'house niggers', 'Hunkies', 'Honyaks', 'Honyocks', 'hoosiers', 'hories', 'hoes', 'honkeye', 'honkies', 'honklets', 'hicks', 'higgers', 'hayseeds', 'hebros', 'heebs', 'heinies', 'hairybacks', 'halfricans', 'gypos', 'gyppies', 'gyppos', 'guineas', 'gurriers', 'gualas', 'gubbas', 'guidettes', 'guidos', 'gooks', 'greaseballs', 'greasers', 'groids', 'guala gualas', 'globalists', 'golliwogs', 'goobers', 'gook eyes', 'gins', 'ginzos', 'gippos', 'gipps', 'ghosts', 'gimps', 'gimpy', 'gin jockeys', 'gingers', 'gender benders', 'Gerudos', 'gews', 'ghetto hamsters', 'ghey', 'fuzzy wuzzies', 'gables', 'gashes', 'gaylord', 'gaylords', 'fuzzies', 'frogs', 'fruits', 'fudgepackers', 'FOBs', 'fog niggers', 'four by twos', 'fezzes', 'flipabeanos', 'flips', 'fags', 'fairies', 'eyeties', 'fagbags', 'faggots', 'faggy', 'dyke jumpers', 'dykes', 'eggs', 'eh holes', 'eight balls', 'dole bludgers', 'dune coons', 'dune niggers', 'divs', 'divvies', 'dogans', 'doguns', 'dhimmis', 'diaper heads', 'dindu', 'dinges', 'dingo fuckers', 'Cushites', 'dagos', 'darkies', 'degos', 'curry munchers', 'curry slurpers', 'curry stinkers', 'Cushis', 'crows', 'cunts', 'cotton pickers', 'cow kissers', 'cowboy killers', 'crackers', 'Congoids', 'coolies', 'coonadians', 'coons', 'cocoas', 'coconuts', 'coloreds', 'coloureds', 'conchudas', 'closetfags', 'cocksuckers', 'Cocoa Puffs', 'clams', 'clog wogs', 'closet fags', 'chonkies', 'Christ killers', 'chugs', 'chunkies', 'clamheads', 'cholo chasers', 'cholo chasing', 'Chinamen', 'Chinese wetbacks', 'ching chongs', 'chinigs', 'chink a billies', 'chee chees', 'chi chis', 'chiggers', 'chili shitters', 'chimped-out', 'celestials', 'charvas', 'charvers', 'chavs', 'carrot snappers', 'Caublasians', 'cave niggers', 'camel jockeys', 'can eaters', 'carpet pilots', 'cab niggers', 'camel cowboys', 'camel fuckers', 'camel humpers', 'camel jackers', 'bungas', 'bungs', 'burrheads', 'butt pirates', 'butterheads', 'Buddhaheads', 'bug eaters', 'buk buks', 'bumblebees', 'brownies', 'bubbles', 'bucketheads', 'buckras', 'bucks', 'brown invader', 'brown invaders', 'border niggers', 'Bounty bars', 'boxheads', 'brass ankles', 'boos', 'bootlips', 'border bunnies', 'border hoppers', 'border jumpers', 'booners', 'boongas', 'boongs', 'boonies', 'boons', 'bongs', 'boojies', 'book books', 'bog hoppers', 'bog jumpers', 'bog trotters', 'bogans', 'bohunks', 'blaxicans', 'blockheads', 'bludgers', 'blue gums', 'bluegums', 'black Barbies', 'black dagos', 'black invaders', 'bints', 'birds', 'bitter clingers', 'bix noods', 'bhremptis', 'beaner shnitzels', 'beaners', 'beanies', 'Bengalis', 'beach niggers', 'bean dippers', 'beaner babies', 'beaner baby', 'banana benders', 'banana landers', 'bananas', 'bamboo coons', 'Aunt Janes', 'Aunt Jemimas', 'Aunt Marys', 'Aunt Sallys', 'azns', 'Argies', 'Armos', 'Anglos', 'Anns', 'apes', 'apples', 'Amos', 'anchor babies', 'Angies', 'Americoons', 'Ahabs', 'albinos', 'abos', 'African catfishes', 'Africoons', 'Afro-Saxons', 'afs', 'abbos', 'ABCDs', 'ziojew', 'yard ape', 'yellow invader', 'wegro', 'whigga', 'tree nigger', 'wapanese', 'suspook', 'taco nigger', 'sheboon', 'sand nip', 'reffo', 'rice nigger', 'red nigger', 'pavement ape', 'Palestinkian', 'niggera', 'niggerette', 'niggerfag', 'niggerize', 'niggerwool', 'nigger-knock', 'nappyhead', 'muzzpig', 'muzzrat', 'muzzy', 'musla', 'muslimal', 'kneegrow', 'jewbag', 'jew-fucker', 'honklet', 'hori', 'guidette', 'gash', 'gay', 'gimp', 'fudgepacker', 'flipabeano', 'fagbag', 'derka derka', 'dindu nuffin', 'coonadian', 'clog wog', 'cocksucker', 'Congoid', 'chimp-out', 'cholo chaser', 'chimp pack', 'butt pirate', 'bootlip', 'black invader', 'tynekere', 'tynkard', 'tynkare', 'Rhine monkey', 'proddywhoddy', 'pommie grant', 'bhrempti', 'mongol', 'blue gum', 'nafri', 'flip', 'globalist', 'holohoax', 'bint', 'latrino', 'conchuda', 'closetfag', 'closet fag', 'tyncar', 'chi chi', 'MTN', 'harambe', 'Hunyock', 'moss eater', 'proddywoddy', 'divvy', 'div', 'spickaboo', 'chinig', 'ZOG lover', 'sideways cooter', 'kotiya', 'gook eye', 'jigarooni', 'smoked Irish', 'oven dodger', 'Russellite ', 'ghetto hamster', 'roofucker', 'ikey mo', 'plastic paddy', 'paddy', 'gin jockey', 'Honyock', 'zigabo', 'smoked Irishman', 'dyke jumper', 'border nigger', 'Amo', 'cave nigger', 'Caublasian', 'carrot snapper', 'camel fucker', 'ice monkey', 'butterhead', 'buk buk', 'buckra', 'brass ankle', 'boon', 'booner', 'slopehead', 'dune nigger', 'nitchee', 'zippohead', 'bog jumper', 'bog hopper', 'dole bludger', 'bludger', 'blaxican', 'bix nood', 'fog nigger', 'beaner shnitzel', 'bean dipper', 'beach nigger', 'banjo lips', 'banana lander', 'banana bender', 'Buddhahead', 'mackerel snapper ', 'camel jacker', 'Hunyak', 'wiggerette', 'pohm', 'semihole', 'Armo', 'chink a billy', 'Chinese wetback', 'tinkard', 'lubra', 'eh hole', 'cab nigger', 'Jim Fish', 'cow kisser', 'mockie', 'dogun', 'bong', 'boong', 'boonga', 'bung', 'curry slurper', 'mockey', 'spigotty', 'Jewbacca', 'bamboo coon', 'four by two', 'quashie', 'Leb', 'muk', 'popolo', 'burrhead', 'mud person', 'moch', 'mock', 'mocky', 'soup taker ', 'ping pang', 'Argie', 'azn', 'anchor baby', 'Anglo', 'AmeriKKKan', 'Afro-Saxon', 'Americoon', 'Africoon', 'camel cowboy', 'pogue', 'lowlander', 'stump jumper', 'moky', 'kyke', 'redskin', 'ocker', 'chili shitter', 'net head', 'boonie', 'dinge', 'guido', 'Bog Irish', 'gubba', 'groid', 'squaw', 'redlegs', 'nigre', 'polack', 'ching chong', 'chee chee', 'Buckwheat', 'dago', 'paleface', 'pineapple nigger', 'papist', 'gyppy', 'carpet pilot', 'bog trotter', 'gator bait', 'darkey', 'ice nigger', 'shanty Irish', 'jockie', 'slag', 'bird', 'jhant', 'jant', 'moke', 'smick', 'gurrier', 'spiv', 'skag', 'scag', 'yobbo', 'yob', 'senga', 'scobe', 'charver', 'charva', 'skanger', 'scanger', 'mil bag', 'millie', 'steek', 'spide', 'scally', 'scallie', 'ned', 'chav', 'surrender monkey', 'tranny', 'three fifths', 'three fifth', 'slave', 'Shy', 'shemale', 'scuffer', 'bogan', 'dhimmi', 'coolie', 'prod', 'pom', 'nip', 'pommie', 'niggar', 'Orangie', 'nigra', 'abo', 'pommy', 'buffie', 'sambo', 'darkie', 'beaney', 'shade', 'Christ killer', 'Gerudo', 'gew', 'Shelta', 'slopy', 'slit', 'Skippy', 'bluegum', 'ghetto', 'chonky', 'chunky', 'spike', 'squinty', 'goober', 'sub human', 'guinea', 'cotton picker', 'greaser', 'Shylock', 'Jap', 'diaper head', 'roundeye', 'jig', 'jijjiboo', 'house nigger', 'jocky', 'octaroon', 'curry stinker', 'white nigger', 'whitey', 'WIC', 'Yank', 'Yankee', 'kraut', 'lemonhead', 'Merkin', 'ZOG', 'sideways pussy', 'cowboy killer', 'eyetie', 'proddy dog', 'prairie nigger', 'Southern fairy', 'coon ass', 'moulie', 'sideways vagina', 'camel humper', 'FOB', 'fresh off the boat', 'gable', 'spade', 'wagon burner', 'moulignon', 'border bunny', 'dune coon', 'mosshead', 'gooky', 'border jumper', 'higger', 'gippo', 'gyppo', 'touch of the tar brush', 'yardie', 'boo', 'Rico Suave', 'redneck', 'muzzie', 'queer', 'nigglet', 'niggur', 'niglet', 'ofay', 'piky', 'piker', 'niggor', 'abbo', 'af', 'sooty', 'alligator bait', 'ape', 'eight ball', 'pickaninny', 'Chinaman', 'nigor', 'chigger', 'Moor', 'African catfish', 'border hopper', 'clam', 'clamhead', 'Bounty bar', 'boxhead', 'bohunk', 'bunga', 'cripple', 'camel jockey', 'dego', 'bug eater', 'domes', 'curry muncher', 'septic', 'spic', 'Ubangee', 'Ubangi', 'sole', 'spear chucker', 'snowflake', 'snout', 'shine', 'shiner', 'slope', 'slant', 'Skip', 'ghost', 'sand nigger', 'gin', 'ginzo', 'gipp', 'slant eye', 'stovepipe', 'Taffy', 'sucker fish', 'tan', 'tar baby', 'teapot', 'gypo', 'gyppie', 'tenker', 'halfrican', 'tiger', 'hick', 'heeb', 'thicklips', 'tinker', 'tynkere', 'heinie', 'hairyback', 'Tommy', 'honkie', 'Hun', 'Hunky', 'hebro', 'trash', 'spigger', 'ike', 'ikey', 'iky', 'Hunkie', 'Honyak', 'Twinkie', 'hymie', 'nicca', 'moon cricket', 'Velcro head', 'jiggaboo', 'Jihadi', 'timber nigger', 'darky', 'coon', 'jungle bunny', 'WASP', 'suntan', 'white chocolate', 'tunnel digger', 'knacker', 'whigger', 'wigga', 'wigger', 'wink', 'wog', 'wop', 'wexican', 'yellow', 'yid', 'leprechaun', 'zebra', 'lawn jockey', 'island nigger', 'jiggabo', 'zip', 'lugan', 'Lebbo', 'zipperhead', 'moxy', 'mud duck', 'mulato', 'mung', 'munt', 'munter', 'mutt', 'mulignan', 'mud shark', 'nacho', 'queen', 'raghead', 'race traitor', 'nichi', 'nig', 'nig nog', 'nigar', 'niger', 'Punjab', 'nidge', 'nigguh', 'mangia cake', 'niggress', 'pollo', 'muktuk', 'powderburn', 'porch monkey', 'moulinyan', 'pointy head', 'Oreo', 'Oriental', 'Northern monkey', 'nigette', 'pinto', 'octroon', 'pancake', 'pancake face', 'papoose', 'quadroon', 'Pepper', 'Pepsi', 'pikey', 'spook', 'neche', 'chug', 'chink', 'towel head', 'property', 'sperg', 'ricepicker', 'dingo fucker', 'ginger', 'albino', 'retard', 'buckethead', 'faggot', 'Fairy', 'ling ling', 'spice nigger', 'beaner', 'fag', 'japie', 'paki', 'wetback', 'gook', 'guala guala', 'guala', 'squarehead', 'fruit', 'Cushi', 'Kushi', 'Kushite', 'Cushite', 'uncircumcised baboon', 'Aunt Jane', 'Aunt Jemima', 'Aunt Mary', 'Aunt Sally', 'mack', 'mick', 'mickey', 'Mickey Finn', 'ABCD', 'cocoa', 'Cocoa Puff', 'coconut', 'colored', 'coloured', 'Jerry', 'crow', 'Angie', 'Ann', 'apple', 'jock', 'Junior Mint', 'banana', 'egg', 'eggplant', 'fez', 'black Barbie', 'blockhead', 'frog', 'fuzzy', 'fuzzy wuzzy', 'book book', 'brownie', 'bubble', 'buck', 'bumblebee', 'can eater', 'celestial', 'monkey', 'Charlie', 'ho', 'hoe', 'chief', 'skinny']

#English Terms marked as "unambiguous" hate speech in HateBase. List from API: see: https://hatebase.org/about
phrase_list_hatebase_unambiguous = ['jewtarded', 'jigaboo', 'jewtard', 'jewtarded', 'jigaboo', 'jewtard', 'krauts', 'niggers', 'nigger', 'nigger-rig', 'durka durkas', 'durka durka', 'derka derkas', 'closet dykes', 'closet dyke', 'black dagoes', 'border baby', 'border babies', 'pickinninys', 'piccaninnys', 'piccaninnies', 'picaninnys', 'pickaninnies', 'pickinninies', 'pickinniny', 'piccaninny', 'picaninnies', 'picaninny', 'smoke jumper', 'niggerdick', 'niggerdicks', 'niggerton', 'niggertown', 'niggerville', 'retarded', 'shekelnose', 'kikesberg', 'pisslam', 'gender nigger', 'black dago', 'Zionazi', 'sand niglet', 'sand niglets', 'Zionazis', 'ZOG lovers', 'zigabos', 'ziojews', 'yellow invaders', 'yids', 'yard apes', 'wogs', 'wops', 'wopspeak', 'wiggas', 'wiggerettes', 'wiggers', 'whiggers', 'white niggers', 'wegroes', 'wetbacks', 'wexicans', 'whiggas', 'Uncle Toms', 'Velcro heads', 'wagon burners', 'tree niggers', 'towel heads', 'trannies', 'timber niggers', 'taco niggers', 'tar babies', 'stump jumpers', 'spiggotties', 'spicspeak', 'spiggers', 'spickish', 'spiclet', 'spicish', 'spickaboos', 'spear chuckers', 'spice niggers', 'smoke jumpers', 'smoked Irishmen', 'slant eyes', 'sideways vaginas', 'sideways cooters', 'sideways pussies', 'shemales', 'sheboons', 'sheenies', 'sand nips', 'sand niggerette', 'sand niggerettes', 'sand niggers', 'sambos', 'sand monkey', 'sand monkeys', 'rice niggers', 'roofuckers', 'roundeyes', 'Rhine monkeys', 'Rhineland bastard', 'Rhineland bastards', 'red niggers', 'rednecks', 'retardeds', 'retards', 'race traitors', 'ragheads', 'quadroons', 'proddy dogs', 'proddywhoddies', 'proddywoddies', 'prairie niggers', 'porch monkeys', 'polacks', 'pommie grants', 'pineapple niggers', 'plastic paddies', 'pickaninnys', 'papists', 'pavement apes', 'pancake faces', 'oven dodgers', 'Pakiland', 'octaroons', 'octroons', 'ofays', 'niglette', 'nigguhs', 'niggurs', 'niglets', 'niggerization', 'nigglets', 'niggors', 'niggars', 'niggerettes', 'nigettes', 'nig nogs', 'muzzies', 'muzzpigs', 'muzzrats', 'mud persons', 'mud sharks', 'mossheads', 'moon crickets', 'mongs', 'kykes', 'latrinos', 'kikes', 'kneegroes', 'jijjiboos', 'jungle bunnys', 'jiggaboos', 'jiggabos', 'jigaboos', 'jigaroonis', 'jewbagg', 'Japs', 'jew-fucked', 'Japland', 'island niggers', 'injuns', 'ice monkeys', 'ice niggers', 'house niggers', 'honkeye', 'honkies', 'honklets', 'higgers', 'hebros', 'heebs', 'heinies', 'halfricans', 'gypos', 'gyppies', 'gyppos', 'groids', 'golliwogs', 'gook eyes', 'gippos', 'gipps', 'gin jockeys', 'ghetto hamsters', 'fudgepackers', 'fog niggers', 'flipabeanos', 'fagbags', 'faggots', 'faggy', 'dune coons', 'dune niggers', 'diaper heads', 'dingo fuckers', 'darkies', 'curry munchers', 'curry slurpers', 'curry stinkers', 'cowboy killers', 'Congoids', 'coonadians', 'closetfags', 'closet fags', 'Christ killers', 'cholo chasers', 'cholo chasing', 'Chinamen', 'Chinese wetbacks', 'ching chongs', 'chink a billies', 'chili shitters', 'Caublasians', 'cave niggers', 'camel jockeys', 'carpet pilots', 'cab niggers', 'camel cowboys', 'camel fuckers', 'camel humpers', 'camel jackers', 'burrheads', 'butt pirates', 'Buddhaheads', 'brown invader', 'brown invaders', 'border niggers', 'border bunnies', 'border hoppers', 'border jumpers', 'bog hoppers', 'bog jumpers', 'bog trotters', 'blaxicans', 'black dagos', 'black invaders', 'beaner shnitzels', 'beach niggers', 'beaner babies', 'beaner baby', 'banana benders', 'banana landers', 'bamboo coons', 'anchor babies', 'Americoons', 'African catfishes', 'Africoons', 'Afro-Saxons', 'ziojew', 'yard ape', 'yellow invader', 'whigga', 'tree nigger', 'suspook', 'taco nigger', 'sheboon', 'sand nip', 'rice nigger', 'red nigger', 'pavement ape', 'Palestinkian', 'niggera', 'niggerette', 'niggerfag', 'niggerize', 'niggerwool', 'nigger-knock', 'nappyhead', 'muzzpig', 'muzzrat', 'muzzy', 'muslimal', 'kneegrow', 'jewbag', 'jew-fucker', 'honklet', 'fudgepacker', 'flipabeano', 'fagbag', 'derka derka', 'dindu nuffin', 'coonadian', 'Congoid', 'cholo chaser', 'butt pirate', 'black invader', 'jigarooni', 'zigabo', 'border nigger', 'dune nigger', 'fog nigger', 'cab nigger', 'Bog Irish', 'pineapple nigger', 'gyppy', 'bog trotter', 'ice nigger', 'shanty Irish', 'tranny', 'shemale', 'niggar', 'darkie', 'Christ killer', 'cotton picker', 'jijjiboo', 'house nigger', 'octaroon', 'curry stinker', 'white nigger', 'sideways pussy', 'eyetie', 'proddy dog', 'prairie nigger', 'coon ass', 'moulie', 'sideways vagina', 'camel humper', 'wagon burner', 'moulignon', 'border bunny', 'dune coon', 'border jumper', 'gippo', 'gyppo', 'touch of the tar brush', 'muzzie', 'nigglet', 'niggur', 'niglet', 'pickaninny', 'Chinaman', 'border hopper', 'camel jockey', 'curry muncher', 'spear chucker', 'sand nigger', 'slant eye', 'gypo', 'gyppie', 'halfrican', 'honkie', 'spigger', 'hymie', 'nicca', 'moon cricket', 'jiggaboo', 'timber nigger', 'darky', 'jungle bunny', 'whigger', 'wigga', 'wigger', 'wexican', 'island nigger', 'jiggabo', 'race traitor', 'nig nog', 'nigguh', 'niggress', 'nigette', 'quadroon', 'towel head', 'faggot', 'spice nigger', 'wetback', 'guala']

#Aggrandizement
#Largely taken from: https://github.com/kellybolding/scripts/blob/master/terms_of_aggrandizement.xquery
phrase_list_aggrandizement = ['acclaimed', 'ambitious', 'notable', 'influential', 'prominent', 'distinguished', 'pioneer', 'prolific', 'seminal', 'gentleman', 'planter', 'genius', 'masterpiece', 'founding father', 'renowned', 'respected', 'prestigious', 'successful', 'acclaimed', 'celebrated', 'esteemed', 'foremost', 'eminent', 'preeminent', 'plantation owner', 'revolutionary', 'expert', 'important', 'wealthy', 'father of', 'man of letters', ]

#Race Euphemisms
phrase_list_euphemisms = ['race relations', 'troubles', 'race situation', 'racial', 'race-based', 'racism', 'color blind', 'colored', 'negro']

#Race terms - largely taken from Princeton lexicon
phrase_list_race_terms = ['native americans', 'natives', 'mulatto', 'mulattos', 'creole', 'creoles', 'oriental', 'aborigines', 'aboriginals', 'arab', 'arabs', 'hispanics', 'japs', 'coolies', 'coolie', 'illegal immigrant', 'illegal alien', 'illegal immigrants', 'illegal aliens', 'exotic', 'ethnic', 'indian', 'indians', 'savages', 'uncivilized', 'squaws', 'pygmy', 'pygmies', 'primitives', 'primitive people', 'bushmen', 'bushman', 'bushwoman', 'bushwomen', 'fag', 'dyke', 'mammy', 'negro', 'negroes', 'negros', 'gypsy', 'sambo', 'blacks', 'asians', 'asiatic', 'chink', 'gook', 'illegals']

#Slavery
phrase_list_slavery = ['slave', 'slaves', 'slavery', 'slave owner', 'enslaved', 'negro', 'slaveholder', 'slave master', 'overseer', 'abolition', 'abolitionist', 'anti-slavery', 'antislavery', 'freedmen', 'freedman', 'manumission', 'freed slaves', 'manumitted', 'bill of sale', 'bills of sale', 'plantation', 'planter']

#Women
phrase_list_women = ['wife', 'spouse', 'mistress', 'muse', 'mrs.', 'miss']

#MODIFY THIS AS NEEDED. Concat two phrase lists together if desired (e.g. phrase_list_race_terms + phrase_list_slavery).
phrase_list = phrase_list_aggrandizement

phrase_patterns = [nlp.make_doc(term) for term in phrase_list]
matcher.add('HateBase', None, *phrase_patterns)

with open(csv_path,'wt', newline='', encoding='utf-8') as csvout:
    writer = csv.writer(csvout)
    row =  ['identifer', 'match_count', 'match_type', 'match_phrase', 'snippet']
    writer.writerow(row)

    for subdir, dirs, files in os.walk(path):
        for f in files:
            if f.endswith(".xml"):
            
                with open(os.path.join(subdir, f), 'r', encoding='utf-8') as xml_file:

                    #create soup object for XML file for parsing
                    soup = BeautifulSoup(xml_file, 'lxml')

                #Get collection info
                identifier = soup.identifier.text
                print (identifier)

                #Note fields (stuff in <p> tags)
                all_descriptions = []
                descriptions = soup.find_all('dc:description')
                for description in descriptions:
                    all_descriptions.append(descriptions)

                #Convert giant list object of p text into one big string
                full_descriptions = str(descriptions)

                #Get rid of extra spaces
                full_descriptions = full_descriptions.split()

                #Remove line breaks and such
                full_descriptions = ' '.join(full_descriptions).replace('\n',' ')

                #Remove commas
                full_descriptions = ' '.join(full_descriptions).replace(',',' ')

                #print (clean_note_text)
                if len(full_descriptions) > 1000000: #nlp has max text length of 1000000 chars
                    continue

                #Giant string of <p> content
                desc = nlp(full_descriptions)

                #Title fields
                title_list = []
                title_tags = soup.find_all('dc:title')
                for title in title_tags:
                     title_list.append(title.text)
                    
                clean_title_text = ' '.join(title_list).replace('\n',' ')
                
                if len(clean_title_text) > 1000000:

                    #nlp has max text length of 1000000 chars
                    continue

                #Giant string of title content

                doc2 = nlp(str(clean_title_text))

                #Create lists of matches for notes and title
                matches_desc = matcher(doc1)
                matches_titles = matcher(doc2)

                #Count total number of matches in collection
                desc_match_count = len(matches_desc)
                title_match_count = len(matches_titles)

                #Report out <p> matches in CSV
                for match_id, start, end in matches_desc:

                    #Term itself
                    span1 = doc1[start:end]
                    start_snippet1 = start - 10 #get 10 tokens before
                    end_snippet1 = end + 10 #get 10 tokens after

                    #Term in context
                    span2 = doc1[start_snippet1:end_snippet1]
                    print (identifier, desc_match_count, 'desc_match', span1.text, span2.text)
                    row = [identifier, desc_match_count, 'desc_match', span1.text, span2.text]
                    writer.writerow(row)

                    #Report out <title> matches in CSV
                    for match_id, start, end in matches_titles:

                        #Term itself
                        span3 = doc2[start:end]
                        start_snippet2 = start - 10
                        end_snippet2 = end + 10

                        #Term in context
                        span4 = doc2[start_snippet2:end_snippet2]
                        print (identifier, clean_collection_title, title_match_count, 'title_match', span3.text, span4.text)
                        row = [identifier, clean_collection_title, title_match_count, 'title_match', span3.text, span4.text]