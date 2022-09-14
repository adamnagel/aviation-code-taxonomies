from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, SKOS, RDFS, DCTERMS, OWL
import csv

# Namespaces
NS = Namespace('http://www.airbus.com/jasc/2008/')
NS_JASC = Namespace('http://www.airbus.com/jasc/2008/schema/')
NS_ATA = Namespace('http://www.airbus.com/ata/schema/')

# Properties
ata_code = NS_ATA.code
jasc_code = NS_JASC.code
ata_chapter_code = NS_ATA.chapter_code
ata_subchapter_code = NS_ATA.subchapter_code

# Types
type_ata_chapter = NS_ATA.Chapter
type_ata_subchapter = NS_ATA.SubChapter


# Program

def build_entry(row):
    uri = NS[row['4-Digit Number'].strip()]
    g.add((uri, RDF.type, SKOS.Concept))
    g.add((uri, jasc_code, Literal(row['4-Digit Number'].strip())))
    g.add((uri, RDFS.label, Literal(row['Name'].strip())))
    g.add((uri, ata_code, Literal(row['ATA style with dash'].strip())))

    g.add((uri, SKOS.inScheme, uri_scheme))

    ata = row['ATA style with dash'].strip()
    if '-' in ata:
        subata = ata[3:]
        parent = ata[0:2]

        # type it and add chapter and subchapter code
        g.add((uri, RDF.type, type_ata_subchapter))
        g.add((uri, ata_subchapter_code, Literal(subata)))
        g.add((uri, ata_chapter_code, Literal(parent)))

        # add links to parent in both directions
        uri_broader = NS[parent]
        g.add((uri, SKOS.broader, uri_broader))
        g.add((uri_broader, SKOS.narrower, uri))

    else:
        # type it as a chapter
        g.add((uri, RDF.type, type_ata_chapter))
        g.add((uri, ata_chapter_code, Literal(ata)))

        # 2-way Top Concept declaration.
        # Only Chapters are Top Concepts (not Sub-Chapters
        g.add((uri, SKOS.topConceptOf, uri_scheme))
        g.add((uri_scheme, SKOS.hasTopConcept, uri))


g = Graph()
g.bind('skos', SKOS)
g.bind('jasc', NS_JASC)
g.bind('ata', NS_ATA)
g.bind('dc', DCTERMS)
g.bind('owl', OWL)
g.bind('', NS)

# Define Ontology
uri_ontology = NS.jasc_codes
g.add((uri_ontology, RDF.type, OWL.Ontology))
g.add((uri_ontology, DCTERMS.title, Literal('JASC Code Taxonomy')))
g.add((uri_ontology, DCTERMS.description, Literal('SKOS taxonomy of Joint Aircraft System/Component (JASC) codes')))

# Define Concept Scheme
uri_scheme = NS.jasc_codes_scheme
g.add((uri_scheme, RDF.type, SKOS.ConceptScheme))
g.add((uri_scheme, RDFS.label, Literal('JASC Codes')))
g.add((uri_scheme, DCTERMS.hasVersion, Literal('2008')))

with open('jasc_2008.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',')
    for row in reader:
        build_entry(row)

# print(g.serialize(format='ttl'))
g.serialize('jasc_2008.ttl')
