"""
Super hacky Python code that generates a Go sort routine for specific slice
type.  You would be utterly nuts if you used this output for production.  So
unless you're a squirrel... don't.

The Sort code being specialized comes from the Go standard library.  It is
covered by the following license:

	// Copyright 2009 The Go Authors. All rights reserved.
	// Use of this source code is governed by a BSD-style
	// license that can be found in the LICENSE file.

"""
import sys

# Template is just the standard library's sort code with comments ripped out and
# with calls to Len, Swap, Less replaced with primitive operations.  The
# Interface itself is replaced with a slice of appropriate type.
template = """package %(pkg)s

func insertionSort(data []%(spectype)s, a, b int) {
	for i := a + 1; i < b; i++ {
		for j := i; j > a && data[j] < data[j-1]; j-- {
			data[j], data[j-1] = data[j-1], data[j]
		}
	}
}

func siftDown(data []%(spectype)s, lo, hi, first int) {
	root := lo
	for {
		child := 2*root + 1
		if child >= hi {
			break
		}
		if child+1 < hi && data[first+child] < data[first+child+1] {
			child++
		}
		if !(data[first+root] < data[first+child]) {
			return
		}
		data[first+root], data[first+child] = data[first+child], data[first+root]
		root = child
	}
}

func heapSort(data []%(spectype)s, a, b int) {
	first := a
	lo := 0
	hi := b - a

	for i := (hi - 1) / 2; i >= 0; i-- {
		siftDown(data, i, hi, first)
	}

	for i := hi - 1; i >= 0; i-- {
		data[first], data[first+i] = data[first+i], data[first]
		siftDown(data, lo, i, first)
	}
}

func medianOfThree(data []%(spectype)s, m1, m0, m2 int) {
	if data[m1] < data[m0] {
		data[m1], data[m0] = data[m0], data[m1]
	}
	if data[m2] < data[m1] {
		data[m2], data[m1] = data[m1], data[m2]
		if data[m1] < data[m0] {
			data[m1], data[m0] = data[m0], data[m1]
		}
	}
}

func swapRange(data []%(spectype)s, a, b, n int) {
	for i := 0; i < n; i++ {
		data[a+i], data[b+i] = data[b+i], data[a+i]
	}
}

func doPivot(data []%(spectype)s, lo, hi int) (midlo, midhi int) {
	m := lo + (hi-lo)/2
	if hi-lo > 40 {
		s := (hi - lo) / 8
		medianOfThree(data, lo, lo+s, lo+2*s)
		medianOfThree(data, m, m-s, m+s)
		medianOfThree(data, hi-1, hi-1-s, hi-1-2*s)
	}
	medianOfThree(data, lo, m, hi-1)

	pivot := lo
	a, c := lo+1, hi-1

	for ; a < c && data[a] < data[pivot]; a++ {
	}
	b := a
	for {
		for ; b < c && !(data[pivot] < data[b]); b++ {
		}
		for ; b < c && data[pivot] < data[c-1]; c-- {
		}
		if b >= c {
			break
		}
		data[b], data[c-1] = data[c-1], data[b]
		b++
		c--
	}
	protect := hi-c < 5
	if !protect && hi-c < (hi-lo)/4 {
		dups := 0
		if !(data[pivot] < data[hi-1]) {
			data[c], data[hi-1] = data[hi-1], data[c]
			c++
			dups++
		}
		if !(data[b-1] < data[pivot]) {
			b--
			dups++
		}
		if !(data[m] < data[pivot]) {
			data[m], data[b-1] = data[b-1], data[m]
			b--
			dups++
		}
		protect = dups > 1
	}
	if protect {
		for {
			for ; a < b && !(data[b-1] < data[pivot]); b-- {
			}
			for ; a < b && data[a] < data[pivot]; a++ {
			}
			if a >= b {
				break
			}
			data[a], data[b-1] = data[b-1], data[a]
			a++
			b--
		}
	}
	data[pivot], data[b-1] = data[b-1], data[pivot]
	return b - 1, c
}

func quickSort(data []%(spectype)s, a, b, maxDepth int) {
	for b-a > 12 {
		if maxDepth == 0 {
			heapSort(data, a, b)
			return
		}
		maxDepth--
		mlo, mhi := doPivot(data, a, b)
		if mlo-a < b-mhi {
			quickSort(data, a, mlo, maxDepth)
			a = mhi
		} else {
			quickSort(data, mhi, b, maxDepth)
			b = mlo
		}
	}
	if b-a > 1 {
		for i := a + 6; i < b; i++ {
			if data[i] < data[i-6] {
				data[i], data[i-6] = data[i-6], data[i]
			}
		}
		insertionSort(data, a, b)
	}
}

func SpecializedSort(data []%(spectype)s) {
	n := len(data)
	maxDepth := 0
	for i := n; i > 0; i >>= 1 {
		maxDepth++
	}
	maxDepth *= 2
	quickSort(data, 0, n, maxDepth)
}
"""

if __name__ == '__main__':
	if len(sys.argv) != 3:
		print "usage: python %s <go pkg> <go type>\n" % sys.argv[0]
		exit()

	print template % {'pkg': sys.argv[1], 'spectype': sys.argv[2]}
