from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import csv
import utils


g = utils.defineProperties()



def getMedDRANamesforeachEventID(dbname, table, EventID):
    listMedDRANames = []
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
        listMedDRANames.append(str(row[2]))
        listMedDRANames.append(str(row[4]))
        listMedDRANames.append(str(row[6]))
        listMedDRANames.append(str(row[8]))
        listMedDRANames.append(str(row[10]))
    return listMedDRANames

#initialize the array with the query
#This is the array for the IR Brighton query a la Botsis
#arrayList = ["'AERO_0000371', 'AERO_0000362', 'AERO_0000246', 'AERO_0000367', 'AERO_0000369', 'AERO_0000251', 'AERO_0000253', 'AERO_0000255', 'AERO_0000256', 'AERO_0000257', 'AERO_0000258', 'AERO_0000259', 'AERO_0000260', 'AERO_0000261', 'AERO_0000263', 'AERO_0000264', 'AERO_0000272', 'AERO_0000276', 'AERO_0000295', 'AERO_0000297', 'AERO_0000299', 'AERO_0000301', 'AERO_0000283', 'AERO_0000285', 'AERO_0000414', 'AERO_0000290', 'AERO_0000382', 'AERO_0000358', 'AERO_0000415', 'AERO_0000279', 'AERO_0000123', 'AERO_0000210'",]

arrayList = []


#This is the array for the MedDRA contingency tables test
#arrayList = ["'Hypersensitivity','Dyspnoea','Throat tightness','Pruritus','Chest discomfort','Pharyngeal oedema','Urticaria','Wheezing','Swelling face','Anaphylactic reaction','Oedema','Swelling','Lip swelling','Discomfort','Swollen tongue','Throat irritation','Eye swelling','Tic','Dysphagia','Vaccination complication','Rash','Anxiety','Paraesthesia oral','Dermatitis allergic','Oxygen saturation','Flushing','Allergy to vaccine','Heart rate increased','Electrocardiogram normal','Palpitations','Dysphonia','Erythema','Oxygen saturation normal','Cough','Electrocardiogram','Chest pain','Eye pruritus','Oedema peripheral','Heart rate','Oral pruritus','Idiopathic urticaria','Angioedema','Tachycardia','Ocular hyperaemia','Dizziness','Pruritus generalised','Hyperventilation','X-ray normal','Rash erythematous','Chest X-ray normal','Non-cardiac chest pain','Oxygen saturation decreased','Adverse drug reaction','Asthma','Hypertension','Rhinitis','Food allergy','Rash macular','Blood glucose increased','Bronchial hyperreactivity','Oedema mouth','Dry throat','Respiratory rate','Chest X-ray','Paraesthesia','Tension','Pyrexia','Feeling abnormal','Presyncope','Altered state of consciousness','Respiratory rate decreased','Rhinitis allergic','Red blood cell count normal','Respiration abnormal','Skin test','X-ray','Eyelid oedema','Hypoaesthesia oral','Feeling hot','Face oedema','Immediate post-injection reaction','Blood glucose','Stridor','No reaction on previous exposure to drug','Blood pressure','Dermatitis','Feeling jittery','Lymph node palpable','Activated partial thromboplastin time shortened','Panic disorder','Skin test negative','Arrhythmia supraventricular','Steroid therapy','Oropharyngeal spasm','Soft tissue inflammation','Laryngospasm','Vaccination site erythema','Barium swallow normal','Lip discolouration','Plantar fasciitis','Food aversion','Computerised tomogram thorax normal','Oropharyngeal swelling','Vaccination site pruritus','Scan myocardial perfusion normal','Vasoconstriction','Blood electrolytes decreased','Venous thrombosis','Troponin','Pain in extremity','Bronchitis','Myalgia','Blood pressure decreased','Metabolic function test','Oxygen supplementation','Productive cough','Serum sickness','Hypokalaemia','Bronchospasm','Hypoventilation','Neutrophil count increased','Hyperhidrosis'",]



