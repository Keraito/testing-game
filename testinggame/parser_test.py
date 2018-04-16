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

def testParserToParseNameInTestInClassExample():
  assertProperty("method", testInClassExample)

def testParserToParseLocInTestInClassExample():
  assertProperty("loc", testInClassExample)

def testParserToParseCodeInTestInClassExample():
  expectedCode = {
    'code': [
      ")    @Test",
      ")    public void testInClassExample() {",
      ")        Assert.assertEquals(0, 0);",
      ")",
      ")        Assert.assertEquals(0, 0);",
      ")",
      ")        Assert.assertEquals(0, 0);",
      ")    }"]
  }
  property = 'code'
  parsedExpectedCode = [line[line.find(')')+1:] for line in expectedCode[property][1:]]
  assert testinggame._find_java_tests(testInClassExample['code'])[0][property] == parsedExpectedCode

def testParserToParseNameInSmallSetupExample():
  assertProperty("method", smallSetupExample)

def testParserToParseLocInSmallSetupExample():
  assertProperty("loc", smallSetupExample)

def testParserToParseCodeInSmallSetupExample():
  expectedCode = {
    "code": [
      ")    @Test",
      ")    public void testSetupExample() {",
      ")        Square[][] grid = new Square[6][4];",
      ")        for (int x = 0; x < grid.length; x++) {",
      ")            for (int y = 0; y < grid[x].length; y++) {",
      ")                grid[x][y] = new BasicSquare();",
      ")            }",
      ")        }",
      ")        board = new Board(grid);",
      ")        Assert.assertEquals(0, 0);",
      ")",
      ")        Assert.assertEquals(0, 0);",
      ")",
      ")        Assert.assertEquals(0, 0);",
      ")    }"]
  }
  property = 'code'
  parsedExpectedCode = [line[line.find(')')+1:] for line in expectedCode[property][1:]]
  assert testinggame._find_java_tests(smallSetupExample['code'])[0][property] == parsedExpectedCode

def testParserToParseNameInEasyExampleNonPublic():
  assertProperty("method", easyExampleNonPublic)

def testParserToParseTheLocInEasyExampleNonPublic():
  assertProperty("loc", easyExampleNonPublic)

def testParserToParseTheCodeInEasyExampleNonPublic():
  assertProperty("code", easyExampleNonPublic)

def testParserToParseNameInSmallNonPublicSetupExample():
  assertProperty("method", smallNonPublicSetupExample)

def testParserToParseLocInSmallNonPublicSetupExample():
  assertProperty("loc", smallNonPublicSetupExample)

def testParserToParseCodeInSmallNonPublicSetupExample():
  expectedCode = {
    "code": [
      ")    @Test",
      ")    void testSetupExample() {",
      ")        Square[][] grid = new Square[6][4];",
      ")        for (int x = 0; x < grid.length; x++) {",
      ")            for (int y = 0; y < grid[x].length; y++) {",
      ")                grid[x][y] = new BasicSquare();",
      ")            }",
      ")        }",
      ")        board = new Board(grid);",
      ")        Assert.assertEquals(0, 0);",
      ")",
      ")        Assert.assertEquals(0, 0);",
      ")",
      ")        Assert.assertEquals(0, 0);",
      ")    }"]
  }
  property = 'code'
  parsedExpectedCode = [line[line.find(')')+1:] for line in expectedCode[property][1:]]
  assert testinggame._find_java_tests(smallNonPublicSetupExample['code'])[0][property] == parsedExpectedCode

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

easyExampleNonPublic = {
  'code': [
    ")    @Test",
    ")    void testExample2() {",
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

testInClassExample = {
  'code': [
    ")  package com.spotify.thing;",
    ")",
    ")  public class ExampleTest {",
    ")",
    ")    @Test",
    ")    public void testInClassExample() {",
    ")        Assert.assertEquals(0, 0);",
    ")",
    ")        Assert.assertEquals(0, 0);",
    ")",
    ")        Assert.assertEquals(0, 0);",
    ")    }",
    ")",
    ")    public void setup() {",
    ")        Square[][] grid = new Square[6][4];",
    ")        for (int x = 0; x < grid.length; x++) {",
    ")            for (int y = 0; y < grid[x].length; y++) {",
    ")                grid[x][y] = new BasicSquare();",
    ")            }",
    ")        }",
    ")        board = new Board(grid);",
    ")    }",
    ")  }"],
  'loc': 5,
  'method': 'testInClassExample'
  }

smallSetupExample = {
  'code': [
    ")  package com.spotify.thing;",
    ")",
    ")  public class ExampleTest {",
    ")",
    ")    @BeforeEach",
    ")    public void setup() {",
    ")        Square[][] grid = new Square[6][4];",
    ")        for (int x = 0; x < grid.length; x++) {",
    ")            for (int y = 0; y < grid[x].length; y++) {",
    ")                grid[x][y] = new BasicSquare();",
    ")            }",
    ")        }",
    ")        board = new Board(grid);",
    ")    }",
    ")",
    ")    @Test",
    ")    public void testSetupExample() {",
    ")        Assert.assertEquals(0, 0);",
    ")",
    ")        Assert.assertEquals(0, 0);",
    ")",
    ")        Assert.assertEquals(0, 0);",
    ")    }",
    ")  }"],
  'loc': 12,
  'method': 'testSetupExample'
  }

smallNonPublicSetupExample = {
  'code': [
    ")  package com.spotify.thing;",
    ")",
    ")  public class ExampleTest {",
    ")",
    ")    @BeforeEach",
    ")    void setup() {",
    ")        Square[][] grid = new Square[6][4];",
    ")        for (int x = 0; x < grid.length; x++) {",
    ")            for (int y = 0; y < grid[x].length; y++) {",
    ")                grid[x][y] = new BasicSquare();",
    ")            }",
    ")        }",
    ")        board = new Board(grid);",
    ")    }",
    ")",
    ")    @Test",
    ")    void testSetupExample() {",
    ")        Assert.assertEquals(0, 0);",
    ")",
    ")        Assert.assertEquals(0, 0);",
    ")",
    ")        Assert.assertEquals(0, 0);",
    ")    }",
    ")  }"],
  'loc': 12,
  'method': 'testSetupExample'
  }
