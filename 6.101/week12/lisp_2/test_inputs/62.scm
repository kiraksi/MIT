(define (divides? x y) (if (equal? y 0) #t (if (< y 0) #f (divides? x (- y x)))))
(define (fizzbuzz n) (if (< n 0) (list) (let ((div3 (divides? 3 n)) (div5 (divides? 5 n))) (let ((thisnum (if (and div3 div5) -9997 (if div3 -9998 (if div5 -9999 n))))) (append (fizzbuzz (- n 1)) (list thisnum))))))
(fizzbuzz 30)
