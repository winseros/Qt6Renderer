#pragma once

#include <QUuid>
#include <QDebug>

void DemoQUuid() {
    QUuid u{QUuid::createUuid()};
    //qInfo() << u.toString(QUuid::WithoutBraces);
}