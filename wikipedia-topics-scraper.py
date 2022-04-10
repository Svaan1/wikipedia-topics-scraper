from main import *

# Initial Setup
change_current_directory()
graph = Graph()
context = avoid_certificate_errors()
import_json_to_dictionary_graph(graph)


# Initial inputs
number_of_searches = int(input("How many items do you wish to search for? "))
print_items = define_print_each_item()

# Main function code
for i in range(number_of_searches):
    main_function(graph, context, print_items=print_items)

# End of function
save_graph_to_json(graph)






    







