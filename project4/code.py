import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET
import cerberus
import schema
import collections

filename = ('/Users/AndrewBryant/Documents/Udacity/p3/santiago_chile.osm')

# Improve Street Names 

av = re.compile(r'^(Av\.|Avda\.?|Avenida\.)', re.IGNORECASE)
pasaje = re.compile(r'^(Pje|Psje)\.?\s+', re.IGNORECASE)
accented_i = re.compile(r'Ã', re.IGNORECASE)
accented_o = re.compile(r'(Ã³|í³)', re.IGNORECASE)
accented_e = re.compile(r'(Ã©|í©)', re.IGNORECASE)
accented_u = re.compile(r'(íº|Ãº)', re.IGNORECASE)
accented_a = re.compile(r'í¡', re.IGNORECASE)
santa = re.compile(r'Sta(\.)?\s+', re.IGNORECASE)
nuestra = re.compile(r'ntra(\s)+', re.IGNORECASE)
senora = re.compile(r'sra', re.IGNORECASE)
n = re.compile(r'í±', re.IGNORECASE)
pob = re.compile(r'pob\.', re.IGNORECASE)

mapping = { "Av.": "Avenida",
            "Pje." : "Pasaje ",
            "Ã" : "í",
            "Ã³": "ó",
            "Ã©": "é",
            "íº": "ú",
            "í³": "ó",
            "í©": "é",
            "í±": "ñ",
            "í¡": "á",
            "Sta": "Santa ",
            "Ntra": "Nuestra ",
            "Sra": "Señora",
            "Pob": "Población",
            }

def audit_street_type(street_types, street_name):
    m1 = av.search(street_name)
    m2 = pasaje.search(street_name)
    m3 = accented_i.search(street_name)
    m4 = accented_o.search(street_name)
    m5 = accented_e.search(street_name)
    m6 = accented_u.search(street_name)
    m7 = accented_a.search(street_name)
    m8 = santa.search(street_name)
    m9 = nuestra.search(street_name)
    m10 = senora.search(street_name)
    m11 = n.search(street_name)
    m12 = pob.search(street_name)
    if m1:
        street_type = m1.group()
        street_types[street_type].add(street_name)
    elif m2:
        street_type = m2.group()
        street_types[street_type].add(street_name)
    elif m3:
        street_type = m3.group()
        street_types[street_type].add(street_name)
    elif m4:
        street_type = m4.group()
        street_types[street_type].add(street_name)
    elif m5:
        street_type = m5.group()
        street_types[street_type].add(street_name)
    elif m6:
        street_type = m6.group()
        street_types[street_type].add(street_name)
    elif m7:
        street_type = m7.group()
        street_types[street_type].add(street_name)
    elif m8:
        street_type = m8.group()
        street_types[street_type].add(street_name)
    elif m9:
        street_type = m9.group()
        street_types[street_type].add(street_name)
    elif m10:
        street_type = m10.group()
        street_types[street_type].add(street_name)
    elif m11:
        street_type = m11.group()
        street_types[street_type].add(street_name)
    elif m12:
        street_type = m12.group()
        street_types[street_type].add(street_name)
    

        
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def update_name(street_types):
    x = street_types
    match1 = re.findall(av, x)
    if match1:
        x = re.sub(av, mapping['Av.'], x)
    match2 = re.findall(pasaje, x)
    if match2:
        x = re.sub(pasaje, mapping['Pje.'], x)
    match3 = re.findall(accented_u, x)
    if match3:
        x = re.sub(accented_u, mapping['íº'], x)
    match4 = re.findall(accented_i, x)
    if match4:
        x = re.sub(accented_i, mapping["Ã"], x)
    match5 = re.findall(accented_o, x)
    if match5:
        x = re.sub(accented_o, mapping["í³"], x)
    match6 = re.findall(accented_e, x)
    if match6:
        x = re.sub(accented_e, mapping["í©"], x)
    match7 = re.findall(n, x)
    if match7:
        x = re.sub(n, mapping['í±'], x)
    match8 = re.findall(accented_a, x)
    if match8:
        x = re.sub(accented_a, mapping["í¡"], x)
    match9 = re.findall(santa, x)
    if match9:
        x = re.sub(santa, mapping['Sta'], x)
    match10 = re.findall(nuestra, x)
    if match10:
        x = re.sub(nuestra, mapping['Ntra'], x)
    match11 = re.findall(senora, x)
    if match11:
        x = re.sub(senora, mapping['Sra'], x)
    match12 = re.findall(pob, x)
    if match12:
        x = re.sub(pob, mapping['Pob'], x)
    return(x)

