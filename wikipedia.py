import wikipediaapi
import requests

def return_article(name):
        #if(name == "Python programing" or name == "Python Language"): return("is okay")

        wiki_wiki = wikipediaapi.Wikipedia('en')
        page_py = wiki_wiki.page(name)
        #print(page_py.sections[0])
        #print(page_py.text[:page_py.text.index("\n")] )
        sections = return_sections(page_py.sections)
        return(page_py.text, sections)
       # return(page_py.sections)

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


#result = requests.get('https://en.wikipedia.org/w/api.php', params=req).json()

articleText, sections = return_article("Russia")
print(articleText[:articleText.index(sections[0])])
#print(articleText)
print(sections)

