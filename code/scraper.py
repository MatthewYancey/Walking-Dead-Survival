from bs4 import BeautifulSoup
import requests
import csv

url = 'http://walkingdead.wikia.com/wiki/TV_Series_Characters'
base_url = 'http://walkingdead.wikia.com'
r = requests.get(url)
s = BeautifulSoup(r.text)
fix_list = ['Gender', 'Hair', 'Age', 'Occupation', 'Family', 'First Appearance', 'Status', 'Series lifespan', 'Ethnicity']
save_file = 'data'
data = []

# finds all the character urls
chars = s.findAll(class_ = 'image image-thumbnail link-internal')
characters_urls = []
for i in range(len(chars)):
    if chars[i].get('href').replace('/wiki/', '') != 'Characters':
        characters_urls.append(chars[i].get('href'))


# goes through the character urls
for i in range(len(characters_urls)):
    print(characters_urls[i])
    new_row = []

    # gets the character name
    name = characters_urls[i].replace('/wiki/', '')
    name = name.replace('_(TV_Series', '')
    name = name.replace('_', ' ')
    name = name.replace(')', '')
    new_row.append(name)

    r = requests.get(base_url + characters_urls[i])
    s = BeautifulSoup(r.text)

    # this handels pages that don't have full content
    if s.find(class_ = 'infobox') is not None:
        text = s.find(class_ = 'infobox').get_text()
        
        # formats the text a little
        for f in fix_list:
            text = text.replace(f + '\n', '\n' + f + ': ')

        # adds the data to the data list
        print(text)
        for f in fix_list:
            if f in text:
                start = text.index(f) + len(f) + 1
                try:
                    end =  text[start:].index('\n') + start
                    new_row.append(text[start:end].strip())
                except:
                    new_row.append('Error')
            else:
                new_row.append('NA')

        
        # gets the start and end of the lifespan
        lifespan = new_row[8]
        start = 'NA'
        end = 'NA'
        if lifespan != 'NA' and lifespan != 'Error':
            start = lifespan[1:lifespan[1:].index('"') + 1]
            if 'to Present' in lifespan:
                end = 'present'
            if lifespan[len(lifespan) - 1] == '"':
                end = lifespan[lifespan[:len(lifespan) - 2].rfind('"'):len(lifespan)]
                end = end.replace('"', '')

        new_row.append(start)
        new_row.append(end)

        data.append(new_row)
    
# gets the ethnicity of characters
for i in range(len(data)):
	e = data[i][9]
	if "American" in e:
		e = e.split("American")[0]
		data[i][9] = e + "American"


# adds the header and saves the file
data.insert(0, ['Name'] + fix_list + ['l_start', 'l_end'])

myfile = open('C:/Users/Matt/OneDrive/Projects/Walking Dead/data/data.csv', 'w', newline = '')
wr = csv.writer(myfile)
wr.writerows(data)
