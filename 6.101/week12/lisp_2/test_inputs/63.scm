(define (allprimes n) (allprimes-iter n (list)))
(define (prime-iter n m) (if (>= n m) #t (if (divides? m n) #f (prime-iter n (+ m 1)))))
(define (prime? n) (if (< n 2) #f (prime-iter n 2)))
(define (prime-iter n m) (if (>= m n) #t (if (divides? m n) #f (prime-iter n (+ m 1)))))
(define (divides? x y) (if (equal? y 0) #t (if (< y 0) #f (divides? x (- y x)))))
(define (allprimes-iter n sofar) (if (< n 0) sofar (let ((isprime (prime? n))) (let ((newlist (if isprime (append sofar (list n)) sofar))) (allprimes-iter (- n 1) newlist)))))
(allprimes 30)
n
m
y
x
newlist
isprime
