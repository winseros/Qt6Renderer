#pragma once

#include <QString>

void DemoPointer() {
    QString str("Hello world");
    QString* pStr = &str;

    QString* pNull = nullptr;
    void* pVoid = pStr;
}