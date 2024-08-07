#include <SFML/Graphics.hpp>
#include <vector>
#include <queue>
#include <unordered_map>
#include <unordered_set>
#include <limits> // Include for std::numeric_limits
#include <iostream>
#include <cmath>

// Define a simple structure for edges 
struct Edge {
    int target;
    int weight;
};

struct Node {
    int x, y;
    int id; // Unique id for nodes based on their position
    float f, g, h; // f = g + h, where g is the cost from the start, and h is the heuristic to the end
    Node* parent;  // Pointer to parent node for path reconstruction

    // Constructor for initializing node properties
    Node(int x, int y) : x(x), y(y), f(0), g(0), h(0), parent(nullptr) {
        id = y * 10 + x; // Assuming a 10x10 grid
    }

    // Calculate the heuristic using Manhattan distance (can be replaced with Euclidean or other appropriate heuristic)
    void calculateHeuristic(Node* end) {
        h = std::abs(end->x - x) + std::abs(end->y - y);
    }

    // Comparator to sort nodes by their f value
    bool operator<(const Node& other) const {
        return f > other.f; // Reversed to make std::priority_queue work
    }
};

// Helper function to draw the grid and the path
void drawGrid(sf::RenderWindow& window, const std::vector<std::vector<Node>>& grid, Node* path) {
    window.clear(sf::Color::Black);
    int size = 40; // Size of each grid cell
    for (const auto& row : grid) {
        for (const auto& node : row) {
            sf::RectangleShape rect(sf::Vector2f(size - 1, size - 1));
            rect.setPosition(node.x * size, node.y * size);
            rect.setFillColor(sf::Color::White); // Default color for unvisited nodes

            // Color visited nodes
            if (node.g > 0) {
                rect.setFillColor(sf::Color::Green);
            }
            
            // Color the path
            if (node.parent != nullptr) {
                rect.setFillColor(sf::Color::Blue);
            }

            window.draw(rect);
        }
    }

    // Draw the path by tracing back from the goal node
    while (path != nullptr) {
        sf::RectangleShape pathRect(sf::Vector2f(size - 1, size - 1));
        pathRect.setPosition(path->x * size, path->y * size);
        pathRect.setFillColor(sf::Color::Red);
        window.draw(pathRect);
        path = path->parent;
    }

    window.display();
}

// Define a simple graph structure using an adjacency list
using Graph = std::unordered_map<int, std::vector<Edge>>;

// Helper function to create a simple graph
Graph createGraph() {
    Graph g;
    g[0] = {{1, 4}, {2, 1}};
    g[1] = {{3, 1}};
    g[2] = {{1, 2}, {3, 5}};
    g[3] = {};
    return g;
}

void drawGraph(sf::RenderWindow& window, const Graph& graph, const std::unordered_map<int, int>& distances, const std::unordered_set<int>& visited, int current) {
    window.clear(sf::Color::Black);
    sf::Font font;
    if (!font.loadFromFile("arial.ttf")) {
        std::cerr << "Failed to load font!" << std::endl;
        return;
    }

    float radius = 30;
    std::vector<sf::Vector2f> positions = {{100, 300}, {300, 100}, {300, 500}, {500, 300}};  // Node positions for visual simplicity

    // Draw edges
    for (const auto& pair : graph) {
        int from = pair.first;
        for (const Edge& edge : pair.second) {
            int to = edge.target;
            sf::Vertex line[] = {
                sf::Vertex(positions[from], sf::Color::White),
                sf::Vertex(positions[to], sf::Color::White),
            };

            window.draw(line, 2, sf::Lines);
        }
    }

    // Draw nodes
    for (const auto& pair : distances) {
        int node = pair.first;
        sf::CircleShape circle(radius);
        circle.setPosition(positions[node].x - radius, positions[node].y - radius);
        circle.setFillColor(visited.count(node) ? sf::Color::Green : sf::Color::Blue);
        if (node == current) {
            circle.setOutlineColor(sf::Color::Red);
            circle.setOutlineThickness(5);
        }

        window.draw(circle);

        sf::Text text(std::to_string(pair.second), font, 20);
        text.setPosition(positions[node].x - text.getLocalBounds().width / 2, positions[node].y - 10);
        text.setFillColor(sf::Color::White);
        window.draw(text);
    }

    window.display();
}

