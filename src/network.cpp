#include "network.h"
#include <iostream>
#include <chrono>

P2PNode::P2PNode() : acceptor(io_context) {}

void P2PNode::start_server(uint16_t port) {
    auto endpoint = boost::asio::ip::tcp::endpoint(boost::asio::ip::tcp::v4(), port);
    acceptor.open(endpoint.protocol());
    acceptor.bind(endpoint);
    acceptor.listen();
    std::cout << "Server listening on port " << port << "\n";
    io_context.run();
}

void P2PNode::connect_peer(const std::string& ip, uint16_t port) {
    boost::asio::ip::tcp::socket socket(io_context);
    socket.connect({boost::asio::ip::make_address(ip), port});
    std::cout << "Connected to peer: " << ip << ":" << port << "\n";
}

void startNetwork() {
    P2PNode node;
    std::thread server_thread([&](){ node.start_server(9333); });
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
    node.connect_peer("127.0.0.1", 9333);
    server_thread.join();
}