def audit(file):
    osm_file = open(file, "r")
    street_types = collections.defaultdict(set)
    for event, elem in ET.iterparse(file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
                    update_name(tag.attrib['v'])
    osm_file.close()
    return street_types

audit(filename)

# Extract to csv 

NODES_PATH = "stgo_sample_nodes.csv"
NODE_TAGS_PATH = "stgo_sample_nodes_tags.csv"
WAYS_PATH = "stgo_sample_ways.csv"
WAY_NODES_PATH = "stgo_ways_sample_nodes.csv"
WAY_TAGS_PATH = "stgo_ways_sample_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
more_than_one_colon = re.compile(r'^([a-z])+:([a-z])+:([a-z])+')

SCHEMA = schema.schema


NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']


def shape_element(elem, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
              problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  
    tag_list = []
    if elem.tag == 'node':
        try:
            del elem.attrib['visible']
            node_attribs[elem.tag] = elem.attrib
        except KeyError:
            node_attribs[elem.tag] = elem.attrib
        for node_tag in elem:
            node_tag_attribs = {}
            match = re.findall(PROBLEMCHARS, node_tag.attrib['k'])
            match2 = re.findall(more_than_one_colon, node_tag.attrib['k'])
            match3 = re.findall(LOWER_COLON, node_tag.attrib['k'])
            if match:
                node_tag_attribs['id'] = elem.attrib['id']
                node_tag_attribs['key'] = None
                node_tag_attribs['value'] = node_tag.attrib['v']
                node_tag_attribs['type'] = 'regular'
                tag_list.append(node_tag_attribs)
            elif match2:
                split = node_tag.attrib['k'].split(':')
                node_tag_attribs['id'] = elem.attrib['id']
                node_tag_attribs['key'] = split[1] + split[2]
                node_tag_attribs['value'] = node_tag.attrib['v']
                node_tag_attribs['type'] = split[0]
                tag_list.append(node_tag_attribs)
            elif match3:
                k_split = node_tag.attrib['k'].split(':')
                node_tag_attribs['id'] = elem.attrib['id']
                node_tag_attribs['key'] = k_split[1]
                node_tag_attribs['value'] = node_tag.attrib['v']
                node_tag_attribs['type'] = k_split[0]
                tag_list.append(node_tag_attribs)
            else:
                node_tag_attribs['id'] = elem.attrib['id']
                node_tag_attribs['key'] = node_tag.attrib['k']
                node_tag_attribs['value'] = node_tag.attrib['v']
                node_tag_attribs['type'] = 'regular'
                tag_list.append(node_tag_attribs)
    if elem.tag == 'way':
        counter = 0
        try:
            del elem.attrib['visible']
            way_attribs[elem.tag] = elem.attrib
        except KeyError:
            way_attribs[elem.tag] = elem.attrib
        for subtag in elem:
            nd_subtag_attribs = {}
            way_tag_attribs = {}
            if subtag.tag == 'nd':
                nd_subtag_attribs['id'] = elem.attrib['id']
                nd_subtag_attribs['node_id'] = subtag.attrib['ref']
                nd_subtag_attribs['position'] = counter
                counter += 1
                way_nodes.append(nd_subtag_attribs)
            if subtag.tag == 'tag':
                match = re.findall(PROBLEMCHARS, subtag.attrib['k'])
                match2 = re.findall(more_than_one_colon, subtag.attrib['k'])
                match3 = re.findall(LOWER_COLON, subtag.attrib['k'])
                if match:
                    way_tag_attribs['id'] = elem.attrib['id']
                    way_tag_attribs['key'] = None
                    way_tag_attribs['value'] = subtag.attrib['v']
                    way_tag_attribs['type'] = 'regular'
                    tag_list.append(way_tag_attribs)
                elif match3:
                    k_split = subtag.attrib['k'].split(':',1)
                    way_tag_attribs['id'] = elem.attrib['id']
                    way_tag_attribs['key'] = k_split[1]
                    way_tag_attribs['value'] = subtag.attrib['v']
                    way_tag_attribs['type'] = k_split[0]
                    tag_list.append(way_tag_attribs)
                else:
                    way_tag_attribs['id'] = elem.attrib['id']
                    way_tag_attribs['key'] = subtag.attrib['k']
                    way_tag_attribs['value'] = subtag.attrib['v']
                    way_tag_attribs['type'] = 'regular'
                    tag_list.append(way_tag_attribs)
    if elem.tag == 'node':
        return {'node': list(node_attribs.values())[0], 'node_tags': tag_list}
    elif elem.tag == 'way':
        return {'way': list(way_attribs.values())[0], 'way_nodes': way_nodes, 'way_tags': tag_list}


# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        try:
            field, errors = next(validator.errors.items())
            message_string = "\nElement of type '{0}' has the following errors:\n{1}"
            error_string = pprint.pformat(errors)
        except TypeError:
            pass      
        try:
            raise Exception(message_string.format(field, error_string))
        except UnboundLocalError:
            pass


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""
    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w') as nodes_file, \
         codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file, \
         codecs.open(WAYS_PATH, 'w') as ways_file, \
         codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file, \
         codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS, delimiter = ';')
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS, delimiter = ';')
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS, delimiter = ';')
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS, delimiter = ';')
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS, delimiter = ';')

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)
                if element.tag == 'node':
                    try:
                        nodes_writer.writerow((el['node']))
                        node_tags_writer.writerows(el['node_tags'])
                    except UnicodeEncodeError:
                        continue
                if element.tag == 'way':
                    try:
                        ways_writer.writerow(el['way'])
                        way_nodes_writer.writerows(el['way_nodes'])
                        way_tags_writer.writerows(el['way_tags'])
                    except UnicodeEncodeError:
                        continue


if __name__ == '__main__':
    # Note: Validation is ~ 10X slower. For the project consider using a small
    # sample of the map when validating.
    process_map(filename, validate=True)
