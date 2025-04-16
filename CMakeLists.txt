cmake_minimum_required(VERSION 3.10)
project(FractalCash)

set(CMAKE_CXX_STANDARD 14)

# Include directories
include_directories(include)

# Define the executable and its source files
add_executable(FractalCash
    src/main.cpp
    src/block.cpp
    src/transaction.cpp
    src/merkle_tree.cpp
    src/fractalhash.cpp
    src/network.cpp
    src/transaction_handler.cpp  # Added
    src/transaction_subset.cpp   # Added (Fixes the linker error)
)

# Link necessary libraries
# Make sure these libraries are installed on your system
# (e.g., libssl-dev, libsodium-dev, libboost-system-dev, libboost-thread-dev, libboost-chrono-dev on Debian/Ubuntu)
target_link_libraries(FractalCash PRIVATE
    ssl
    crypto
    sodium
    boost_system
    boost_thread
    boost_chrono
)

