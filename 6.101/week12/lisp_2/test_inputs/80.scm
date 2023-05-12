(define x (list 1 -1 -3 -2))
(filter (lambda (x) (> x 0)) x)
x
(filter (lambda (x) (or (> x 0) (< x 0))) (list 1 1 1 1 0 0 0 -1 -1 -1 -1))
(filter (lambda (x) #t) (list 1 1 1 1 0 0 0 -1 -1 -1 -1))
(filter (lambda (x) (or (> x 0) (< x 0))) ())
(filter (lambda (x) (or (> x 0) (< x 0))) (list))
