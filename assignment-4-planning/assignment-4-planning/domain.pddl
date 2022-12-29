(define (domain sokorobotto)
  (:requirements :typing :negative-preconditions)
  (:types  robot pallette - robot_or_pallette 
  shipment order location saleitem)

  (:predicates
  (ships ?s - shipment ?o - order)
  (orders ?o - order ?si - saleitem)
  (unstarted ?s - shipment)
  (packing-location ?l - location)
  (available ?l - location)
  (started ?s - shipment)
  (contains ?p - pallette ?si - saleitem)
  (free ?r - robot)
  (connected ?l1 - location ?l2 - location)
  (at ?bo - robot_or_pallette ?l - location)
  (no-robot ?l - location)
  (no-pallette ?l - location)
  (includes ?s - shipment ?si - saleitem)

  
  (has ?r - robot ?p - pallette)
  )

  (:action startShipment
    :parameters (?s - shipment ?o - order ?l - location)
    :precondition (and (unstarted ?s) (ships ?s ?o) (available ?l) (packing-location ?l))
    :effect (and (started ?s) (not (unstarted ?s)) (not (available ?l)))
   )

  (:action robotMove
      :parameters (?r - robot ?l1 - location ?l2 - location)
      :precondition (and (at ?r ?l1) (no-robot ?l2) (connected ?l1 ?l2) (free ?r))
      :effect (and (at ?r ?l2) (no-robot ?l1) (not (at ?r ?l1)) (not (no-robot ?l2)) )
      )
  
  (:action robotMoveWithPallette
      :parameters (?r - robot ?p - pallette ?l1 - location ?l2 - location)
      :precondition (and (at ?r ?l1) (free ?r)(at ?p ?l1)  (no-robot ?l2) (no-pallette ?l2) (connected ?l1 ?l2) 
                    (not (no-pallette ?l1)) (not (no-robot ?l1))) 
      :effect (and (has ?r ?p) (at ?r ?l2) (at ?p ?l2) 
                   (no-robot ?l1) (no-pallette ?l1) 
                   (not (at ?r ?l1)) (not (at ?p ?l1))
                   (not (no-robot ?l2))(not (no-pallette ?l2)))
      
      )

  (:action moveItemFromPalletteToShipment
      :parameters (?l - location ?s - shipment ?si - saleitem ?p - pallette ?o - order)
      :precondition (and (at ?p ?l) (contains ?p ?si) (packing-location ?l) (ships ?s ?o)
                    (orders ?o ?si) (not (includes ?s ?si)))
      :effect (and (includes ?s ?si) (not (contains ?p ?si)))
   )
  
  (:action completeShipment
     :parameters (?s - shipment ?o - order ?l - location)
     :precondition (and (ships ?s ?o)(started ?s) (packing-location ?l) (not (available ?l)))
     :effect (and (available ?l) )
    )
)
