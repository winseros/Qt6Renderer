#pragma once

#include <QDateTime>
#include <QCalendar>
#include <QCalendar>
#include <QDate>
#include <QTime>
#include <QTimeZone>
#include <QDebug>

void DemoQDateTime() {
    QDateTime d1;
    QDateTime d2{QDateTime::currentDateTime()};
    QDateTime d3{QDateTime::currentDateTimeUtc()};
    QDateTime d4{QDate{2022, 04, 26}, QTime{13, 07}};
    QDateTime d5{QDate{2022, 04, 27}, QTime{14, 05}, Qt::OffsetFromUTC, -1 * 3600};
    QDateTime d6{QDate{2022, 04, 27}, QTime{14, 05}, QTimeZone{2 * 3600}};
}