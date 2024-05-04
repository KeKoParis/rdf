from rdflib import Graph, URIRef, Literal, RDF, XSD
from rdflib.plugins.sparql import prepareQuery

from tkinter import *
from tkinter.ttk import Combobox

graph = Graph()

resource_uri = "http://example.com/resource/"
class_uri = "http://example.com/class/"
property_uri = "http://example.com/property/"
relation_uri = "http://example.com/relation/"


def get_graph():
    try:
        global graph
        graph.parse(file_input.get("1.0", "end-1c"))
        text_update()
    except BaseException:
        print("no such file")


def save():
    try:
        global graph
        graph.serialize(destination=file_input.get("1.0", "end-1c"), format="xml")
    except BaseException:
        print("no such file")


def add_relation():
    global graph, resource_uri, class_uri, relation_uri, property_uri


def run_query():
    global graph
    query_text = sparql_text.get("1.0", "end-1c")

    query = prepareQuery(query_text)
    results = graph.query(query)
    str_res = ""
    for i in results:
        str_res += (str(i)) + "\n"

    popup(str_res)


def popup(str_res):
    pop = Tk()
    pop.title("sparql result")
    pop.geometry("800x400")
    text_frame = Frame(pop)
    text_frame.grid(row=0, column=0)

    pop_label = Text(text_frame)
    pop_label.grid(row=0, column=0)

    pop_label.delete("1.0", "end-1c")
    pop_label.insert(END, str_res)

    pop.mainloop()


def add_rel(add=False, delete=False):
    global graph, class_uri, relation_uri, resource_uri, property_uri
    arr = [class_uri, resource_uri, property_uri]
    obj_1 = box_object_1.get()
    obj_2 = box_object_2.get()
    rel = box_rel.get()

    first_obj = URIRef("")
    second_obj = URIRef("")

    for i in arr:
        if i.find(obj_1) != -1:
            first_obj = URIRef(i + object_1.get("1.0", "end-1c"))
        if i.find(obj_2) != -1:
            second_obj = URIRef(i + object_2.get("1.0", "end-1c"))

    command = ()
    if rel == "belongs":
        command = (first_obj, RDF.type, second_obj)
    if rel == "relation":
        command = (first_obj, URIRef(relation_uri + rel_text.get("1.0", "end-1c")), second_obj)
    if rel == "property":
        print(obj_2)
        command = (first_obj, URIRef(property_uri + rel_text.get("1.0", "end-1c")),
                   Literal(object_2.get("1.0", "end-1c"), datatype=XSD.string))

    if add:
        graph.add(command)
    if delete:
        graph.remove(command)

    text_update()


root = Tk()
root.title("ква")
root.geometry("950x600")

# textfield
text_field_frame = Frame(root)
text_field_frame.grid(row=0, column=0)

label = Label(text_field_frame, text="file: ")
label.grid(row=0, column=0)

file_input = Text(text_field_frame, height=1, width=50)
file_input.grid(row=0, column=1)

submit = Button(text_field_frame, text="submit", command=get_graph)
submit.grid(row=0, column=2, padx=5)

save_button = Button(text_field_frame, text="save", command=save)
save_button.grid(row=0, column=3, padx=5)

# add rel

rel_frame = Frame(root)
rel_frame.grid(row=3, column=0)

# add rel

box_object_1 = Combobox(rel_frame, values=["class", "resource"])
box_object_1.current(0)
box_object_1.grid(row=0, column=0)

object_1 = Text(rel_frame, height=1, width=20)
object_1.grid(row=0, column=1)

box_rel = Combobox(rel_frame, values=["belongs", "relation", "property"])
box_rel.current(0)
box_rel.grid(row=0, column=2)

rel_text = Text(rel_frame, height=1, width=20)
rel_text.grid(row=0, column=3)

box_object_2 = Combobox(rel_frame, values=["class", "resource", "literal"])
box_object_2.current(0)
box_object_2.grid(row=0, column=4)

object_2 = Text(rel_frame, height=1, width=20)
object_2.grid(row=0, column=5)

add_button = Button(rel_frame, text="add", command=lambda: add_rel(add=True))
add_button.grid(row=1, column=0)
del_button = Button(rel_frame, text="del", command=lambda: add_rel(delete=True))
del_button.grid(row=1, column=1)
# get rdf

ont = Text(root, height=20)
ont.grid(row=5, column=0)


def text_update():
    global graph
    query_text = """
        SELECT ?subject ?predicate ?object
        WHERE {
            ?subject ?predicate ?object .
        }
    """

    query = prepareQuery(query_text)
    results = graph.query(query)
    str_res = ""
    for row in results:
        subject = row.subject
        predicate = row.predicate
        object = row.object
        str_res += f"Subject: {subject}\nPredicate: {predicate}\nObject: {object}\n\n\n"

    ont.delete("1.0", "end-1c")
    ont.insert(END, str_res)


# sparql

sparql_frame = Frame(root)
sparql_frame.grid(row=4, column=0)

spaqrl_label = Label(sparql_frame, text="SPARQL query field")
spaqrl_label.grid(row=0, column=0)

query_frame = Frame(sparql_frame)
query_frame.grid(row=1, column=0)

sparql_text = Text(query_frame, height=12)
sparql_text.grid(row=0, column=0, sticky="nsew")

scrollbar = Scrollbar(query_frame, command=sparql_text.yview)
scrollbar.grid(row=0, column=1, sticky="ns")

sparql_text.configure(yscrollcommand=scrollbar.set)

sparql_submit = Button(sparql_frame, text="submit", command=run_query)
sparql_submit.grid(row=3, column=0)

root.mainloop()
