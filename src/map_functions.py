from text_handlers import *
slurs = set([
    'ching chong','chink','christ-killer','christ killer','gook',
    'goy','half-breed','half breed', 'heeb','hebe','kike','jewboy',
    'jigaboo','jiggabo', 'jig', 'jigga', 'jigger', 'jungle bunny',
    'kyke','niglet','nig-nog', 'nig nog', 'nignog','nigger',
    'nigga', 'nigress','niggah', 'nigga','porch monkey','raghead',
    'rag head', 'sambo','shylock','slant-eye', 'slant eye','spic',
    'spick','spik','tar baby','tar-baby','tyrone','towel head', 
    'uncle tom','wetback','beaner','camel jockey','coon-ass','coon',
    'tnb','yard ape','welfare queen', 'unemployus', 'satchmo','sambo',
    'race traitor','race-traitor','mammy','pickaninny','sheboon',
    'furfag','chimpout'
])
def slurred(comment):
    