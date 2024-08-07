#include "DetectionEngine.h"
#include <iostream>
#include <sstream>
#include <fstream>
#include <vector>
#include <Poco/Net/HTTPClientSession.h>
#include <Poco/Net/HTTPRequest.h>
#include <Poco/Net/HTTPResponse.h>
#include <Poco/StreamCopier.h>

// Function to retrieve the API key from a configuration file
std::string getApiKey() {
    std::ifstream configFile("api_key.config");
    std::string line;
    std::string prefix = "API_KEY=";
    if (configFile.is_open()) {
        while (getline(configFile, line)) {
            size_t prefixPosition = line.find(prefix);
            if (prefixPosition == 0) {
                return line.substr(prefix.length());
            }
        }
        configFile.close();
    } else {
        std::cerr << "Unable to open API key configuration file." << std::endl;
    }
    return "";
}

// Function to fetch threat data from the OTX API
void DetectionEngine::fetchThreatData() {
    std::string apiKey = getApiKey();
    if (apiKey.empty()) {
        std::cerr << "API key is not set in the configuration file." << std::endl;
        return;
    }

    Poco::Net::HTTPClientSession session("otx.alienvault.com");
    Poco::Net::HTTPRequest request(Poco::Net::HTTPRequest::HTTP_GET, "/api/v1/pulses/subscribed", Poco::Net::HTTPMessage::HTTP_1_1);
    request.set("X-OTX-API-KEY", apiKey);

    session.sendRequest(request);
    Poco::Net::HTTPResponse response;
    std::istream& rs = session.receiveResponse(response);

    std::stringstream ss;
    Poco::StreamCopier::copyStream(rs, ss);  // Corrected method name here
    std::string responseBody = ss.str();

    std::cout << "API Response: " << responseBody << std::endl;
}