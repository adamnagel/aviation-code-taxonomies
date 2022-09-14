from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, SKOS, RDFS, DCTERMS, OWL
import csv

# Namespaces
NS_ATA = Namespace('http://www.airbus.com/ata/schema/')
NS = Namespace('http://www.airbus.com/ata/')

# Properties
ata_code = NS_ATA.code
ata_chapter_code = NS_ATA.chapter_code
ata_subchapter_code = NS_ATA.subchapter_code

# Types
type_ata_chapter = NS_ATA.Chapter
type_ata_subchapter = NS_ATA.SubChapter


# Program

def build_entry(row):
    uri = NS[row['Chapter Number'].strip()]
    g.add((uri, RDF.type, SKOS.Concept))
    g.add((uri, RDF.type, type_ata_chapter))

    g.add((uri, RDFS.label, Literal(row['ATA Chapter Name'].strip())))
    g.add((uri, ata_code, Literal(row['Chapter Number'].strip())))
    g.add((uri, ata_chapter_code, Literal(row['Chapter Number'].strip())))

    # 2-way Top Concept declaration
    g.add((uri, SKOS.topConceptOf, uri_scheme))
    g.add((uri_scheme, SKOS.hasTopConcept, uri))

    g.add((uri, SKOS.inScheme, uri_scheme))


g = Graph()
g.bind('skos', SKOS)
g.bind('ata', NS_ATA)
g.bind('dc', DCTERMS)
g.bind('owl', OWL)
g.bind('', NS)

# Define Ontology
uri_ontology = NS.ata_chapters
g.add((uri_ontology, RDF.type, OWL.Ontology))
g.add((uri_ontology, DCTERMS.title, Literal('ATA Chapter Taxonomy')))
g.add((uri_ontology, DCTERMS.description, Literal('SKOS taxonomy of Air Transport Association (ATA) chapters')))

# Define Concept Scheme
uri_scheme = NS.ata_chapter_scheme
g.add((uri_scheme, RDF.type, SKOS.ConceptScheme))
g.add((uri_scheme, RDFS.label, Literal('ATA Chapters')))

with open('ata_from_wikipedia.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',')
    for row in reader:
        build_entry(row)

# print(g.serialize(format='ttl'))
g.serialize('ata-chapters.ttl')
