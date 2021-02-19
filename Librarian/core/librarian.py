class Librarian:
    
    def __init__(self):
        return

    

# utility functions for class 'Librarian'
def find_links(url):

    # create an empty list which will be used to store links
    links = []

    # open the given URL and sent HTML request
    html = urlopen(url)

    # parse it through BeatifulSoup
    bs = BeautifulSoup(html, 'html.parser')

    # get all links in the page
    tags_including_links = bs.findAll(lambda tag: 'href' in tag.attrs)

    for tag in tags_including_links:
        # todo: add a pipeline for filtering irrelevant links in the page
        links.append(tag.attrs['href'])

    return links