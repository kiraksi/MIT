(define x 28)
(define (foo x) (begin (let ((y (+ x 2)) (z (* x 3))) (set! x (+ y z))) x))
(foo 9)
x
y
(define a 2)
((lambda (x) (begin (del a) x)) 7)
((lambda (x) (begin (del x) x)) 7)
((lambda (x) (begin (del x) a)) 7)
