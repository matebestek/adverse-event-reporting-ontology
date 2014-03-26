import MySQLdb
import csv
from FuXi.Syntax.InfixOWL import *
from rdflib import plugin, BNode, Namespace, Literal, URIRef
from rdflib.Literal import _XSD_NS
from rdflib.syntax.NamespaceManager import NamespaceManager
from rdflib.Graph import Graph, ConjunctiveGraph
from rdflib.util import first
import urllib
from SPARQLWrapper import SPARQLWrapper, JSON, XML, RDF
from string import Template


#writes the graph graph in the filename RDF file
def writeRDFFile(graph, filename):
    f=open(filename,'w')
    print graph.serialize(f,format='pretty-xml')
    print "graph %s written in file %s " % (graph,filename)
    ## #print g.serialize()
    f.close()


#mysql connection to the database dbname
def MySQLConnect(dbname):
        db = MySQLdb.connect(unix_socket = '/Applications/MAMP/tmp/mysql/mysql.sock',
                     host="localhost", # your host, usually localhost
                     user="root", # your username
                     passwd="root", # your password
                     db=dbname) # name of the data base
        return db

    #define namespaces and static stuff throughout
def defineProperties():
        #namespaces definition
        aeroOntology = Namespace('http://purl.obolibrary.org/obo/aero.owl')
        skosNS = Namespace('http://www.w3.org/2004/02/skos/core#')
        umlsNS = Namespace('http://bioportal.bioontology.org/ontologies/umls/')
        aeroNS = Namespace('http://purl.obolibrary.org/obo/')
        OntologyNS = Namespace('http://purl.org/vaers/')
        medraNS = Namespace('http://purl.bioontology.org/ontology/MDR/')


        namespace_manager = NamespaceManager(Graph())
        namespace_manager.bind('obo', aeroNS, override=False)
        namespace_manager.bind('owl', OWL_NS, override=False)
        namespace_manager.bind('aero', aeroOntology, override=False)
        namespace_manager.bind('skos-core',skosNS, override=False)
        namespace_manager.bind('umls', umlsNS, override=False)


        #create the main graph
        g = Graph()
        g.namespace_manager = namespace_manager
        #this tells you that all objects will be created in the g graph -> no need to pass an extra parameter to each
        Individual.factoryGraph = g
        return g

