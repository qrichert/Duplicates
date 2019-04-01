LANG = 'en'

if LANG == 'fr':
	import translation.fr as tr
else:  # English is default ('en')
	import translation.en as tr
