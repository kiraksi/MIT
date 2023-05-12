(begin
    (define (fib n) (fib-iter n 0 1))
    (define (fib-iter n a b)
      (if (equal? n 1)
        b 
        (if (equal? n 0)
          a
          (fib-iter (- n 1) b (+ a b))
        )
      )
    )
    (define (square x) (* x x))
)
