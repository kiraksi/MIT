(define (spam eggs) (lambda (x y) (- eggs x y)))
(define eggs 7)
(define something (spam 6))
(something 2 3)
((spam 9) 8 7)
eggs
x
y
