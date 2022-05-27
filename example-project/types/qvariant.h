#include <QVariant>
#include <QRect>
#include <QMatrix4x4>

void DemoQVariant() {
    QVariant v_bool(true);
    QVariant v_int(10);
    QVariant v_uint(static_cast<quint32>(10));
    QVariant v_longlong(static_cast<qint64>(10));
    QVariant v_ulonglong(static_cast<quint64>(10));
    QVariant v_double(static_cast<double>(10.1));

    QSharedPointer<QObject> ptr(new QObject);
    QVariant v_void = QVariant::fromValue(static_cast<void *>(ptr.data()));
    QVariant v_long = QVariant::fromValue(static_cast<long>(10));
    QVariant v_short = QVariant::fromValue(static_cast<qint16>(10));
    QVariant v_char = QVariant::fromValue(static_cast<char>(10));
    QVariant v_ulong = QVariant::fromValue(static_cast<unsigned long>(10));
    QVariant v_ushort = QVariant::fromValue(static_cast<quint16>(10));
    QVariant v_uchar = QVariant::fromValue(static_cast<quint8>(10));
    QVariant v_float(static_cast<float >(10.1));
    QVariant v_schar = QVariant::fromValue(static_cast<qint8>(10));

    QRect r{1, 2, 3, 4};
    QVariant v_rect(r);//is_shared = false

    QMatrix4x4 m{
            1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8,
            9.9, 10.10, 11.11, 12.12, 13.13, 14.14, 15.15, 16.16
    };
    QVariant v_shared(m);//is_shared = true
}