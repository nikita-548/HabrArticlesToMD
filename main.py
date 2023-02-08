# Program by Ilyashenko N.
#
#
# Version   Date    Info
# 1.0       2023    Beta Version
#
# -------------------------------


import re                       # for convert html code to Markdown markup
import requests                 # for request a page
from bs4 import BeautifulSoup   # for work with html content


def html_to_string(content: BeautifulSoup) -> str:
    """
    Function for converting html markup to Markdown markup.


    :param content: type: BeautifulSoup / content to be changed
    :return content_html_to_string: content with Markdown markup
    :rtype: str
    """

    content_html_to_string = str(content)
    content_html_to_string = re.sub('&gt;', '>', content_html_to_string)

    html_to_markdown_dict = {
        'h1': ' # ',
        'h2': ' ## ',
        'h3': ' ### ',
        'h4': ' #### ',
        'h5': ' ##### ',
        'h6': ' ###### ',
        'em': '**',
        'strong': '*',
        'div': '',
        'br': '',
        'pre': '\n',
        'code': '```\n',
        'a': '',
        'p': '\n',
        'figure': '',
        'blockquote': '>'
    }

    find_link = re.findall(r'(data-src=")(http?s?:?\/\/[^"\']*\.(?:png|jpg|jpeg|gif|png|svg))', content_html_to_string)
    links = list(map(lambda link_i: link_i[1], find_link))

    for link in links:
        md_link = f'\n![{link}]({link})\n'
        content_html_to_string = re.sub(rf'<img.*?>', md_link, content_html_to_string, 1)

    for element_html, element_markdown in html_to_markdown_dict.items():
        content_html_to_string = re.sub(fr'<[\/]?{element_html}[^>]*>', f'{element_markdown}', content_html_to_string)

    return content_html_to_string


def create_md(title: str, content: str) -> None:
    """
    Function for create markdown file with content

    :param title: type: str / article title
    :param content: type: str / article content
    :return: None
    """
    with open(f'{title}.md', 'w') as file:
        file.write('# ' + title + "\n")
        file.write(content)


def main():
    """
    Entry point. Function for getting content from a link entered by the user
    :return: None
    """

    try:
        headers = {
            'User-agent':
            'Mozilla/5.0 (Linux; Android 7.0; LGMP260) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.93 Mobile Safari/537.36'
        }
        link = input('Input link to the Habr.com article: ')
        page = requests.get(f'{link}', headers=headers)

        if page.status_code != 200:
            raise Exception('Check your link')
        soup = BeautifulSoup(page.content, 'html.parser')
        article_title = soup.find(class_="tm-article-snippet__title tm-article-snippet__title_h1").get_text()
        content_html = soup.find(id="post-content-body")

        content_string = html_to_string(content_html)
        create_md(article_title, content_string)
        print('File created.')
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
