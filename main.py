from urllib import request
from bs4 import BeautifulSoup
from re import compile
from ssl import create_default_context, CERT_NONE
from json import load, dump
from random import choice
from os import path, chdir

# Variables
regex = compile('^/wiki/[A-Za-z_]+$')
dir_path = path.dirname(path.realpath(__file__))

# Classes
class Graph:
    
    def __init__(self):
        self.graph_dict = {}

    def add_edge(self, start, end):
        if start in self.graph_dict:
            if end in self.graph_dict[start]:
                return
            else:
                self.graph_dict[start].append(end)
        else:
            self.graph_dict[start] = [end]
                
# Functions
def change_current_directory():
    chdir(dir_path)

def avoid_certificate_errors():
    ctx = create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = CERT_NONE
    return ctx

def import_json_to_dictionary_graph(graph):
    try:
        with open("graph.json") as json_file:
            graph.graph_dict = load(json_file)
    except:
        pass

def save_graph_to_json(graph):
    with open("graph.json", "w") as outfile:
        dump(graph.graph_dict, outfile)

def define_print_each_item():
    while True:
        print_items = int(input("\nDo you wish to print each added item?\n[1] Yes\n[2] No\n"))
        if print_items == 1:
            print_items = True
            break
        if print_items == 2:
            print_items = False
            break
        else:
            print('Digite uma opção válida. ')
    return print_items

def find_url_from_topic(topic):
    return 'https://en.wikipedia.org/wiki/' + topic

def parse_html_from_url(url, ctx):
    try:
        html = request.urlopen(url, context=ctx)
    except:
        raise Exception('Theres a problem with given topic, try another one.')
    parsed_html = BeautifulSoup(html, 'html.parser')
    return parsed_html

def find_topics_in_html(parsed_html):
    raw_anchor_tags = list()
    for anchor_tag in parsed_html.findAll('a'):
        raw_anchor_tags.append( str(anchor_tag.get('href')) )
    filtered_anchor_tags = list(filter(regex.match, raw_anchor_tags))
    return [anchor_tag[6:] for anchor_tag in filtered_anchor_tags][:-2] # This removes the '/wiki/' and remove the 2 last elements of the list, both Main_Page

def topic_list_to_graph(graph, starting_topic, ending_topic_list, print_items=False):
    starting_topic = starting_topic.capitalize()
    for ending_topic in ending_topic_list:
        if ending_topic.lower() == starting_topic.lower(): # If the searched topic is equal to the found one, ignore it
            continue
        graph.add_edge(starting_topic, ending_topic) # Create a graph edge, basically [ITEM_SEARCHED, ITEM_FOUND]
        if print_items: print('Key:', starting_topic, 'Value:', ending_topic)

def find_next_topic(graph):
    if graph.graph_dict == {}: # If the graph dictionary is empty, manual input is required
        return input("\nDigite seu primeiro tópico: ").replace(' ','_')
    else:
        dictionary_key = choice(list(graph.graph_dict.keys())) # Choose a random key from the graph
        next_topic = choice(graph.graph_dict[dictionary_key]) # Then choose a random value from that key
        return next_topic # This is our new topic!

def main_function(graph, context, print_items=False):
    topic = find_next_topic(graph)
    url = find_url_from_topic(topic)
    parsed_html = parse_html_from_url(url, context)
    topics_list = find_topics_in_html(parsed_html)
    topic_list_to_graph(graph, topic, topics_list, print_items)
