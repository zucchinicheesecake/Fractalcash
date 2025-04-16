#pragma once
#include <boost/asio.hpp>
#include <thread>

class P2PNode {
    boost::asio::io_context io_context;
    boost::asio::ip::tcp::acceptor acceptor;
public:
    P2PNode();
    void start_server(uint16_t port);
    void connect_peer(const std::string& ip, uint16_t port);
};

void startNetwork();
