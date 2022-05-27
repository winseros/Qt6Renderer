#pragma once

#include <QBitArray>

void DemoQBitArray() {
    QBitArray a1;
    QBitArray a2(4, true);
    QBitArray a3;
    a3.resize(10);
    a3.setBit(0);
    a3.setBit(1);
    a3.setBit(3);
    a3.setBit(9);
}