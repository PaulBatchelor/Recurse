(defn dzfetch [nodepath index contents]
  (def row (index nodepath))
  (file/seek contents :set (row 0))

  (file/read contents (row 1))  
)

(defn load-index [keys-file]
  (var index @{})

  (var fp (file/open keys-file))
  (var lines
    (filter
      (fn [x] (> (length x) 0))
      (string/split "\n" (file/read fp :all))))
  (each line lines
    (def row (string/split ":" line))
    (set (index (row 0)) @[(eval-string (row 1)) (eval-string (row 2))]))
  (file/close fp)
  index
)
