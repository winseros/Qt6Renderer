#pragma once

#include <QTimeZone>

void DemoQTimeZone() {
    QTimeZone t1;
    QTimeZone t2(3600);
    QTimeZone t3(-7200);
    QTimeZone t4(-7202);
}