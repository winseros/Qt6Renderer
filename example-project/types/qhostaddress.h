#pragma once

#include <QHostAddress>

void DemoQHostAddress() {
    QHostAddress a1{QHostAddress::SpecialAddress::Null};
    QHostAddress a2{QHostAddress::SpecialAddress::Broadcast};
    QHostAddress a3{QHostAddress::SpecialAddress::LocalHost};
    QHostAddress a4{QHostAddress::SpecialAddress::LocalHostIPv6};
    QHostAddress a5{"10.20.5.3"};
    QHostAddress a6{"2345:0425:2CA1:0000:0000:0567:5673:23b5"};
}