#This is the list Contingency tables + SMQ (it is a set, we removed duplicates)
arrayList = ["'Laryngospasm', 'Blood electrolytes decreased', 'Dyspnoea', 'X-ray normal', 'Anaphylactoid reaction', 'Tachycardia', 'Dizziness', 'Oxygen saturation decreased', 'Neutrophil count increased', 'Electrocardiogram normal', 'Lymph node palpable', 'Choking sensation', 'Discomfort', 'Bronchial hyperreactivity', 'Oxygen saturation', 'Throat tightness', 'Pain in extremity', 'Oxygen saturation normal', 'Anxiety', 'Plantar fasciitis', 'Anaphylactic shock', 'Vaccination site pruritus', 'Ocular hyperaemia', 'Eye pruritus', 'Hyperventilation', 'Respiratory rate decreased', 'Scan myocardial perfusion normal', 'Type I hypersensitivity', 'Rhinitis allergic', 'Diastolic hypotension', 'Swelling', 'Circumoral oedema', 'No reaction on previous exposure to drug', 'Blood glucose', 'Circulatory collapse', 'Reversible airways obstruction', 'Blood pressure decreased', 'Face oedema', 'Blood pressure systolic decreased', 'Choking', 'Blood pressure', 'Sneezing', 'Non-cardiac chest pain', 'Rash generalised', 'Rash', 'Eyelid oedema', 'Vaccination site erythema', 'Skin swelling', 'Cardio-respiratory arrest', 'Tongue oedema', 'Bronchial oedema', 'Metabolic function test', 'Throat irritation', 'Tension', 'Feeling hot', 'Adverse drug reaction', 'Chest discomfort', 'Blood pressure diastolic decreased', 'Cough', 'Hypoventilation', 'Respiratory arrest', 'Hypoaesthesia oral', 'Heart rate increased', 'Blood glucose increased', 'Troponin', 'Lip oedema', 'Paraesthesia oral', 'Vasoconstriction', 'Pyrexia', 'Paraesthesia', 'Swelling face', 'X-ray', 'Chest X-ray normal', 'Rash erythematous', 'Skin test negative', 'Bronchitis', 'Generalised erythema', 'Altered state of consciousness', 'Immediate post-injection reaction', 'Rhinitis', 'Cardiovascular insufficiency', 'Angioedema', 'Lip swelling', 'Oedema mouth', 'Oedema', 'Swollen tongue', 'Vaccination complication', 'Food allergy', 'Laryngeal oedema', 'Computerised tomogram thorax normal', 'Lip discolouration', 'Idiopathic urticaria', 'Hypersensitivity', 'Flushing', 'Rash macular', 'Hyperhidrosis', 'Pruritus generalised', 'Red blood cell count normal', 'Stridor', 'Hypotension', 'Anaphylactoid shock', 'Serum sickness', 'Chest X-ray', 'Eye swelling', 'Chest pain', 'Urticaria papular', 'Laryngeal dyspnoea', 'Anaphylactic transfusion reaction', 'Oxygen supplementation', 'Laryngotracheal oedema', 'Feeling jittery', 'Shock', 'Myalgia', 'Presyncope', 'Respiration abnormal', 'First use syndrome', 'Cardiac arrest', 'Upper airway obstruction', 'Bronchospasm', 'Acute respiratory failure', 'Hypokalaemia', 'Respiratory distress', 'Asthma', 'Dry throat', 'Pruritus', 'Cardio-respiratory distress', 'Dysphonia', 'Soft tissue inflammation', 'Dermatitis', 'Pharyngeal oedema', 'Wheezing', 'Sensation of foreign body', 'Respiratory rate', 'Tic', 'Oropharyngeal spasm', 'Pruritus allergic', 'Dermatitis allergic', 'Rash pruritic', 'Respiratory failure', 'Kounis syndrome', 'Venous thrombosis', 'Allergy to vaccine', 'Erythema', 'Oropharyngeal swelling', 'Hypertension', 'Feeling abnormal', 'Anaphylactic reaction', 'Allergic oedema', 'Arrhythmia supraventricular', 'Steroid therapy', 'Activated partial thromboplastin time shortened', 'Fixed eruption', 'Oral pruritus', 'Tracheal obstruction', 'Eye oedema', 'Barium swallow normal', 'Tracheal oedema', 'Dysphagia', 'Skin test', 'Food aversion', 'Productive cough', 'Periorbital oedema', 'Palpitations', 'Heart rate', 'Panic disorder', 'Oedema peripheral', 'Urticaria', 'Electrocardiogram'",]



