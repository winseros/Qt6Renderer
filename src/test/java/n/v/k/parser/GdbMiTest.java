package n.v.k.parser;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

public class GdbMiTest {
    @Test
    public void Test_fromStringMultiple_Reads_Mi_Output() {
        var output = "result={token=\"17\",data=[{name=\"[statics]\",iname=\"local.[statics]\",numchild=\"1\",value=\"\",},{iname=\"local.hash\",name=\"hash\",numchild=\"3\",children=[{children=[{name=\"key\",address=\"0x21f5d8f82d0\",numchild=\"0\",type=\"int\",value=\"5\",},{name=\"value\",address=\"0x21f5d8f82d4\",numchild=\"0\",type=\"int\",value=\"6\",},],keyprefix=\"[0] \",key=\"5\",value=\"6\",},{children=[{name=\"key\",address=\"0x21f5d8f82c0\",numchild=\"0\",type=\"int\",value=\"1\",},{name=\"value\",address=\"0x21f5d8f82c4\",numchild=\"0\",type=\"int\",value=\"2\",},],keyprefix=\"[1] \",key=\"1\",value=\"2\",},{children=[{name=\"key\",address=\"0x21f5d8f82c8\",numchild=\"0\",type=\"int\",value=\"3\",},{name=\"value\",address=\"0x21f5d8f82cc\",numchild=\"0\",type=\"int\",value=\"4\",},],keyprefix=\"[2] \",key=\"3\",value=\"4\",},],address=\"0xc3032ff598\",type=\"QHash<int,int>\",valueencoded=\"itemcount\",value=\"3\",},{iname=\"local.tf1\",name=\"tf1\",numchild=\"1\",address=\"0xc3032ff568\",type=\"QFile\",valueencoded=\"utf16\",value=\"740065006D00700031002E00740078007400\",},{iname=\"local.str\",name=\"str\",numchild=\"1\",address=\"0xc3032ff538\",type=\"QString\",valueencoded=\"utf16\",value=\"480065006C006C006F002C00200057006F0072006C0064002100\",},{iname=\"local.rt\",name=\"rt\",numchild=\"1\",address=\"0xc3032ff5b8\",type=\"QRect\",value=\"3x3+0+1\",},],partial=\"1\"}";
        var mi = new GdbMi();
        mi.fromStringMultiple(output);

        Assertions.assertTrue(mi.isValid());
        Assertions.assertEquals(GdbMiType.Tuple, mi.getType());

        var data = mi.getChild("result").getChild("data");
        Assertions.assertNotNull(data);
        Assertions.assertEquals(GdbMiType.List, data.getType());
        Assertions.assertEquals(5, data.size());

        var statics = data.get(0);
        Assertions.assertEquals(GdbMiType.Tuple, statics.getType());
        Assertions.assertEquals(4, statics.size());
        Assertions.assertEquals("[statics]", statics.getChild("name").getData());
        Assertions.assertEquals("local.[statics]", statics.getChild("iname").getData());
        Assertions.assertEquals("1", statics.getChild("numchild").getData());
        Assertions.assertEquals("", statics.getChild("value").getData());

        var hash = data.get(1);
        Assertions.assertEquals(GdbMiType.Tuple, hash.getType());
        var hashChildren = hash.getChild("children");
        Assertions.assertEquals(3, hashChildren.size());
        Assertions.assertEquals("5", hashChildren.get(0).getChild("key").getData());
        Assertions.assertEquals("6", hashChildren.get(0).getChild("value").getData());

        var str = data.get(3);
        Assertions.assertEquals(GdbMiType.Tuple, str.getType());
        Assertions.assertEquals(7, str.size());
        Assertions.assertEquals("str", str.getChild("name").getData());
        Assertions.assertEquals("local.str", str.getChild("iname").getData());
        Assertions.assertEquals("1", str.getChild("numchild").getData());
        Assertions.assertEquals("0xc3032ff538", str.getChild("address").getData());
        Assertions.assertEquals("QString", str.getChild("type").getData());
        Assertions.assertEquals("utf16", str.getChild("valueencoded").getData());
        Assertions.assertEquals("480065006C006C006F002C00200057006F0072006C0064002100", str.getChild("value").getData());
    }
}
