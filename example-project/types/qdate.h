#pragma once

#include <QDate>
#include <QCalendar>
#include <QDebug>

void DemoQDate() {
    QDate d1;
//    qInfo() << d1.isValid();
//    qInfo() << d1.isNull();

    QDate d2 = QDate::currentDate();
//    qInfo() << d2.isValid();
//    qInfo() << d2.isNull();
//    qInfo() << d2.year();
//    qInfo() << d2.month();
//    qInfo() << d2.day();

    QCalendar calendar;
    QDate d3 = calendar.dateFromParts(2020, 04, 25);
//    qInfo() << d3.isValid();
//    qInfo() << d3.isNull();
//    qInfo() << d3.year();
//    qInfo() << d3.month();
//    qInfo() << d3.day();
}