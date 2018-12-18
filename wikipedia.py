import wikipediaapi
import requests

def return_article(name):
        if(name == "Python programing" or name == "Python Language"):
                return("is okay")

        wiki_wiki = wikipediaapi.Wikipedia('en')
        page_py = wiki_wiki.page(name)
        #print(page_py.sections[0])
        #print(page_py.text[:page_py.text.index("\n")] )
        print_sections(page_py.sections)
        return(page_py.text[:page_py.text.index("\n")])
       # return(page_py.sections)

def print_sections(sections, level=0):

        for s in sections:

                print("%s " % ( s.title))
                print_sections(s.sections, level + 1)







def wiki_search(name):
        url = "https://en.wikipedia.org/w/api.php?action=query&origin=*&format=json&generator=search&gsrsearch='{}'".format(name)
        response = requests.get(url)
        content = response.content.decode("utf8")
        print(content)


#result = requests.get('https://en.wikipedia.org/w/api.php', params=req).json()

print(return_article("Python language") )