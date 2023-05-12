(if (or (< 3 4) (< 5 (define y 8))) 1 0)
y
(if (or (< 3 4) (var)) 1 0)
(if (or ((lambda (x) (< 3 x)) 2) #f) 1 0)
(if (or ((lambda (x) (< 3 x)) 2) #t) 1 0)
