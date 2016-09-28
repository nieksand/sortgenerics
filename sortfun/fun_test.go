package main

import (
	"math/rand"
	"testing"

	"github.com/nieksand/sortgenerics/specint"
	"github.com/nieksand/sortgenerics/specint32"
	"github.com/nieksand/sortgenerics/specint8"
	"github.com/nieksand/sortgenerics/specstring"
	libsort "sort"
)

var numElem = 10000

var testDatInt []int
var testDatInt8 []int8
var testDatInt32 []int32
var testDatString []string

func init() {
	testDatInt = make([]int, numElem)
	for i := 0; i < numElem; i++ {
		testDatInt[i] = rand.Int()
	}

	testDatInt8 = make([]int8, numElem)
	for i := 0; i < numElem; i++ {
		testDatInt8[i] = int8(rand.Int())
	}

	testDatInt32 = make([]int32, numElem)
	for i := 0; i < numElem; i++ {
		testDatInt32[i] = rand.Int31()
	}

	testDatString = make([]string, numElem)
	alpha := "abcdefghijklmnopqrstuvwxyz"
	bs := make([]byte, 8)
	for i := 0; i < numElem; i++ {
		for j := 0; j < len(bs); j++ {
			bs[j] = alpha[rand.Intn(len(alpha))]
		}
		testDatString[i] = string(bs)
	}
}

func TestSpecInt(t *testing.T) {
	vs := make([]int, numElem)
	copy(vs, testDatInt)
	specint.SpecializedSort(vs)
	if !libsort.IntsAreSorted(vs) {
		t.Error("specialized int not sorted")
	}
}

func TestSpecString(t *testing.T) {
	vs := make([]string, numElem)
	copy(vs, testDatString)
	specstring.SpecializedSort(vs)
	if !libsort.StringsAreSorted(vs) {
		t.Error("specialized string not sorted")
	}
}

func BenchmarkLibInt(b *testing.B) {
	vs := make([]int, numElem)
	b.ResetTimer()

	for i := 0; i < b.N; i++ {
		b.StopTimer()
		copy(vs, testDatInt)
		b.StartTimer()
		libsort.Ints(vs)
	}
}

func BenchmarkSpecInt(b *testing.B) {
	vs := make([]int, numElem)
	b.ResetTimer()

	for i := 0; i < b.N; i++ {
		b.StopTimer()
		copy(vs, testDatInt)
		b.StartTimer()
		specint.SpecializedSort(vs)
	}
}

type Int8Slice []int8

func (p Int8Slice) Len() int           { return len(p) }
func (p Int8Slice) Less(i, j int) bool { return p[i] < p[j] }
func (p Int8Slice) Swap(i, j int)      { p[i], p[j] = p[j], p[i] }

func BenchmarkLibInt8(b *testing.B) {
	vs := make(Int8Slice, numElem)
	b.ResetTimer()

	for i := 0; i < b.N; i++ {
		b.StopTimer()
		copy(vs, Int8Slice(testDatInt8))
		b.StartTimer()
		libsort.Sort(vs)
	}
}

func BenchmarkSpecInt8(b *testing.B) {
	vs := make([]int8, numElem)
	b.ResetTimer()

	for i := 0; i < b.N; i++ {
		b.StopTimer()
		copy(vs, testDatInt8)
		b.StartTimer()
		specint8.SpecializedSort(vs)
	}
}

type Int32Slice []int32

func (p Int32Slice) Len() int           { return len(p) }
func (p Int32Slice) Less(i, j int) bool { return p[i] < p[j] }
func (p Int32Slice) Swap(i, j int)      { p[i], p[j] = p[j], p[i] }

func BenchmarkLibInt32(b *testing.B) {
	vs := make(Int32Slice, numElem)
	b.ResetTimer()

	for i := 0; i < b.N; i++ {
		b.StopTimer()
		copy(vs, Int32Slice(testDatInt32))
		b.StartTimer()
		libsort.Sort(vs)
	}
}

func BenchmarkSpecInt32(b *testing.B) {
	vs := make([]int32, numElem)
	b.ResetTimer()

	for i := 0; i < b.N; i++ {
		b.StopTimer()
		copy(vs, testDatInt32)
		b.StartTimer()
		specint32.SpecializedSort(vs)
	}
}

func BenchmarkLibString(b *testing.B) {
	vs := make([]string, numElem)
	b.ResetTimer()

	for i := 0; i < b.N; i++ {
		b.StopTimer()
		copy(vs, testDatString)
		b.StartTimer()
		libsort.Strings(vs)
	}
}

func BenchmarkSpecString(b *testing.B) {
	vs := make([]string, numElem)
	b.ResetTimer()

	for i := 0; i < b.N; i++ {
		b.StopTimer()
		copy(vs, testDatString)
		b.StartTimer()
		specstring.SpecializedSort(vs)
	}
}
