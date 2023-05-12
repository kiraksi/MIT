; sudoku solver implemented in Scheme :)

; build up a board as a list of lists, and call
;   (solve-sudoku board)
; to see a result.  it will return the solved board if the board can be solved,
; or -1 otherwise

; multiple boards are already defined for you below (see board1, board2,
; board3 containing the same example boards from lecture 6, and board4
; containing an insoluble puzzle)


(begin
    (define height length)
    (define (width board) (length (list-ref board 0)))

    (define (contains? list_ elt)
        (if (equal? (list) list_)
            #f
            (if (equal? (car list_) elt)
                #t
                (contains? (cdr list_) elt)
            )
        )
    )

    (define (slice list_ start stop)
        (map
            (lambda (i) (list-ref list_ i))
            (range start stop 1)
        )
    )

    (define (list-replace list_ replace-ix elt)
        (map
            (lambda (i) (if (equal? i replace-ix) elt (list-ref list_ i)))
            (range 0 (length list_) 1)
        )
    )

    (define (empty? list_) (equal? (length list_) 0))

    (define (zip l1 l2)
        (if (empty? l1)
            (list)
            (append
                (list (cons (car l1) (car l2)))
                (zip (cdr l1) (cdr l2))
            )
        )
    )
    (define (map func list_)
        (if (empty? list_)
            list_
            (append (list (func (car list_))) (map func (cdr list_)))
        )
    )

    (define (filter func list_)
        (if (empty? list_)
            list_
            (let ((h (car list_)))
                (append (if (func h) (list h) (list))
                        (filter func (cdr list_))
                )
            )
        )
    )

    (define (reduce func list_ start)
        (if (empty? list_)
            start
            (reduce func (cdr list_) (func start (car list_)))
        )
    )

    (define (subgrid-index x)
        ; this would be easier if we had floor division, but...oh well
        (if (contains? (list 0 1 2) x)
            0
            (if (contains? (list 3 4 5) x)
                1
                (if (contains? (list 6 7 8) x)
                    2
                    -1
                )
            )
        )
    )


    (define (set-difference l1 l2)
        (filter (lambda (x) (not (contains? l2 x))) l1)
    )

    (define (range start stop step)
        (if (>= start stop)
            (list)
            (append (list start) (range (+ start step) stop step))
        )
    )
    (define all-moves (range 1 10 1))
    (define (valid-moves board r c)
        (set-difference
            all-moves
            (append
                (values-in-row board r)
                (values-in-column board c)
                (values-in-subgrid board (subgrid-index r) (subgrid-index c))
            )
        )
    )

    (define (get-value board r c) (list-ref (list-ref board r) c))

    (define (!= x y) (not (equal? x y)))
    (define (nonzero? x) (!= x 0))
    (define (nonzero-vals list_) (filter nonzero? list_))

    (define (values-in-row board r)
        (nonzero-vals (list-ref board r))
    )
    (define (values-in-column board c)
        (nonzero-vals (map (lambda (row) (list-ref row c)) board))
    )

    (define (values-in-subgrid board sr sc)
        (let ((start-r (* sr 3)) (start-c (* sc 3)))
            (nonzero-vals
                (append
                    (slice (list-ref board start-r) start-c (+ start-c 3))
                    (slice (list-ref board (+ start-r 1)) start-c (+ start-c 3))
                    (slice (list-ref board (+ start-r 2)) start-c (+ start-c 3))
                )
            )
        )
    )

    (define (board-replace board r c elt)
        (map
            (lambda (r-ix)
                (let ((test-row (list-ref board r-ix)))
                    (if (equal? r-ix r)
                        (list-replace test-row c elt)
                        test-row
                    )
                )
            )
            (range 0 (height board) 1)
        )
    )

    (define (all-conss l1 l2)
        (let ((single-term (lambda (e1) (map (lambda (e2) (cons e1 e2)) l2))))
            (reduce append (map single-term l1) (list))
        )
    )
    (define (get-value-cons board c) (get-value board (car c) (cdr c)))
    (define (find-first-zero board)
        (begin
            (define (helper vals-to-try)
                (if (empty? vals-to-try)
                    (cons -1 -1)
                    (if (equal? 0 (get-value-cons board (car vals-to-try)))
                        (car vals-to-try)
                        (helper (cdr vals-to-try))
                    )
                )
            )
            (helper (all-conss (range 0 9 1) (range 0 9 1)))
        )
    )

    (define (solve-helper board r c vals)
        (if (empty? vals)
            -1 ; signal failure
            (let ((rec-result (solve-sudoku (board-replace board r c (car vals)))))
                (if (equal? rec-result -1) ; failure?!
                    (solve-helper board r c (cdr vals))
                    rec-result
                )
            )
        )
    )

    (define (solve-sudoku board)
        (let ((zero-ix (find-first-zero board)))
            (if (equal? (car zero-ix) -1)
                board ; omg solved!
                (solve-helper board (car zero-ix) (cdr zero-ix) (valid-moves board (car zero-ix) (cdr zero-ix)))
            )
        )
    )

    (define board1
         (list
            (list 5 1 7 6 0 0 0 3 4)
            (list 2 8 9 0 0 4 0 0 0)
            (list 3 4 6 2 0 5 0 9 0)
            (list 6 0 2 0 0 0 0 1 0)
            (list 0 3 8 0 0 6 0 4 7)
            (list 0 0 0 0 0 0 0 0 0)
            (list 0 9 0 0 0 0 0 7 8)
            (list 7 0 3 4 0 0 5 6 0)
            (list 0 0 0 0 0 0 0 0 0)
        )
    )

    (define board2
         (list
            (list 5 1 7 6 0 0 0 3 4)
            (list 0 8 9 0 0 4 0 0 0)
            (list 3 0 6 2 0 5 0 9 0)
            (list 6 0 0 0 0 0 0 1 0)
            (list 0 3 0 0 0 6 0 4 7)
            (list 0 0 0 0 0 0 0 0 0)
            (list 0 9 0 0 0 0 0 7 8)
            (list 7 0 3 4 0 0 5 6 0)
            (list 0 0 0 0 0 0 0 0 0)
         )
    )

    (define board3
        (list
            (list 0 0 1 0 0 9 0 0 3)
            (list 0 8 0 0 2 0 0 9 0)
            (list 9 0 0 1 0 0 8 0 0)
            (list 1 0 0 5 0 0 4 0 0)
            (list 0 7 0 0 3 0 0 5 0)
            (list 0 0 6 0 0 4 0 0 7)
            (list 0 0 8 0 0 5 0 0 6)
            (list 0 3 0 0 7 0 0 4 0)
            (list 2 0 0 3 0 0 9 0 0)
        )
    )

    (define board4
         (list
            (list 5 1 7 6 8 0 0 3 4)
            (list 2 8 9 0 0 4 0 0 0)
            (list 3 4 6 2 0 5 0 9 0)
            (list 6 0 2 0 0 0 0 1 0)
            (list 0 3 8 0 0 6 0 4 7)
            (list 0 0 0 0 0 0 0 0 0)
            (list 0 9 0 0 0 0 0 7 8)
            (list 7 0 3 4 0 0 5 6 0)
            (list 0 0 0 0 0 0 0 0 0)
        )
    )
)
