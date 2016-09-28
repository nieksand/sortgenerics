# Overhead of Go's Generic Sort
This started while prototyping an idea to make smarter external merge sorts
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
I'm seeing about a 1.5x to 2.5x performance penalty from the standard library
approach.  It is fun to play with the numElem variable to see how the size of
the random input array impacts the timings.

These numbers come from Go 1.7.1 on my mid-2013 Macbook Air.  For each type,
BenchmarkLib is the standard library sort and BenchmarkSpec is the specialized
implementation.

	BenchmarkLibInt-4       	    1000	   2087739 ns/op
	BenchmarkSpecInt-4      	    2000	    927293 ns/op

	BenchmarkLibInt8-4      	    1000	   1372540 ns/op
	BenchmarkSpecInt8-4     	    3000	    493541 ns/op

	BenchmarkLibInt32-4     	    1000	   2101148 ns/op
	BenchmarkSpecInt32-4    	    2000	    794551 ns/op

	BenchmarkLibString-4    	     500	   3623716 ns/op
	BenchmarkSpecString-4   	     500	   2537745 ns/op

You can run the benchmark yourself:

	prompt> cd sortfun
	prompt> go test -bench .

## Implementation
There is a super cheesy Python script which has the standard library Sort
massaged with some Vim macro love.  The []type gets string interpolated in.

Example usage:

	python specialize_sort.py specint8 int8 > specint8/sort.go
