(define (spam x) (* x x x))
(define ham spam)
(ham (spam 7))
