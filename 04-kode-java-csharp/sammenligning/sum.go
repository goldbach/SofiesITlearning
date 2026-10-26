package main

import (
	"fmt"
	"time"
)

func main() {
	start := time.Now()
	var total int64
	for i := int64(0); i < 100_000_000; i++ {
		total += i % 7
	}
	fmt.Printf("%d %.2f s\n", total, time.Since(start).Seconds())
}
