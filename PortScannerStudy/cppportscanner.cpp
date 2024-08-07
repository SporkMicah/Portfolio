// This only works with IP addresses. URL support will be added at a later date.


#include <iostream>
#include <winsock2.h>
#include <ws2tcpip.h>
#include <string>
#include <vector>
#include <thread>
#include <mutex>

#pragma comment(lib, "Ws2_32.lib")

std::mutex cout_mutex;

void scan_port(const std:: string& ip, int port, const std::string& scan_type) {
    WSADATA wsaData;
    WSAStartup(MAKEWORD(2, 2), &wsaData);

    SOCKET sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_port = htons(port);
    inet_pton(AF_INET, ip.c_str(), &addr.sin_addr);

    int result = SOCKET_ERROR;
    if (scan_type == "connect") {
        result = connect(sock, (sockaddr*)&addr, sizeof(addr));
    }

    if (result != SOCKET_ERROR) {
        std::lock_guard<std::mutex> lock(cout_mutex);
        std::cout << "Port " << port << " is open.";

        // Simple service identification by sending a HTTP GET request and checking the response
        if (port == 80) {
            std::string http_get = "Get / HTTP/1.1\r\nHost: " + ip + "\r\n\r\n";
            send(sock, http_get.c_str(), http_get.length(), 0);
            char response[4096] = {};
            recv(sock, response, sizeof(response), 0);
            std::cout << " HTTP service detected.";
        }

        std::cout << std::endl;

    }
    closesocket(sock);
    WSACleanup();
}

void worker_thread(const std::string& ip, int start_port, int end_port, const std:: string& scan_type) {
    for (int port = start_port; port <= end_port; ++port) {
        scan_port(ip, port, scan_type);
    }
}

int main() {
    std::string target_ip = "INSERT IP ADDRESS HERE";
    int start_port = 1;
    int end_port = 100;
    int num_threads = 10;
    std::string scan_type = "connect";

    std::vector<std::thread> threads;
    int ports_per_thread = (end_port - start_port + 1) / num_threads;

    for (int i = 0; i < num_threads; ++i) {
        int thread_start_port = start_port + i * ports_per_thread;
        int thread_end_port = (i == num_threads -1) ? end_port : thread_start_port + ports_per_thread - 1;
        threads.emplace_back(worker_thread, target_ip, thread_start_port, thread_end_port, scan_type);
    }

    for (auto& t : threads) {
        t.join();
    }

    return 0;
}