void merge(std::vector<int>& arr, int l, int m, int r, sf::RenderWindow& window) {
    int i, j, k;
    int n1 = m - l + 1;
    int n2 = r - m;

    // Create temp arrays
    std::vector<int> L(n1), R(n2);

    // Copy data to temp arrays L[] and R[]
    for (i = 0; i < n1; i++)
        L[i] = arr[l + i];
    for (j = 0; j < n2; j++)
        R[j] = arr[m + 1 + j];
    

    // Merge the temp arrays back into arr[l..r]
    i = 0;
    j = 0;
    k = l;
    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) {
            arr[k] = L[i];
            i++;
        } else {
            arr[k] = R[j];
            j++;
        }
        k++;

        // Visualization step: Redraw the array with updated elements
        window.clear(sf::Color::Black);
        drawArray(window, arr, {l, r});
        window.display();
        sf::sleep(sf::milliseconds(100)); // Pause for visibility
    }

    // Copy the remaining elements of L[], if there are any
    while (i < n1) {
        arr[k] = L[i];
        i++;
        k++;

        window.clear(sf::Color::Black);
        drawArray(window, arr, {l, r});
        window.display();
        sf::sleep(sf::milliseconds(100)); // Same as before, pause for visibility
    }

    // Copy the remaining elements of R[], if they exist
    while (j < n2) {
        arr[k] = R[j];
        j++;
        k++;

        window.clear(sf::Color::Black);
        drawArray(window, arr, {l, r});
        window.display();
        sf::sleep(sf::milliseconds(100)); // Pausing for visibility again
    }
}

void mergeSort(std::vector<int>& arr, int l, int r, sf::RenderWindow& window) {
    if (l < r) {
        // Same as (l+r)/2, but avoids overflow for large l and h
        int m = l + (r - l) / 2;

        // Sort first and second halves
        mergeSort(arr, l, m, window);
        mergeSort(arr, m + 1, r, window);

        merge(arr, l, m, r, window);
    }
}

void visualizeMergeSort() {
    sf::RenderWindow window(sf::VideoMode(800, 600), "Merge Sort Visualizer");
    std::vector<int> arr = {38, 27, 43, 3, 9, 82, 10};

    // Initial call to merge sort function
    mergeSort(arr, 0, arr.size() - 1, window);

    while (window.isOpen()) {
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed)
                window.close();
        }

        window.clear(sf::Color::Black);
        drawArray(window, arr, {});
        window.display();
    }
}

// Helper function to draw the array elements as bars
void drawArray(sf::RenderWindow& window, const std::vector<int>& arr,
               const std::unordered_set<int>& highlightIndices,
               sf::Color highlightColor = sf::Color::Red,
               sf::Color defaultColor = sf::Color::White,
               bool textDisplay = false) {
    window.clear(sf::Color::Black);
    float barWidth = 800.0f / arr.size(); // Calculate the width of each bar based on array size
    sf::Font font;
    if (textDisplay) {
        if (!font.loadFromFile("arial.ttf")) { // Load font and handle case if font is not loaded
            std::cerr << "Failed to load font!" << std::endl;
            return;
        }
    }

    for (size_t i = 0; i < arr.size(); i++) {
        sf::RectangleShape bar(sf::Vector2f(barWidth - 1, arr[i] * 5)); // Creates rectangle for each element 
        bar.setPosition(i * barWidth, window.getSize().y - arr[i] * 5); 
        bar.setFillColor(highlightIndices.count(i) ? highlightColor : defaultColor);
        window.draw(bar);

        if (textDisplay) {
            sf::Text text(std::to_string(arr[i]), font, 15);
            text.setPosition(i * barWidth + (barWidth / 2) - text.getLocalBounds().width / 2,
                             window.getSize().y - arr[i] * 5 - 20);
            text.setFillColor(sf::Color::Yellow);
            window.draw(text);
        }
    }

    window.display(); // Display everything that has been drawn to the window
}

