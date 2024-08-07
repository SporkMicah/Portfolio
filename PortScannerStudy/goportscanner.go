package main

import (
	"fmt"
	"net"
	"sort"
	"sync"
	"time"
)

func worker(ports, results chan int, wg *sync.WaitGroup, target string) {
	defer wg.Done()
	for p := range ports {
		address := fmt.Sprintf("%s:%d", target, p)
		conn, err := net.DialTimeout("tcp", address, 1*time.Second)
		if err != nil {
			results <- 0
			continue
		}
		conn.Close()
		results <- p
	}
}

func main() {
	var wg sync.WaitGroup
	ports := make(chan int, 100)
	results := make(chan int)
	var openPorts []int

	target := "scanme.nmap.org"

	for i := 0; i < cap(ports); i++ {
		wg.Add(1)
		go worker(ports, results, &wg, target)
	}

	go func() {
		for i := 1; i <= 1024; i++ {
			ports <- i
		}
		close(ports)
	}()

	go func() {
		wg.Wait()
		close(results)
	}()

	for r := range results {
		if r != 0 {
			openPorts = append(openPorts, r)
		}
	}

	sort.Ints(openPorts)
	for _, port := range openPorts {
		fmt.Printf("Port %d is open\n", port)
	}
}