(begin
  (define (foo bar) (lambda (x y) (- bar x y)))
  (define bar 7)
  (define something (foo 6))
  (list (something 2 3)
        ((foo 9) 8 7)
  )
)
