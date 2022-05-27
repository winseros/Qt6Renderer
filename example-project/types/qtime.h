#pragma once

#include <QTime>

void DemoQTime() {
    QTime t1;
    t1.setHMS(10, 2, 1, 555);
    QTime t2{0, 0, 0, 0};
    QTime t3{23, 59, 59, 999};
}