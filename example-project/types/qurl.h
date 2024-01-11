#pragma once

#include <QUrl>
#include <QDebug>

void DemoQUrl() {
    QUrl u1{"https://user:pass@site.com:443/path/p1?p2=v2&p3=v3#client=p4"};
    QUrl u2{"https://user@site.com"};
    QUrl u3{"https://:pass@site.com:0"};
    QUrl u4{"https://:pass@site.com:-1"};
    QUrl u5{"https://site.com"};
//    qInfo() << u1.toString();
//    qInfo() << u2.toString();
//    qInfo() << u3.toString();
//    qInfo() << u4.toString();
//    qInfo() << u5.toString();
}