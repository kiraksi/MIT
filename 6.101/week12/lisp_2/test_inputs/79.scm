(define (factorial n) (if (<= n 1) 1 (* n (factorial (- n 1)))))
(define x (list 7 9 3 2))
(map factorial x)
x
(define n 0)
(define (factorial n) (if (<= n 1) 1 (* n (factorial (- n 1)))))
(map factorial x)
x
n
(map factorial (list))
n
(map - (list 1 2 3))
(map length (list (list) (list 1 2 3) (list 9 8 7 6 5 4 3 2 1) (list 2)))
(map (lambda (x) (list-ref x 2)) (list (list 1 2 3) (list 9 8 7) (list 10 13 14 15 6)))
(map (lambda (x) (map (lambda (y) (* 2 y)) x)) (list (list 1 2 3) (list 9 8 7) (list 10 13 14 15 6)))
(map - (list))
(map - ())
