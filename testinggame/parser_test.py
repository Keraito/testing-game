import pytest
import testinggame

def testParserToParseNameInEasyExample():
  assertProperty("method", easyExample)

def testParserToParseTheLocInEasyExample():
  assertProperty("loc", easyExample)

def testParserToParseTheCodeInEasyExample():
  assertProperty("code", easyExample)

def testParserToParseNameInOneNestedBlockExample():
  assertProperty("method", oneBlockNestedExample)

def testParserToParseTheLocInOneNestedBlockExample():
  assertProperty("loc", oneBlockNestedExample)

def testParserToParseTheCodeInOneNestedBlockExample():
  assertProperty("code", oneBlockNestedExample)

def testParserToParseNameInMultipleBlockNestedExample():
  assertProperty("method", multipleBlockNestedExample)

def testParserToParseTheLocInMultipleBlockNestedExample():
  assertProperty("loc", multipleBlockNestedExample)

def testParserToParseTheCodeInMultipleBlockNestedExample():
  assertProperty("code", multipleBlockNestedExample)

def testParserToParseNameInMultipleBlockTwoTimesNestedExample():
  assertProperty("method", multipleBlockTwoTimesNestedExample)

def testParserToParseTheLocInMultipleBlockTwoTimesNestedExample():
  assertProperty("loc", multipleBlockTwoTimesNestedExample)

def testParserToParseTheCodeInMultipleBlockTwoTimesNestedExample():
  assertProperty("code", multipleBlockTwoTimesNestedExample)


def assertProperty(property, expectation):
  assertAgainst = expectation[property]
  if property == "code":
    assertAgainst = [line[line.find(')')+1:] for line in expectation[property][1:]]
  assert testinggame._find_java_tests(expectation['code'])[0][property] == assertAgainst

easyExample = {
  'code': [
    ")    @Test",
    ")    public void testExample2() {",
    ")        Assert.assertEquals(0, 0);",
    ")",
    ")        Assert.assertEquals(0, 0);",
    ")",
    ")        Assert.assertEquals(0, 0);",
    ")    }"],
  'loc': 5,
  'method': 'testExample2'
  }

oneBlockNestedExample = {
  "code": [
    ")    @Test",
    ")    public void testOnCompletedThrows2() {",
    ")        TestSubscriber<Integer> ts = new TestSubscriber<Integer>() {",
    ")            @Override",
    ")            public void onComplete() {",
    ")                throw new RuntimeException(new TestException());",
    ")            }",
    ")        };",
    ")        SafeSubscriber<Integer> safe = new SafeSubscriber<Integer>(ts);",
    ")    }"],
  "method": "testOnCompletedThrows2",
  "loc": 7
}

multipleBlockNestedExample = {
  "code": [
    ")    @Test",
    ")    public void testOnCompletedThrows3() {",
    ")        TestSubscriber<Integer> ts = new TestSubscriber<Integer>() {",
    ")            @Override",
    ")            public void onComplete() {",
    ")                throw new RuntimeException(new TestException());",
    ")            }",
    ")        };",
    ")        SafeSubscriber<Integer> safe = new SafeSubscriber<Integer>(ts);",
    ")",
    ")        try {",
    ")            safe.onComplete();",
    ")        } catch (RuntimeException ex) {",
    ")            // expected",
    ")        }",
    ")    }"],
  "method": "testOnCompletedThrows3",
  "loc": 13
}

multipleBlockTwoTimesNestedExample = {
  "code": [
    ")    @Test",
    ")    public void testOnCompletedThrows3() {",
    ")        try {",
    ")            TestSubscriber<Integer> ts = new TestSubscriber<Integer>() {",
    ")              @Override",
    ")              public void onComplete() {",
    ")                  throw new RuntimeException(new TestException());",
    ")              }",
    ")            };",
    ")            SafeSubscriber<Integer> safe = new SafeSubscriber<Integer>(ts);",
    ")            safe.onComplete();",
    ")        } catch (RuntimeException ex) {",
    ")            // expected",
    ")        }",
    ")    }"],
  "method": "testOnCompletedThrows3",
  "loc": 12
}