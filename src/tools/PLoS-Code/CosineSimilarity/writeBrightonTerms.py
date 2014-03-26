#!/usr/bin/python
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
import utils


#for each EventID, we add the restriction "has component some AERO term", where AERO term is the result of applying the MedDRA to Brighton mapping
#EventID is the ID of the report of interest
#listAERO_IDs is the list of all AERO_IDs in the mapping (i.e., all the AERO terms in the anaphylaxis guideline that are mapped to from MedDRA)
#listMedDRAIDs is the list of all MedDRA terms that are associated with the EventID
#a is the dict containing the relation MedDRA <-> AERO, in the form a[MedDRAID] = AEROID
#addNegation (default value = True) indicates whether or not we want to write the axion not(has component some AEROID) to "close the world"
def addHasComponentMeddra(EventID, listAERO_IDs, listMedDRAIDs, a, addNegation=True):
    
    has_component = Property(URIRef("http://purl.obolibrary.org/obo/AERO_0000125"))
    OGMS_0000014 = Class(URIRef("http://purl.obolibrary.org/obo/OGMS_0000014"))
    listAEROmapped = [EventID]
    #create the VAERS report individual
    vaersURI = "http://purl.org/vaers/" + str(EventID)
    # print str(row[0])
    vaersIndividual = Individual(URIRef(vaersURI))
    vaersIndividual.type =  OGMS_0000014


    #for each meddra annotation, figure out what is the mapping if any
    for MedDRAID in listMedDRAIDs:
        if MedDRAID in a:
            AEROIDmapped = a[MedDRAID]
            listAEROmapped.append(AEROIDmapped)
            print "mapped AERO = " +AEROIDmapped

    return listAEROmapped

#Retrieves the list of AEROIDs in the mapping                
def getlistAEROIDSinMapping(dbname, tablename):
    listAERO_IDs = []
    db = utils.MySQLConnect(dbname)
    cur = db.cursor()
    cur.execute("""SELECT distinct AERO_ID FROM %s order by AERO_ID""" % tablename)
    for row in cur.fetchall() :
        #AERO_term = URIRef("http://purl.obolibrary.org/obo/"+row[0])
        listAERO_IDs.append(row[0])
    return listAERO_IDs    
    
#This function takes a database cursor, the table to query, the event ID, and the list of mapped AERO_IDs as parameters
#For each EventID, it will use cur3 to fetch in table the MedDRA annotations corresponding to this EventID
# We compare with the conten of a, as we want to keep only those MedDRA terms that are actually mapped to an AERO ID, as only those are relevant in establishing a Brighton diagnosis
def getMedDRAIDsforeachEventID(dbname, table, EventID):
    listMedDRAIDs = []
    ###print "event ID is", EventID
    db = utils.MySQLConnect(dbname)
    cur = db.cursor()
    #get the rows from the mysql table
    cur.execute('set profiling = 1')
    try:
        cur.execute("""SELECT EventID, llt1_code, llt1_name, llt2_code, llt2_name, llt3_code, llt3_name, llt4_code, llt4_name, llt5_code, llt5_name FROM %s WHERE EventID=%%s""" % table, (EventID))
    except Exception:
        cur.execute('show profiles')
        for row in cur3:
            print(row)
        
    #browse result
    for row in cur.fetchall():
        listMedDRAIDs.append(str(row[1]))
        listMedDRAIDs.append(str(row[3]))
        listMedDRAIDs.append(str(row[5]))
        listMedDRAIDs.append(str(row[7]))
        listMedDRAIDs.append(str(row[9]))
    return listMedDRAIDs

#gets a dict a[MedDRAID]=AEROID that represents the mapping between MedDRA and AERO        
def getListMappedAEROIDs(dbname, tablename):
    a ={}
    db = utils.MySQLConnect(dbname)
    cur = db.cursor() 
    #get all the Meddra IDs in the mapping
    cur.execute("""select distinct AERO_ID, llt1_code from %s""" % tablename)
    for row in cur.fetchall() :
        mappedAEROID = str(row[0])
        mappedMedDRATermID = str(row[1])
        a[mappedMedDRATermID] = mappedAEROID
    return a

#gets the total number of events in the table (useful to determine the number of chunks needed)    
def getNumberOfEvents(dbname,tablename):
    db = utils.MySQLConnect(dbname)
    cur = db.cursor()
    cur.execute("""select COUNT( distinct EventID) from %s""" % tablename)
    for row in cur.fetchall() :
        nbEvents = str(row[0])
    #print "number of Events is %s" %nbEvents
    return nbEvents

#gets a list of all events in the database (Remember that one event can span multiple rows)
def getListOfEvents(dbname,tablename):
    listEvents=[]
    db = utils.MySQLConnect(dbname)
    cur = db.cursor()
    cur.execute("""select distinct EventID from %s order by EventID""" % tablename)
    for row in cur.fetchall() :
        listEvents.append(str(row[0]))
    return listEvents
       

if __name__ == "__main__":           


    g = utils.defineProperties()


    #get all the Meddra IDs in the mapping
    #We care only about those MedDRA IDs that are actually mapped to AEROIds
    a = getListMappedAEROIDs("mappingAnaphylaxisMedDRA","table4")


    # I need to get the count and list of all EventIDs, and then for each of those get the info. Otherwise when I split by 50 records, I may split in the middle of on event, and in each file get half the meddra terms. As a result I would not get the expected inference in each individual file (which I would get if all the meddra terms where physically in one file)  


    listEvents = getListOfEvents("H1N1Classification","VAERSDATA")

    listAERO_IDs = getlistAEROIDSinMapping("H1N1Classification","table4")

    #EventID = 371707
    #print "looking up data for record ", EventID
    with open('./VAERSBrightonTermsTotal.csv','wb') as fp:
        csvwriter = csv.writer(fp, delimiter=',',
                    quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for EventID in listEvents:
            print "looking up data for record ", EventID
            listMedDRAIDs = getMedDRAIDsforeachEventID("H1N1Classification", "VAERSDATA", EventID)
            a = getListMappedAEROIDs("H1N1Classification","table4")  
            listAEROmapped = addHasComponentMeddra(EventID, listAERO_IDs, listMedDRAIDs, a, True)   
            #if len(listAEROmapped) >1:
            csvwriter.writerow(listAEROmapped)
            print "done for ", EventID

    # print g.serialize()
    #ID = 2
    #filename = 'smalltest' + str(ID) +'.owl'
    #utils.writeRDFFile(g,filename)  
    
