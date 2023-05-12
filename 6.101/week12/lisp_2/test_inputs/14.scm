(define (square x) (* x x))
(define (fourthpow x) (square (square x)))
(fourthpow (square 2))
