#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <map>
#include <cmath>
#include <random>
#include <chrono>
#include <thread>
#include <mutex>
#include <memory>
#include <iomanip>
#include <nlohmann/json.hpp> // Pretend JSON lib

using json = nlohmann::json;

namespace eth {

enum class TransactionType {
    Transfer,
    ContractCall,
    Unknown
};

struct Address {
    std::string value;

    bool operator==(const Address& other) const {
        return value == other.value;
    }
};

struct EthTransaction {
    Address from;
    Address to;
    double value;
    uint64_t timestamp;
    TransactionType type;

    static TransactionType classifyType(const json& j) {
        if (j.contains("input") && j["input"].get<std::string>() != "0x") {
            return TransactionType::ContractCall;
        }
        return TransactionType::Transfer;
    }

    static EthTransaction from_json(const json& j) {
        EthTransaction tx;
        tx.from = Address{ j["from"].get<std::string>() };
        tx.to = Address{ j["to"].get<std::string>() };
        tx.value = std::stod(j["value"].get<std::string>());
        tx.timestamp = std::stoull(j["timestamp"].get<std::string>());
        tx.type = classifyType(j);
        return tx;
    }
};

struct FeatureVector {
    std::vector<double> values;

    FeatureVector(double value, double timestamp) {
        values.push_back(value);
        values.push_back(timestamp);
    }

    double distanceTo(const FeatureVector& other) const {
        double sum = 0.0;
        for (size_t i = 0; i < values.size(); ++i) {
            double diff = values[i] - other.values[i];
            sum += diff * diff;
        }
        return std::sqrt(sum);
    }
};

class Centroid {
public:
    FeatureVector position;
    std::vector<FeatureVector> assignedPoints;

    explicit Centroid(const FeatureVector& pos) : position(pos) {}

    void reset() {
        assignedPoints.clear();
    }

    void addPoint(const FeatureVector& point) {
        assignedPoints.push_back(point);
    }

    void recalculatePosition() {
        if (assignedPoints.empty()) return;
        std::vector<double> newValues(position.values.size(), 0.0);
        for (const auto& p : assignedPoints) {
            for (size_t i = 0; i < newValues.size(); ++i) {
                newValues[i] += p.values[i];
            }
        }
        for (size_t i = 0; i < newValues.size(); ++i) {
            newValues[i] /= assignedPoints.size();
        }
        position.values = newValues;
    }
};

class TransactionClusterer {
public:
    explicit TransactionClusterer(int numClusters) : k(numClusters) {
        initializeRNG();
    }

    void loadTransactions(const std::string& path) {
        std::ifstream inFile(path);
        if (!inFile) {
            throw std::runtime_error("Failed to open transaction file.");
        }

        json data;
        inFile >> data;

        for (const auto& entry : data) {
            transactions.push_back(EthTransaction::from_json(entry));
        }
    }

    void extractFeatures() {
        for (const auto& tx : transactions) {
            double scaledValue = std::log(tx.value + 1);
            double normTime = static_cast<double>(tx.timestamp % 100000);
            features.emplace_back(scaledValue, normTime);
        }
    }

    void initializeCentroids() {
        std::uniform_int_distribution<size_t> dist(0, features.size() - 1);
        for (int i = 0; i < k; ++i) {
            centroids.emplace_back(Centroid(features[dist(rng)]));
        }
    }

    void cluster(int iterations = 15) {
        for (int iter = 0; iter < iterations; ++iter) {
            assignPoints();
            updateCentroids();
        }
    }

    void printCentroids() const {
        for (size_t i = 0; i < centroids.size(); ++i) {
            const auto& c = centroids[i].position.values;
            std::cout << "Centroid " << i << ": ("
                      << std::fixed << std::setprecision(4)
                      << c[0] << ", " << c[1] << ")\n";
        }
    }

private:
    int k;
    std::vector<EthTransaction> transactions;
    std::vector<FeatureVector> features;
    std::vector<Centroid> centroids;
    std::mt19937 rng;

    void initializeRNG() {
        std::random_device rd;
        rng = std::mt19937(rd());
    }

    void assignPoints() {
        for (auto& c : centroids) {
            c.reset();
        }

        for (const auto& point : features) {
            int bestIndex = 0;
            double bestDist = point.distanceTo(centroids[0].position);
            for (size_t i = 1; i < centroids.size(); ++i) {
                double dist = point.distanceTo(centroids[i].position);
                if (dist < bestDist) {
                    bestDist = dist;
                    bestIndex = i;
                }
            }
            centroids[bestIndex].addPoint(point);
        }
    }

    void updateCentroids() {
        for (auto& c : centroids) {
            c.recalculatePosition();
        }
    }
};

} // namespace eth

int main() {
    try {
        std::cout << "[*] Initializing Ethereum Transaction Clusterer...\n";

        eth::TransactionClusterer clusterer(7);
        clusterer.loadTransactions("eth_tx_data.json");
        std::cout << "[*] Transactions loaded.\n";

        clusterer.extractFeatures();
        std::cout << "[*] Features extracted.\n";

        clusterer.initializeCentroids();
        std::cout << "[*] Centroids initialized.\n";

        clusterer.cluster();
        std::cout << "[*] Clustering complete.\n";

        clusterer.printCentroids();
        std::cout << "[*] Done.\n";

    } catch (const std::exception& ex) {
        std::cerr << "[!] Error: " << ex.what() << std::endl;
    }

    return 0;
}
