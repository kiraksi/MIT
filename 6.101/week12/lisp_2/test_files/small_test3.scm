(begin
  (define (foo bar) (lambda (x y) (- bar x y)))
  (define bar 7)
  (define something (foo 6))
  (list (something 2 3)
        ((foo 9) 8 7)
  )
  (map
  (lambda (x)
    (* x 2)
  )
  (list 1 2 3 4)
)
)
