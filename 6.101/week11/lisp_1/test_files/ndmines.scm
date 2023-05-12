; n-d minesweeper implemented in Scheme :)

; example code to run:
; (define game (new-game-nd (list 2 4) (list (list 0 0) (list 1 0) (list 1 1))))
; (game-get-board game)
; (dig-nd game (list 0 1))
; (dig-nd game (list 0 3))
; (game-get-mask game)
; (game-get-state game)

(begin
  ; State is represented as follow: 0 => 'ongoing', 1 => 'victory', 2 => 'defeat'
  ; Game board uses -1 to indicate that a bomb is present. Non-negative counts represent non-bomb squares.
  ; Mask uses #t and #f to represent whether a square is revealed or hidden respectively.

  ; helpers for map and reduce (filter not used here)
  (define (empty? list_) (equal? (length list_) 0))

  (define (map func list_)
    (if (empty? list_)
      (list)
      (append (list (func (car list_))) (map func (cdr list_)))
    )
  )

  (define (reduce func list_ start)
    (if (empty? list_)
      start
      (reduce func (cdr list_) (func start (car list_)))
    )
  )

  ; Equivalent to Python's `range` builtin.
  (define (range start stop)
    (if (>= start stop)
      (list)
      (cons start (range (+ start 1) stop))
    )
  )

  ; Equivalent to Python's `all` builtin that takes in a list.
  (define (all values)
    (if (equal? (length values) 0)
      #t
      (and (car values) (all (cdr values)))
    )
  )

  ; Equivalent to Python's `min` builtin for two arguments.
  (define (min a b)
    (if (< a b)
      a
      b
    )
  )

  ; Equivalent to Python's `max` builtin for two arguments.
  (define (max a b)
    (if (> a b)
      a
      b
    )
  )

  ; Equivalent to Python's `zip` builtin for two linked lists.
  (define (zip a b)
    (if (or (equal? (length a) 0) (equal? (length b) 0))
      (list)
      (cons
        (cons (car a) (car b))
        (zip (cdr a) (cdr b))
      )
    )
  )

  ; Sets the element at a given index in a linked list.
  (define (set-list-ref ll index value)
    (if (equal? index 0)
      (cons value (cdr ll))
      (cons (car ll) (set-list-ref (cdr ll) (- index 1) value))
    )
  )

  ; Creates an nd-array of the specified dimensions filled with an initial value.
  (define (initialize-nd dimensions value)
    (if (equal? (length dimensions) 0)
      ; Base case.
      value

      ; Recursive case. Make multiple smaller nd-arrays.
      (map (lambda (_)
        (initialize-nd
          (cdr dimensions)
          value
        )
      ) (range 0 (car dimensions)))
    )
  )

  ; Returns a list of all neighboring coordinates.
  (define (neighbors-nd dimensions coordinates)
    (if (equal? (length dimensions) 0)
      ; Base case.
      (list (list))

      ; Recursive case. Use a recursive call to generate the suffix. Map each suffix to a list of of valid neighbors.
      ; Use reduce to flatten all neighbors.
      (reduce
        append
        (map
          (lambda (suffix)
            (map
              (lambda (prefix) (append (list prefix) suffix))
              (range (max 0 (- (car coordinates) 1)) (min (car dimensions) (+ (car coordinates) 2)))
            )
          )
          (neighbors-nd (cdr dimensions) (cdr coordinates))
        )
        (list)
      )
    )
  )

  ; Gets the value in an nd-array at the specified coordinate.
  (define (get-nd board coordinates)
    (if (equal? (length coordinates) 1)
      ; Base case.
      (list-ref board (car coordinates))

      ; Recursive case. Go to the correct board with one less dimension than the current board.
      (get-nd (list-ref board (car coordinates)) (cdr coordinates))
    )
  )

  ; Sets the value in an nd-array at the specified coordinate. Returns a possibly new linked list.
  (define (set-nd board coordinates value)
    (if (equal? (length coordinates) 1)
      ; Base case.
      (set-list-ref board (car coordinates) value)

      ; Recursive case. Go to the correct board with one less dimension than the current board.
      (set-list-ref
        board
        (car coordinates)
        (set-nd (list-ref board (car coordinates)) (cdr coordinates) value)
      )
    )
  )

  ; Checks if the victory condition has been met.
  (define (is-victory board mask dimensions)
    (if (equal? (length dimensions) 0)
      ; Base case. Every non-bomb square must be revealed.
      (or mask (equal? board -1))

      ; Recursive case. All smaller dimensions must be in a victory state.
      (all (map
        (lambda (cons)
          (is-victory (car cons) (cdr cons) (cdr dimensions))
        )
        (zip board mask)
      ))
    )
  )

  ; All get/set helpers for the game.
  (define (game-get-state game) ((list-ref game 0)))
  (define (game-set-state game state) ((list-ref game 1) state))
  (define (game-get-board game) ((list-ref game 2)))
  (define (game-set-board game board) ((list-ref game 3) board))
  (define (game-get-mask game) ((list-ref game 4)))
  (define (game-set-mask game mask) ((list-ref game 5) mask))
  (define (game-get-dimensions game) ((list-ref game 6)))

  ; Starts a new game and returns an instance (as a function list) with appropriate getter and setter methods.
  (define (new-game-nd dimensions bombs)
    (begin
      ; Set up instance variables.
      (define state 0)
      (define board (initialize-nd dimensions 0))
      (define mask (initialize-nd dimensions #f))

      ; Set up instance methods.
      (define self (list
        ; Get state.
        (lambda () state)
        ; Set state.
        (lambda (new_state) (set! state new_state))
        ; Get board.
        (lambda () board)
        ; Set board.
        (lambda (new_board) (set! board new_board))
        ; Get mask.
        (lambda () mask)
        ; Set mask.
        (lambda (new_mask) (set! mask new_mask))
        ; Get dimensions.
        (lambda () dimensions)
      ))

      ; Go through each bomb to place it and increment the neighbors.
      (map (lambda (bomb)
        (begin
          (game-set-board self (set-nd (game-get-board self) bomb -1))
          (map (lambda (neighbor)
            (begin
              (define value (get-nd (game-get-board self) neighbor))
              (if (>= value 0)
                (game-set-board self (set-nd (game-get-board self) neighbor (+ value 1)))
                (list)
              )
            )
          ) (neighbors-nd dimensions bomb))
        )
      ) bombs)

      ; Return the list of methods which can be used to access and mutate the instance.
      self
    )
  )

  ; Recursively digs up the square at coordinates and neighboring squares. Returns the number of squares dug.
  (define (dig-nd game coordinates)
    ; Check the game state and mask before digging.
    (if (or (get-nd (game-get-mask game) coordinates) (not (equal? (game-get-state game) 0)))
      ; Do nothing because either the square is already revealed or the game is not ongoing.
      0

      ; Check if we dug a bomb.
      (if (equal? (get-nd (game-get-board game) coordinates) -1)
        ; We dug a bomb. Reveal the square and update the game state.
        (begin
          (game-set-mask game (set-nd (game-get-mask game) coordinates #t))
          (game-set-state game 2)
          1
        )

        ; We dug a non-bomb square.
        (begin
          ; Define a helper function to do the recursive digging.
          (define (dig-helper coordinates)
            ; Check if the square was already dug.
            (if (get-nd (game-get-mask game) coordinates)
              ; Already dug square.
              0

              ; Not already dug. Reveal and recursively dig if necessary.
              (begin
                (game-set-mask game (set-nd (game-get-mask game) coordinates #t))
                (if (equal? (get-nd (game-get-board game) coordinates) 0)
                  ; Get the sum of all recursive digs.
                  (reduce +
                    (map
                      (lambda (neighbor) (dig-helper neighbor))
                      (neighbors-nd (game-get-dimensions game) coordinates)
                    )
                  1)

                  ; No neighbors to dig.
                  1
                )
              )
            )
          )

          ; Get the total number of squares dug.
          (define count (dig-helper coordinates))

          ; Check for victory condition and update the game state if necessary.
          (if (is-victory (game-get-board game) (game-get-mask game) (game-get-dimensions game))
            (game-set-state game 1)
            (list)
          )

          ; Return the total squares dug.
          count
        )
      )
    )
  )
)
