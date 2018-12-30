import wikipediaapi
import requests

def return_article(name):
        print(name)

        if(isEnglish(name)):
                wiki_wiki = wikipediaapi.Wikipedia('en')
                page_py = wiki_wiki.page(name)

                #check for existing page
                if(page_py.exists()): # if page exists
                        sections = return_sections(page_py.sections)

                else:
                        return("/pageNotFound", ["none"])

                # Special cases
                if (name == "/start"): #welcome message
                        return("/start", ["none"])

                elif("may refer to:" in page_py.text):
                        print("REFER TO")
                        return("/refer", sections)

                return(page_py.text, sections)

        else: #for russian language
                wiki_wiki = wikipediaapi.Wikipedia('en')
                page_py = wiki_wiki.page(name)

                if (page_py.exists()):  # if page exists
                        sections = return_sections(page_py.sections)

                else:
                        return ("/pageNotFound", ["none"])

                # print(page_py.sections[0])
                # print(page_py.text[:page_py.text.index("\n")] )

                if ("may refer to:" in page_py.text):
                        print("REFER TO")
                return (page_py.text, sections)

# check if entered english request
def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

def return_sections(sections, level=0, section = []):
        section = []
        for s in sections:
                section.append(s.title)
                #print("%s " % ( s.title))
                return_sections(s.sections, level + 1, section)

        return section

def wiki_search(name):

        url = "https://en.wikipedia.org/w/api.php?action=query&origin=*&format=json&generator=search&gsrsearch='{}'".format(name)
        response = requests.get(url)
        content = response.content.decode("utf8")
        print(content)

def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]

#result = requests.get('https://en.wikipedia.org/w/api.php', params=req).json()


#
#articleToPrint = articleText[:articleText.index(sections[0])]
#
# listOfEndLines = find(articleToPrint, '\n')
# print(listOfEndLines)
#
# for i in range(len(listOfEndLines)-1, 0, -1):
#         if listOfEndLines[i] < 4096:
#                 print( articleToPrint[0:listOfEndLines[i]])
#                 print("#############")
#                 print(articleToPrint[listOfEndLines[i]:] )
#                 break

#4096
#print("22222222222")
#print(articleToPrint)


# print(sections)
a,b,c = return_article("russia")
print( c )

