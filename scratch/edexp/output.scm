; the output, manually formatted for legibility

(define (fib-rec n)
  (if (< n 2)
    n
    (+ (fib-rec (- n 1)) (fib-rec (- n 2)))))

(display (fib-rec 10))
