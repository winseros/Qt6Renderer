#pragma once

#include <QUuid>
#include <QDebug>

void DemoQUuid() {
    QUuid u1;
    QUuid u2{QUuid::createUuid()};
    QUuid u3("00f8f7ac-6085-11ee-8c99-0242ac120002");
    //qInfo() << u2.toString(QUuid::WithoutBraces);
}