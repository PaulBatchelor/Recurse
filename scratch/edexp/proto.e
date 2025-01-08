ns edexp_test
nn comments
nn structure
gr commentary on structure
nn program
ns +program
. define
co $ ../../comments/test_node
co $ ../../structure/fib_rec
co $ ../../generated/output.scm/fib_rec

nn ../comments/test_node
ln this is a test node
co $ ..

nn ../structure/fib_rec
ln top-level entry for fib-rec
co $ ..
co $ ../../generated/output.scm/fib_rec

+ fib-rec
co $ ../../comments/fib_rec
nn ../comments/fib_rec
ln A recursive definition for producing a fibonacci
ln sum
co $ ..

. n
-

+ if
co $ ../../structure/fib_rec/01_conditional
nn ../structure/fib_rec/01_conditional
ln Conditional structure handling base case if n < 2
co $ ..

+ <
. n
. 2

- n
co $ ../../structure/fib_rec/01_conditional/01_return_n
nn ../structure/fib_rec/01_conditional/01_return_n
co $ ..
ln Return n if n < 2


+ +
co $ ../../structure/fib_rec/01_conditional/02_add_previous
nn ../structure/fib_rec/01_conditional/02_add_previous
co $ ..
ln Add previous values
+ fib-rec
+ -
. n
. 1
< 2
+ fib-rec
+ -
. n
. 2
< 5


. display
co $ ../../structure/run_test
nn ../structure/run_test
ln Run test and display output
co $ ..
+ fib-rec
co $ ../../comments/a_small_test
nn ../comments/a_small_test
ln Perform a small test, fib(10)
co $ ..
. 10

zz program
ns ..

nn generated/output.scm
fr output.scm

nn generated/output.scm/fib_rec
fr $ 3 6

nn generated/output.scm/display
fr $ 8
