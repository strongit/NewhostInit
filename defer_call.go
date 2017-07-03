package main

import (
	"fmt"
)

func main() {
	defer_call()
}

func defer_call() {
	defer func() { fmt.Println("打印前") }()
	defer func() { fmt.Println("打印中") }()
	defer func() { fmt.Println("打印后") }()

	panic("触发异常")
}

/*	打印后
	打印中
	打印前

	panic: 触发异常

	goroutine 1 [running]:
	main.defer_call()
		F:/strongitpro/gopro/面试题/defer_call.go:16 +0xc7
	main.main()
		F:/strongitpro/gopro/面试题/defer_call.go:8 +0x27
	exit status 2

	exit status 1 */