#This is the array for MedDRA SMQ
#arrayList = ["'Anaphylactic reaction','Anaphylactic shock','Anaphylactic transfusion reaction','Anaphylactoid reaction','Anaphylactoid shock','Circulatory collapse','First use syndrome','Kounis syndrome','Shock','Type I hypersensitivity','Acute respiratory failure','Asthma','Bronchial oedema','Bronchospasm','Cardio-respiratory distress','Chest discomfort','Choking','Choking sensation','Circumoral oedema','Cough','Dyspnoea','Hyperventilation','Laryngeal dyspnoea','Laryngeal oedema','Laryngospasm','Laryngotracheal oedema','Oedema mouth','Oropharyngeal spasm','Oropharyngeal swelling','Respiratory arrest','Respiratory distress','Respiratory failure','Reversible airways obstruction','Sensation of foreign body','Sneezing','Stridor','Swollen tongue','Throat tightness','Tongue oedema','Tracheal obstruction','Tracheal oedema','Upper airway obstruction','Wheezing','Allergic oedema','Angioedema','Erythema','Eye oedema','Eye swelling','Eyelid oedema','Face oedema','Fixed eruption','Flushing','Generalised erythema','Lip oedema','Lip swelling','Oedema','Periorbital oedema','Pruritus','Pruritus allergic','Pruritus generalised','Rash','Rash erythematous','Rash generalised','Rash pruritic','Skin swelling','Swelling','Swelling face','Urticaria','Urticaria papular','Blood pressure decreased','Blood pressure diastolic decreased','Blood pressure systolic decreased','Cardiac arrest','Cardio-respiratory arrest','Cardiovascular insufficiency','Diastolic hypotension','Hypotension'",]
#print arrayList

listEvents = []
with open('./VAERSMedDRATermsSMQCosineValues.csv','rU') as fp:
    reader = csv.reader(fp)
    for row in reader:
        listEvents.append(row[0])

print len(listEvents)
###listEvents = ['371707', '378840']
for VAERSID in listEvents:
#VAERSID = 371707
    listMedDRANames =  getMedDRANamesforeachEventID("H1N1Classification", "VAERSDATA", VAERSID)
    stringMedDRA = filter(None, listMedDRANames)
    stringMedDRA = str(stringMedDRA).strip('[]')
    arrayList.append(stringMedDRA)

#print arrayList
                

#custom tokenizer to avoid having a split per term. Instead we want to have a split per keyword (e.g., 'abdominal pain" and not 'abdominal', 'pain'
REGEX = re.compile(r",\s*")
def tokenize(text):
    return [tok.strip() for tok in REGEX.split(text)]



#get the vectorizer using the right tokenizer
tfidf_vectorizer = TfidfVectorizer(tokenizer=tokenize)

#fit it to the input documents and assign weights
tfidf_matrix = tfidf_vectorizer.fit_transform(arrayList)

#check the shape. We should have a matrix with m rows and n columns, where m is the number of docs we are analyzing and n is the length of the query
# for examle if we are looking at 1 report against the Brigthon terms, we expect (2,32) (the query counts as one doc, and brighton has 32 terms for anaphylaxis)
print tfidf_matrix.shape

#we can check that the right features were used
#print tfidf_vectorizer.get_feature_names()

#we can print the matrix
#print tfidf_matrix

#compute the cosine for first row of matrix against the other ones
# input is similar to cosine:  [[ 1.          0.24265071  0.24265071]]
# 1 because the query is identical to itself, then the score for each doc it is compared against
cosine = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix)

#print "cosine: ", cosine
#f = open('./results.txt', 'w')
for value in cosine[0]:
    print value


#print cosine[0]
#print cosine[0][0]
#print cosine[0][1]
#print cosine[0][2]



#print vocab
