(if (and (> 3 4) (< 5 (define x 6))) 1 0)
x
(if (and (> 3 4) (var)) 1 0)
(if (and ((lambda (x) (> 3 x)) 2) #t) 1 0)
(if (and ((lambda (x) (> 3 x)) 2) #f) 1 0)
