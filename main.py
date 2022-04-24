from urllib import request
from bs4 import BeautifulSoup
from re import compile
from ssl import create_default_context, CERT_NONE
from sqlite_handler import *

# Variables
regex = compile('^/wiki/[A-Za-z_]+$')

ctx = create_default_context()
ctx.check_hostname = False
ctx.verify_mode = CERT_NONE

# Functions
def parse_html_from_url(topic):
    try:
        html = request.urlopen('https://en.wikipedia.org/wiki/' + topic, context=ctx)
    except:
        raise Exception('Theres a problem with given topic, try another one.')
    parsed_html = BeautifulSoup(html, 'html.parser')
    return parsed_html

def find_topics_in_html(parsed_html):
    raw_anchor_tags = list()
    for anchor_tag in parsed_html.findAll('a'):
        raw_anchor_tags.append( str(anchor_tag.get('href')) )
    filtered_anchor_tags = list( filter(regex.match, raw_anchor_tags) )
    return [anchor_tag[6:].capitalize() for anchor_tag in filtered_anchor_tags][:-2] # This removes the '/wiki/' and remove the 2 last elements of the list, both Main_Page

def topics_to_database(starting_topic, ending_topic_list):
    starting_topic = starting_topic.replace(' ','_').capitalize()
    add_to_topics_table(starting_topic)
    for ending_topic in ending_topic_list:
        ending_topic = ending_topic.replace(' ','_').capitalize()
        if starting_topic == ending_topic:
            continue
        add_to_topics_table(ending_topic)
        add_to_relations_table(starting_topic, ending_topic)
        print('Key:', starting_topic, 'Value:', ending_topic)
    set_as_done(starting_topic)

def find_next_topic():
    if count_topics() == 0:
        return input("\nDigite seu primeiro tópico: ").replace(' ','_').capitalize()
    else:
        return find_next_undone_topic()

def main_function():
    create_tables()
    current_topic = find_next_topic()
    parsed_html = parse_html_from_url(current_topic)
    topics_list = find_topics_in_html(parsed_html)
    topics_to_database(current_topic, topics_list)
    con.commit()