void visualizeBinarySearch() {
    sf::RenderWindow window(sf::VideoMode(800, 600), "Binary Search Visualizer");
    std::vector<int> arr = {3, 9, 10, 25, 35, 45, 87}; // Example sorted array
    int target = 25; // Target value for binary search

    int left = 0, right = arr.size() - 1, mid, foundIndex = -1;

    // Main loop to keep the window open
    while (window.isOpen()) {
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed)
                window.close();
        }

        // Perform binary search iteration until target is found or search space is empty
        if (left <= right) {
            mid = left + (right - left) / 2; // Compute the middle index

            // Visualization step: Redraw the array with the current search boundaries
            window.clear(sf::Color::Black);
            drawArray(window, arr, {left, mid, right});
            window.display();
            sf::sleep(sf::milliseconds(1000)); // Pause for visibility

            // Check if the mid element is the target
            if (arr[mid] == target) {
                foundIndex = mid; // Save the index of found element
                std::cout << "Element found at index " << mid << std::endl;
                break; // Stop search
            }

            // Adjust search range based on comparison
            if (arr[mid] < target)
                left = mid + 1;
            else
                right = mid - 1;
        } else {
            // Element is not found
            std::cout << "Element is not found in the array." << std::endl;
            break;
        }
    }
    
    // Final display with the found element highlighted
    if (foundIndex != -1) {
        while (window.isOpen()) {
            sf::Event event;
            while (window.pollEvent(event)) {
                if (event.type == sf::Event::Closed)
                    window.close();
            }

            window.clear(sf::Color::Black);
            drawArray(window, arr, {foundIndex}, sf::Color::Red, sf::Color::White, true);
            window.display();
        }
    }
}

void visualizeDijkstra() {
    sf::RenderWindow window(sf::VideoMode(800, 600), "Dijkstra's Algorithm Visualizer");
    Graph graph = createGraph();
    std::priority_queue<std::pair<int, int>, std::vector<std::pair<int, int>>, std::greater<>> pq; // Min-heap priority queue
    std::unordered_map<int, int> distances;
    std::unordered_set<int> visited;

    // Initialize distances
    for (const auto& pair : graph) {
        distances[pair.first] = std::numeric_limits<int>::max();
    }

    int startNode = 0;
    distances[startNode] = 0;
    pq.push({0, startNode});

    while (!pq.empty() && window.isOpen()) {
        auto [cost, node] = pq.top();
        pq.pop();

        if (!visited.insert(node).second) continue; // Skip when already visited

        // Process each neighbour
        for (const auto& edge : graph[node]) {
            int next = edge.target;
            int nextCost = cost + edge.weight;
            if (nextCost < distances[next]) {
                distances[next] = nextCost;
                pq.push({nextCost, next});
            }
        }

        // Visualize the current state of the graph
        drawGraph(window, graph, distances, visited, node);
        sf::sleep(sf::milliseconds(1000)); // Pause for visibility

        // Handle Window events
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed)
                window.close();
        }
    }

    // Final display showing all nodes processed
    while (window.isOpen()) {
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed)
                window.close();
        }

        drawGraph(window, graph, distances, visited, -1); // No current node to highlight
    }
}

void visualizeFibonacci() {
    sf::RenderWindow window(sf::VideoMode(800, 600), "Fibonacci Sequence Visualizer");
    sf::Font font;
    if (!font.loadFromFile("arial.ttf")) {
        std::cerr << "Failed to load font!" << std::endl;
        return;
    }

    int n = 15; // Display the first 15 Fibonacci numbers
    std::vector<int> fib(n, 0); // Vector to store Fibonacci numbers

    // Initialize the first two Fibonacci numbers
    if (n > 0) fib[0] = 0;
    if (n > 1) fib[1] = 1;
    
    // Compute Fibonacci numbers iteratively
    for (int i = 2; i < n; ++i) {
        fib[i] = fib[i - 1] + fib[i - 2];
    }

    while (window.isOpen()) {
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed)
                window.close();
        }

        window.clear(sf::Color::Black);

        // Display Fibonacci numbers
        for (int i = 0; i < n; ++i) {
            sf::Text text(std::to_string(fib[i]), font, 24);
            text.setPosition(50, 50 + i * 30); // Position the text vertically spaced
            text.setFillColor(sf::Color::White);
            window.draw(text);
        }

        window.display();

        sf::sleep(sf::milliseconds(500)); // Slow down the visualization
    }
}

