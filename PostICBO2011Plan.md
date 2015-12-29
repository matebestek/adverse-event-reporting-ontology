# Introduction #

Following several discussions at ICBO 2011, here is a list of proposed updates.


# Details #

  * adverse events classes (such as "seizure according to Brighton") should be defined classes
Symptoms and signs (such as a seizure or a rash) are not specific of the adverse event, and should be taken from an independent resource, such as the Symptom Ontology.
In AERO, we don't describe the universal "seizure" but rather the set of symptoms that taken together are labeled "seizure according to Brighton" (i.e., a defined class), which may or may not be of type "seizure" as defined in the symptom ontology (the lack of definition at http://bioportal.bioontology.org/ontologies/44749?p=terms&conceptid=SYMP%3A0000124 doesn't allow to assert this one way or another).
  * we won't rely on (ogms:sign or ogms:symptom) anymore
  * we will work towards describing investigations leading to causality assesment
The "adverse event" is a process, and the diagnosis process concretizes the realization of some specific guideline, such as Brighton. The type of the event doesn't change whether its etiology is elucidated or not ( => the same referent in reality), and the root cause is determined by different processes, such as statistical studies, epidemiology, biological plausibility etc. The output of this investigation process is an information entity that assigns a root cause to the adverse event process (e.g., you broke your leg because the vaccine made you dizzy or you broke your leg because you slipped on ice unrelated to vaccine administration)
Causality is an Information Entity (from IAO) determined by a clinician. There is always a causal chain of processes leading to a disorder such as a rash, it is up to the clinician to assert, via a diagnosis process, if the root of this causal chain is for example the vaccine administration.
All adverse events are aero:adverse event. We will add an information entity such as "diagosis" or "statistical correlation". This will also allow us to add the different types of evidence as determined by the clinician/reviewing board.
  * we will coordinate with OBI and/or other resources to add relevant processes (cohort studies etc) such as needed by investigations to assess causality of the reported adverse events.
See further discussion about [evidence bearing on causality](http://code.google.com/p/adverse-event-reporting-ontology/wiki/EvidenceBearingOnCausality)