#include <iostream>
#include <string>
#include <vector>
#include <fstream>
#include <sstream>
#include <openssl/evp.h>
#include <openssl/pem.h>
#include <openssl/param_build.h>
#include <openssl/core_names.h>
#include <openssl/sha.h>
#include <openssl/err.h>

// Helper function to print OpenSSL errors
void print_openssl_errors() {
    unsigned long err;
    while ((err = ERR_get_error()) != 0) {
        char *err_str = ERR_error_string(err, NULL);
        std::cerr << "OpenSSL error: " << err_str << std::endl;
    }
}

// Generate an address from a public key
std::string generate_address(EVP_PKEY* pkey) {
    // Get the public key bytes
    size_t pub_key_len = 0;
    
    // First, get the size needed
    if (EVP_PKEY_get_octet_string_param(pkey, OSSL_PKEY_PARAM_PUB_KEY, NULL, 0, &pub_key_len) != 1) {
        print_openssl_errors();
        std::cerr << "Error determining public key length" << std::endl;
        return "";
    }
    
    // Allocate memory
    std::vector<unsigned char> pubkey(pub_key_len);
    
    // Get the key bytes
    if (EVP_PKEY_get_octet_string_param(pkey, OSSL_PKEY_PARAM_PUB_KEY, pubkey.data(), pubkey.size(), &pub_key_len) != 1) {
        print_openssl_errors();
        std::cerr << "Error getting public key bytes" << std::endl;
        return "";
    }
    
    // Create a SHA-256 hash of the public key
    unsigned char sha256_hash[SHA256_DIGEST_LENGTH];
    SHA256(pubkey.data(), pubkey.size(), sha256_hash);
    
    // Convert hash to hex string
    std::string address;
    for (int i = 0; i < SHA256_DIGEST_LENGTH; i++) {
        char hex[3];
        sprintf(hex, "%02x", sha256_hash[i]);
        address += hex;
    }
    
    // Take first 40 chars for an address-like format
    return "0x" + address.substr(0, 40);
}

// Display the balance for a wallet
void displayBalance() {
    // Open the wallet file
    FILE* fp = fopen("wallet.pem", "r");
    if (!fp) {
        std::cerr << "Could not open wallet file" << std::endl;
        return;
    }
    
    // Read the private key
    EVP_PKEY* pkey = PEM_read_PrivateKey(fp, NULL, NULL, NULL);
    fclose(fp);
    
    if (!pkey) {
        print_openssl_errors();
        std::cerr << "Failed to load private key" << std::endl;
        return;
    }
    
    // Generate address from public key
    std::string address = generate_address(pkey);
    if (address.empty()) {
        EVP_PKEY_free(pkey);
        return;
    }
    
    // Here you would typically query a blockchain or database for the balance
    
    // For demonstration, just display the address
    std::cout << "Address: " << address << std::endl;
    std::cout << "Balance: 0.00000000 FRC" << std::endl;
    
    // Clean up
    EVP_PKEY_free(pkey);
}

