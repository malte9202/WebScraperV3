from yattag import Doc
import requests

doc, tag, text, line = Doc().ttl()


def render_html():
    doc.asis('<!DOCTYPE html')
    with tag('html'):
        with tag('head'):
            doc.asis('<meta charset="UTF-8">'
                     '<meta name="viewport" content="width=device-width, initial-scale=1.0">')
            with tag('title'):
                text('Price Alert App')
        with tag('h1'):
            text('Price Alert App')
        with tag('body'):
            with tag('p'):
                text('App to monitor prices and receive notifications if the price drops below a threshold.'
                     'You can do the following things in this app: ')
                with tag('ul', id='feature-list'):
                    line('li', 'add products to your list whose prices you want to monitor')
                    line('li', 'receive mail notifications if the price drops below a limit you defined')
                    line('li', 'view current and best prices for the products')
            with tag('table'):
                with tag('thead'):
                    with tag('tr'):
                        with tag('th'):
                            text('Name')
                        with tag('th'):
                            text('Price Limit')
                        with tag('th'):
                            text('URL')
                with tag('tbody'):
                    productlist = requests.get('http://localhost:5000/productlist').json()
                    for product in productlist:
                        name = product['name']
                        price_threshold = product['price_threshold']
                        url = product['url']
                        with tag('tr'):
                            with tag('td'):
                                text(name)
                            with tag('td'):
                                text(price_threshold)
                            with tag('td'):
                                text(url)
        html_result = doc.getvalue()
        return html_result

