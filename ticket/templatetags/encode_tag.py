import base64
import bs4

from django import template

register = template.Library()


def encode64(value):
    html_string = base64.standard_b64decode(value)
    html = bs4.BeautifulSoup(html_string, 'lxml')  # BeautifulSoup.
    html.text.replace('\t', '')
    string_list = html.text.split('\n')
    tmp = string_list.index('\tcharset=utf-8')
    return string_list[tmp+1:]


def breaktext(value):
    tmp = value.split()
    for t in tmp:
        if len(t) > 20:
            string_part_one = t[:int(len(t)/2)]
            string_part_two = t[int(len(t)/2):]
            tmp[tmp.index(t)] = '\n'.join([string_part_one, string_part_two])
    return ' '.join(tmp)


register.filter('encode64', encode64)
register.filter('breaktext', breaktext)