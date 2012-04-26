(with-ontology count-top-level-findings (:collecting t) 
    ((asq
      ;; build the sign hierarchy. 

      (imports !<http://purl.obolibrary.org/obo/bfo.owl>)

      (declaration (class !obo:OGMS_0000014))
      (annotation-assertion !rdfs:label !obo:OGMS_0000014 "clinical finding")
      (declaration (class !obo:IAO_0000027))
      (annotation-assertion !rdfs:label !obo:IAO_0000027 "data item")
      (sub-class-of !obo:OGMS_0000014 !obo:IAO_0000027)
      (sub-class-of !obo:IAO_0000027 !obo:BFO_0000031)

      (declaration (class !respiratory-distress-finding) )
      (sub-class-of !respiratory-distress-finding !obo:OGMS_0000014)

      (declaration (class !tachypnoea-finding))
      (declaration (class !recession-finding))
      (declaration (class !cyanosis-finding))
      (declaration (class !grunt-finding))

      (disjoint-classes !tachypnoea-finding !recession-finding !cyanosis-finding !grunt-finding
			!increased-use-of-accessory-respiratory-muscles-finding)

      (declaration (class !increased-use-of-accessory-respiratory-muscles-finding))

      (declaration (class !increased-use-of-intercostal-muscles-finding))
      (declaration (class !increased-use-of-diaphragm-finding))

      (declaration (class !patient))
      (sub-class-of !patient !obo:BFO_0000004)
      (disjoint-classes !increased-use-of-intercostal-muscles-finding !increased-use-of-diaphragm-finding)

      (declaration (object-property !tp)) ; internal
      (declaration (object-property !observed-of))
      (declaration (object-property !has-finding))
      (inverse-object-properties !has-finding !observed-of)

      (object-property-domain !observed-of !obo:OGMS_0000014)
      (object-property-range !observed-of !patient)
      (functional-object-property !observed-of)

      (declaration (class !token))
      (class-assertion !token !tachypnoea-token)
      (class-assertion !token !recession-token)
      (class-assertion !token !cyanosis-token)
      (class-assertion !token !grunt-token)
      (class-assertion !token !increased-use-of-accessory-respiratory-muscles-token)
      (different-individuals !tachypnoea-token !recession-token !cyanosis-token
			     !grunt-token !increased-use-of-accessory-respiratory-muscles-token)

      (sub-class-of !tachypnoea-finding !respiratory-distress-finding)
      (sub-class-of !tachypnoea-finding (object-has-value !tp !tachypnoea-token))

      (sub-class-of !recession-finding !respiratory-distress-finding)
      (sub-class-of !recession-finding (object-has-value !tp !recession-token))

      (sub-class-of !cyanosis-finding !respiratory-distress-finding)
      (sub-class-of !cyanosis-finding (object-has-value !tp !cyanosis-token))

      (sub-class-of !grunt-finding !respiratory-distress-finding)
      (sub-class-of !grunt-finding (object-has-value !tp !grunt-token))

      (sub-class-of !increased-use-of-accessory-respiratory-muscles-finding
		    !respiratory-distress-finding)
      (sub-class-of !increased-use-of-accessory-respiratory-muscles-finding
		    (object-has-value !tp !increased-use-of-accessory-respiratory-muscles-token))

      (sub-class-of !increased-use-of-intercostal-muscles-finding !increased-use-of-accessory-respiratory-muscles-finding)
      (sub-class-of !increased-use-of-diaphragm-finding !increased-use-of-accessory-respiratory-muscles-finding)

      (declaration (object-property !patient-finding-tp))

;      (sub-object-property-of (object-property-chain !has-sign !tp) !patient-finding-tp )

      (equivalent-classes
       (object-intersection-of !patient (object-some-values-from !has-finding (object-has-value !tp !cyanosis-token)))
       (object-intersection-of !patient (object-has-value !patient-finding-tp !cyanosis-token)))

      (equivalent-classes
       (object-intersection-of !patient (object-some-values-from !has-finding (object-has-value !tp !tachypnoea-token)))
       (object-intersection-of !patient (object-has-value !patient-finding-tp !tachypnoea-token)))

      (equivalent-classes
       (object-intersection-of !patient (object-some-values-from !has-finding (object-has-value !tp !grunt-token)))
       (object-intersection-of !patient (object-has-value !patient-finding-tp !grunt-token)))

      (equivalent-classes
       (object-intersection-of !patient (object-some-values-from !has-finding (object-has-value !tp !increased-use-of-accessory-respiratory-muscles-token)))
       (object-intersection-of !patient (object-has-value !patient-finding-tp !increased-use-of-accessory-respiratory-muscles-token)))

      (equivalent-classes
       (object-intersection-of !patient (object-some-values-from !has-finding (object-has-value !tp !recession-token)))
       (object-intersection-of !patient (object-has-value !patient-finding-tp !recession-token)))

      (declaration (class !respiratory-distress-patient))
      (sub-class-of !respiratory-distress-patient !patient)
      (equivalent-classes !respiratory-distress-patient (object-intersection-of !patient (object-min-cardinality 2 !patient-finding-tp)))
      
      (declaration (named-individual !p1))
      (declaration (named-individual !tach1))
      (declaration (named-individual !cyan1))
      (class-assertion !patient !p1)
      (class-assertion !tachypnoea-finding !tach1)
      (class-assertion !cyanosis-finding !cyan1)
      (object-property-assertion !observed-of !tach1 !p1)
      (object-property-assertion !observed-of !cyan1 !p1)
      
      (class-assertion !patient !p2)
      (class-assertion !increased-use-of-intercostal-muscles-finding !intercostal+2)
      (class-assertion !increased-use-of-diaphragm-finding !diaphram+2)
      (object-property-assertion !observed-of !diaphram+2 !p2)
      (object-property-assertion !observed-of !intercostal+2 !p2)

      (class-assertion !patient !p3)
      (class-assertion !increased-use-of-intercostal-muscles-finding !intercostal+3)
      (declaration (named-individual !cyan3))
      (class-assertion !cyanosis-finding !cyan3)
      (object-property-assertion !observed-of !intercostal+3 !p3)
      (object-property-assertion !observed-of !cyan3 !p3)
      ))
  (write-rdfxml count-top-level-findings "~/Desktop/count-top-level-findings.owl")
  ;(show-classtree foo :include-instances t)
  )

;; Melanie says:
;;
;; respiratory distress = ('has component' min 2 'respiratory distress sign')
;; and ('has component' max 1 tachypnoea)
;; and ('has component' max 1 recession)
;; and ('has component' max 1 cyanosis)
;; and ('has component' max 1 grunting)
;; and ('has component' max 1 'increased use of accessory respiratory muscles')

;; respiratory distress sign
;;   tachypnoea 
;;   recession  
;;   cyanosis 
;;   grunting 
;;   increased use of accessory respiratory muscles 
;;     increased use of intercostal muscles (A)
;;     increased use of diaphragm (B)

;; Case 1: if I just say 

;; respiratory distress =
;;  ('has component' min 2 'respiratory distress sign'),

;; then the patient which has A and B will be classified as having
;; respiratory distress, which is undesired. I therefore need to restrict
;; to say "at max 1 of each type"

;; Case 2: I can't say "has exactly one" in case use of accessory
;; respiratory muscle, as in some cases patient may suffer of A *and* B

;; Case 3: patient has A, B *and* tachypnoea => it should classify as
;; respiratory distress.

;; has component min 2 tp