// Generate a new wallet
void generateWallet(const std::string& password) {
    EVP_PKEY_CTX *pctx = NULL;
    EVP_PKEY *pkey = NULL;
    
    // Create a context for parameter generation
    pctx = EVP_PKEY_CTX_new_from_name(NULL, "EC", NULL);
    if (!pctx) {
        print_openssl_errors();
        return;
    }
    
    // Initialize parameter generation
    if (EVP_PKEY_paramgen_init(pctx) <= 0) {
        print_openssl_errors();
        EVP_PKEY_CTX_free(pctx);
        return;
    }
    
    // Set the EC curve name parameter (secp256k1 is common for cryptocurrencies)
    if (EVP_PKEY_CTX_set_ec_paramgen_curve_nid(pctx, NID_secp256k1) <= 0) {
        print_openssl_errors();
        EVP_PKEY_CTX_free(pctx);
        return;
    }
    
    // Create the parameter object
    EVP_PKEY *params = NULL;
    if (EVP_PKEY_paramgen(pctx, &params) <= 0) {
        print_openssl_errors();
        EVP_PKEY_CTX_free(pctx);
        return;
    }
    
    // Create a context for key generation
    EVP_PKEY_CTX_free(pctx);
    pctx = EVP_PKEY_CTX_new(params, NULL);
    if (!pctx) {
        print_openssl_errors();
        EVP_PKEY_free(params);
        return;
    }
    
    // Initialize key generation
    if (EVP_PKEY_keygen_init(pctx) <= 0) {
        print_openssl_errors();
        EVP_PKEY_CTX_free(pctx);
        EVP_PKEY_free(params);
        return;
    }
    
    // Generate the key pair
    if (EVP_PKEY_keygen(pctx, &pkey) <= 0) {
        print_openssl_errors();
        EVP_PKEY_CTX_free(pctx);
        EVP_PKEY_free(params);
        return;
    }
    
    // Clean up parameter generation
    EVP_PKEY_CTX_free(pctx);
    EVP_PKEY_free(params);
    
    // Save the key to a file
    FILE* fp = fopen("wallet.pem", "w");
    if (!fp) {
        std::cerr << "Could not open file for writing" << std::endl;
        EVP_PKEY_free(pkey);
        return;
    }
    
    int ret;
    if (!password.empty()) {
        ret = PEM_write_PrivateKey(fp, pkey, EVP_aes_256_cbc(), 
                                  (unsigned char*)password.c_str(), password.length(), NULL, NULL);
    } else {
        ret = PEM_write_PrivateKey(fp, pkey, NULL, NULL, 0, NULL, NULL);
    }
    
    fclose(fp);
    
    if (ret != 1) {
        print_openssl_errors();
        std::cerr << "Failed to save private key" << std::endl;
        EVP_PKEY_free(pkey);
        return;
    }
    
    std::cout << "New wallet generated and saved to wallet.pem" << std::endl;
    
    // Display the new wallet address
    std::string address = generate_address(pkey);
    if (!address.empty()) {
        std::cout << "Wallet address: " << address << std::endl;
    }
    
    // Clean up
    EVP_PKEY_free(pkey);
}

// Send FractalCash to another address (simplified)
void sendFunds(const std::string& to_address, double amount) {
    std::cout << "Sending " << amount << " FRC to " << to_address << std::endl;
    std::cout << "Transaction successful! (simulated)" << std::endl;
}

// Display help menu
void displayHelp() {
    std::cout << "FractalCash Wallet - Commands:" << std::endl;
    std::cout << "  balance             - Check your wallet balance" << std::endl;
    std::cout << "  generate [password] - Generate a new wallet" << std::endl;
    std::cout << "  send <address> <amount> - Send FRC to an address" << std::endl;
    std::cout << "  help                - Display this help message" << std::endl;
    std::cout << "  exit                - Exit the program" << std::endl;
}

int main() {
    // Initialize OpenSSL
    OpenSSL_add_all_algorithms();
    ERR_load_crypto_strings();
    
    std::cout << "Welcome to FractalCash Wallet" << std::endl;
    std::cout << "Type 'help' for a list of commands" << std::endl;
    
    std::string input;
    bool running = true;
    
    while (running) {
        std::cout << "\nFractalCash> ";
        std::getline(std::cin, input);
        
        std::istringstream iss(input);
        std::string command;
        iss >> command;
        
        if (command == "balance") {
            displayBalance();
        }
        else if (command == "generate") {
            std::string password;
            iss >> password;
            generateWallet(password);
        }
        else if (command == "send") {
            std::string address;
            double amount;
            iss >> address >> amount;
            
            if (address.empty() || amount <= 0) {
                std::cout << "Usage: send <address> <amount>" << std::endl;
            } else {
                sendFunds(address, amount);
            }
        }
        else if (command == "help") {
            displayHelp();
        }
        else if (command == "exit") {
            running = false;
        }
        else if (!command.empty()) {
            std::cout << "Unknown command. Type 'help' for a list of commands." << std::endl;
        }
    }
    
    // Clean up OpenSSL
    EVP_cleanup();
    CRYPTO_cleanup_all_ex_data();
    ERR_free_strings();
    
    return 0;
}
