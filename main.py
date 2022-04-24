from urllib import request
from bs4 import BeautifulSoup
from re import compile
from ssl import create_default_context, CERT_NONE
from os import path, chdir

# Variables
regex = compile('^/wiki/[A-Za-z_]+$')
dir_path = path.dirname(path.realpath(__file__))

ctx = create_default_context()
ctx.check_hostname = False
ctx.verify_mode = CERT_NONE

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
graph = Graph()    
     
# Functions
def change_current_directory():
    chdir(dir_path)
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
    filtered_anchor_tags = list(filter(regex.match, raw_anchor_tags))
    return [anchor_tag[6:] for anchor_tag in filtered_anchor_tags][:-2] # This removes the '/wiki/' and remove the 2 last elements of the list, both Main_Page
def topic_list_to_graph(starting_topic, ending_topic_list):
    starting_topic = starting_topic.capitalize()
    for ending_topic in ending_topic_list:
        if ending_topic.lower() == starting_topic.lower(): # If the searched topic is equal to the found one, ignore it
            continue
        graph.add_edge(starting_topic, ending_topic) # Create a graph edge, basically [ITEM_SEARCHED, ITEM_FOUND]
        print('Key:', starting_topic, 'Value:', ending_topic)
def find_next_topic():
    if graph.graph_dict == {}: # If the graph dictionary is empty, manual input is required
        return input("\nDigite seu primeiro tópico: ").replace(' ','_')
    else:
        for key in graph.graph_dict.keys():
            for value in graph.graph_dict[key]:
                if value not in graph.graph_dict.keys():
                    return value
def main_function():
    topic = find_next_topic()
    parsed_html = parse_html_from_url(topic)
    topics_list = find_topics_in_html(parsed_html)
    topic_list_to_graph(topic, topics_list)
