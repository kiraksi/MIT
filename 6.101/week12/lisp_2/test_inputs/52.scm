(define x 7)
(define y 8)
(define (square x) (* x x))
y
x
(square (del x))
y
x
((del square) y)
y
(square 7)
(del y)
y
(define * /)
(* 42 28)
((del *) 9 10)
(* 42 28)
(del *)
(* 42 28)
(del +)
(+ 2 3)
((lambda (x) (del y)) 7)
(define y 9)
((lambda (x) (del y)) 7)
y
((lambda (x) (del +)) 7)
((lambda (x) (del x)) 7)
(((lambda (a) (lambda (b) (del a))) 7) 10)
(((lambda (a) (lambda (b) (del b))) 9) 12)
