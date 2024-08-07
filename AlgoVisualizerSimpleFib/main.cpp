#include <iostream>
#include <vector>
#include <thread>
#include <chrono>

// Function to print the current Fibonacci sequence
void printFibonacci(const std::vector<int>& fib) {
    for (int value : fib) {
        for (int i = 0; i < value; ++i) {
            std::cout <<"<3";
        }

        std::cout << " (" << value << ") " << std::endl;
    }

    std::cout << std::endl;
}

// Function to generate and visualize the Fibonacci sequence
void visualizeFibonacci(int n) {
    if (n <= 0) return; // If no elements are requested, exit early.

    std::vector<int> fib;
    fib.reserve(n); // Reserve memory to avoid multiple reallocations.

    // Handle the special case for n = 1 and n = 2 separately
    if (n >= 1) fib.push_back(0);
    if (n >= 2) fib.push_back(1);

    // Compute the Fibonacci numbers and visualize incrementally 
    for (int i = 2; i < n; ++i) {
        int next = fib[i - 1] + fib[i - 2];
        fib.push_back(next);
        printFibonacci(fib); // Visualize the current state of Fibonacci
        std::this_thread::sleep_for(std::chrono::milliseconds(500)); // We are, in fact, pausing for visualization observation
    }

    // Final print to show the complete sequence
    printFibonacci(fib);
}

int main() {
    int n;
    std::cout << "Enter the number of Fibonacci numbers to visualize: ";
    std::cin >> n;

    visualizeFibonacci(n);

    return 0;
}