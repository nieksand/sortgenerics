# Overhead of Go's Generic Sort
This started while prototyping an idea to make faster external merge sorts
through additional bookkeeping and introspection.  I began with a fairly naive,
top-down merge sort and was surprised to see it matching and even drastically
outperforming the standard library's sort routine for some inputs.

That led me to ponder just how much overhead comes from sort.Sort() forcing the
use of an interface:

* https://golang.org/pkg/sort/#Interface

I hacked together a Python script which takes the standard library's sort and
emits code specialized for a given []type.  So rather than using interface
functions like Swap() and Less(), it directly uses `a,b=b,a` and `a<b`.

You could see this as an argument for generics in Go.  Alternatively you could
argue that the optimizer be made smarter.  In either case, knowing the overhead
of the current implementation is quite interesting.

## Results
I'm seeing about a 1.5x to 2.5x performance penalty from the standard library's
current implementation.  It is fun to play with the numElem variable to see how
the size of the random input array impacts the timings.

These numbers come from Go 1.7.1 on my mid-2013 Macbook Air.  For each type,
BenchmarkLib is the standard library sort and BenchmarkSpec is the specialized
implementation.

From feedback on a Hacker News discussion, I added in a test case for
specializing sorts on a struct rather than a primitive type.  Potato has an int
and a string and we sort on the former.  Note that for this case, I can still
specialize the Swap and Len but not the Less operation.

With 10K random elements:

	BenchmarkLibInt-4       	   10000	   2045356 ns/op
	BenchmarkSpecInt-4      	   20000	    926124 ns/op

	BenchmarkLibInt8-4      	   10000	   1353532 ns/op
	BenchmarkSpecInt8-4     	   30000	    492396 ns/op

	BenchmarkLibInt32-4     	   10000	   1984590 ns/op
	BenchmarkSpecInt32-4    	   20000	    774953 ns/op

	BenchmarkLibString-4    	    5000	   3580412 ns/op
	BenchmarkSpecString-4   	    5000	   2471724 ns/op

	BenchmarkLibPotato-4    	   10000	   2166569 ns/op
	BenchmarkSpecPotato-4   	   10000	   1020842 ns/op

Sorting 10M random elements:

	BenchmarkLibInt-4       	       3	3540916295 ns/op
	BenchmarkSpecInt-4      	      10	1472208735 ns/op

	BenchmarkLibInt8-4      	      10	1353120802 ns/op
	BenchmarkSpecInt8-4     	      30	 478561462 ns/op

	BenchmarkLibInt32-4     	       3	3512489914 ns/op
	BenchmarkSpecInt32-4    	      10	1426428402 ns/op

	BenchmarkLibString-4    	       1	10616472819 ns/op
	BenchmarkSpecString-4   	       2	7489515205 ns/op

	BenchmarkLibPotato-4    	       3	3829722562 ns/op
	BenchmarkSpecPotato-4   	      10	1802874882 ns/op

You can run the benchmark yourself:

	prompt> cd sortfun
	prompt> go test -benchtime=10s -bench .

## Implementation
There is a super cheesy Python script which has the standard library Sort
massaged with some Vim macro love.  The []type gets string interpolated in.

Example usage:

	python specialize_sort.py specint8 int8 > specint8/sort.go
