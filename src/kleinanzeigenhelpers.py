import mechanicalsoup


def get_listings_page(keywords, postcode, radius=0):
    browser = mechanicalsoup.StatefulBrowser()
    browser.open("https://www.kleinanzeigen.de")
    browser.select_form('form[data-testid="search-form"]')
    browser['keywords'] = keywords
    browser['locationStr'] = postcode
    browser['radius'] = str(radius)
    # browser['categoryId'] =  # TODO

    res = browser.submit_selected()
    return res


def extract_items(page):
    if page.soup.find_all(id='saved-search-empty-result'):
        return []

    items = []
    for item in page.soup.find_all('article'):
        title = item.a.text
        url = 'https://www.kleinanzeigen.de' + item.a.attrs['href']
        price = item.find(attrs={'class': 'aditem-main--middle--price-shipping--price'}).text
        image = item.find(attrs={'class': 'imagebox srpimagebox'}).img
        image_url = ''
        if image:
            image_url = image.attrs['src']
        items.append({'title': title, 'url': url,
                      'price': price, 'image': image_url})

    return items
