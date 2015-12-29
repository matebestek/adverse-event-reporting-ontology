# Introduction #

In AERO, the causality between the reported event and the medical intervention is not established. See the current definition of aero:adverse event at http://code.google.com/p/adverse-event-reporting-ontology/wiki/AdverseEventDefinition

This differentiates the AERO ontology from the AEO ontology developed by the He group and available at http://sourceforge.net/projects/aeo/, in which adverse events are defined as being induced by the medical intervention.

A discussion pertaining to difference and usage of both resources can be found on the [AEO list](http://sourceforge.net/mailarchive/forum.php?forum_name=aeo-devel&max_rows=25&style=nested&viewmonth=201102)


# Details #

Let us consider the example of a clinician in an institution who follows some guideline and  for that reason reports that a seizure occurred in some patient who was given an immunization a few days earlier.

AERO describes the event that happened at the reporting time, when no association other than temporal can be established. Later on, those reported events may be used to generate an hypothesis as to whether the seizure was actually induced by the immunization - this is usually done when reports are forwarded to a committee which will assess causality relationship between the events and establish a degree of causality.

AEO describes the adverse event for which causality has been proven to be induced by the medical intervention, where induced means that there is a chain of processes starting with the intervention and resulting in the adverse event. This restriction makes it unfit to annotate data in current reporting systems such as VAERS, MAUDE or the CAEFI database.

More information about causality and adverse events is available on the [causality](http://code.google.com/p/adverse-event-reporting-ontology/wiki/Causality) page.