void visualizeAStar() {
    sf::RenderWindow window(sf::VideoMode(400, 400), "A* Pathfinding Visualizer");
    std::priority_queue<Node> openSet;

    // Create 10x10 grid
    std::vector<std::vector<Node>> grid;
    for (int y = 0; y < 10; y++) {
        std::vector<Node> row;
        for (int x = 0; x < 10; x++) {
            row.emplace_back(x, y);
        }

        grid.push_back(row);
    }

    Node* start = &grid[0][0];
    Node* goal = &grid[9][9];
    start->g = 0;
    start->calculateHeuristic(goal);
    start->f = start->h; // Initial f is the heuristic
    openSet.push(*start);

    Node* current = nullptr;

    while (!openSet.empty() && window.isOpen()) {
        current = &grid[openSet.top().y][openSet.top().x];
        openSet.pop();

        if (current == goal) {
            break; // Path has been found
        }

        // Explore neighbours
        std::vector<std::pair<int, int>> directions = {{0, 1}, {1, 0}, {0, -1}, {-1, 0}}; // Four possible directions
        for (auto& dir : directions) {
            int nx = current->x + dir.first;
            int ny = current->y + dir.second;

            if (nx >= 0 && nx < 10 && ny >= 0 && ny < 10) { // Check boundaries
                Node* neighbor = &grid[ny][nx];
                float tentative_g = current->g + 1; // Assume cost of 1 for each move
                if (tentative_g < neighbor->g) {
                    neighbor->parent = current;
                    neighbor->g = tentative_g;
                    neighbor->calculateHeuristic(goal);
                    neighbor->f = neighbor->g + neighbor->h;
                    openSet.push(*neighbor);
                }
            }
        }

        drawGrid(window, grid, nullptr); // Draw the grid without a final path

        // Handle window events
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed)
                window.close();
        }
    }

    // Draw the final path if the goal was reached
    if (current == goal) {
        drawGrid(window, grid, current); // Draw the grid with the final path

        while (window.isOpen()) {
            sf::Event event;
            while (window.pollEvent(event)) {
                if (event.type == sf::Event::Closed)
                    window.close();
            }
        }
    }
}

// Function to display the menu and handle user input 
void showMenu() {
    std::cout << "\nSelect an algorithm to visualize:\n"
              << "1. Merge Sort\n"
              << "2. Binary Search\n"
              << "3. Dijkstra's Algorithm\n"
              << "4. Fibonacci Sequence\n"
              << "5. A* Search Algorithm\n"
              << "6. Exit\n"
              << "Enter your choice (1-6): ";
}

// Main function to drive the program
int main() {
    int choice; // Variable to store the user's choice

    while (true) {
        showMenu(); // Display the menu to the user
        std::cin >> choice;

        // Check for invalid input
        if (std::cin.fail()) {
            std::cin.clear(); // Clear error flag
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); // Ignore wrong input
            std::cout << "Invalid input, please enter a number between 1 and 6.\n";
            continue; // Skip the rest of the loop iteration
        }

        // Process the user's input
        switch (choice) {
            case 1:
                visualizeMergeSort();
                break;
            case 2:
                visualizeBinarySearch();
                break;
            case 3:
                visualizeDijkstra();
                break;
            case 4:
                visualizeFibonacci();
                break;
            case 5:
                visualizeAStar();
                break;
            case 6:
                std::cout << "Closing down visualizer.\n";
                return 0; // Exit the program
            default:
                std::cout << "Invalid choice. Please try again with a number between 1 and 6.\n";
        }
    }
}
