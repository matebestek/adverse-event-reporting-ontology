;;;; -*- Mode: LISP -*-
;;;;

(in-package :asdf)

(setf (logical-pathname-translations "aero")
      `(("branches;*.*" ,(make-pathname :directory
						    (append (butlast (pathname-directory *load-pathname*) 3)
							    '("src" "ontology"))
						    :name :wild
						    :type :wild))
	("build;*.*" ,(make-pathname :directory (append (butlast (pathname-directory *load-pathname*) 3)
							'("build"))
				     :name :wild
				     :type :wild))
	("newids;*.*" ,(make-pathname :directory (append (butlast (pathname-directory *load-pathname*) 3)
							'("trunk""build" "newids"))
				     :name :wild
				     :type :wild))
	("lisp;*.*" ,(make-pathname :directory (append (butlast (pathname-directory *load-pathname*) 3)
						       '("src" "tools" "build"))
				    :name :wild
				    :type :wild))
	("spreadsheets;*.*" ,(make-pathname :directory (append (butlast (pathname-directory *load-pathname*) 3)
						       '("ontology" "spreadsheets" "in"))
				    :name :wild
				    :type :wild))

	("releases;**;*.*" ,(make-pathname :directory (append (butlast (pathname-directory *load-pathname*) 4)
						       '(:wild-inferiors))
				    :name :wild
				    :type :wild))
	))

(defsystem :aero
    :name "AERO Tools"
    :author "Melanie Courtot and Alan Ruttenberg"
    :version "1"
    :licence "BSD"
    :components
    ((:module macros
	      :pathname ""
	      :components
	      ((:file "util")))
     (:module main
	      :pathname ""
	      :components 
	      ((:file "create-aero-external-derived")
		(:file "jena"))
	      :depends-on (macros)))
     :depends-on (owl))

;;;; eof
