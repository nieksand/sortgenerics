# Overhead of Go's Generic Sort
This started while prototyping an idea to make smarter external merge sorts
through additional bookkeeping and introspection.  I began with a fairly naive,
top-down merge sort and was surprised to see it matching and even drastically
outperforming the standard library's sort routine for some inputs.

That led me to ponder just how much overhead comes sort.Sort() forcing the use
of an interface:

* https://golang.org/pkg/sort/#Interface

I hacked together a Python script which takes the standard library's
implementation and emits specialized output for a given []type.  So rather than
using interface functions like Swap() and Less(), it directly uses `a,b=b,a` and
`a<b`.

Whether you want to case this as an argument for generic in Go or just an
opportunity to make the compiler smarter on optimization is up to you.  I think
knowing the overhead of the generic vs. specialized implementation is
interesting in either case.

## Results
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

I'm seeing about a 1.5x to 2.5x performance penalty from the standard library
approach.  It is fun to play with the numElem variable to see how the size of
the random input array impacts the timings.

## Implementation
There is a super cheesy python script which has the standard library Sort
massaged with some Vim macro love.  The type gets string interpolated in.
Example usage:

	python specialize_sort.py specint8 int8 > specint8/sort.go
