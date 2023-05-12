(begin
  (define (abs x) (if (>= x 0) x (- x)))
  (filter (lambda (x) (> (abs x) 20)) (list -100 -40 -19 -5 0 5 19 40 100))
)
