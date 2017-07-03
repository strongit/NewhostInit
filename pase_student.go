package main

import (
	"fmt"
)

type student struct {
	Name string
	Age  int
}

func pase_student() {
	m := make(map[string]*student)
	stus := []student{
		{Name: "zhou", Age: 24},
		{Name: "li", Age: 23},
		{Name: "wang", Age: 22},
	}
	fmt.Println(m)
	for _, stu := range stus {
		m[stu.Name] = &stu
		fmt.Println(m[stu.Name])
	}

}

func main() {
	pase_student()
}
