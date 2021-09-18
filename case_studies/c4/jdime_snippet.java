<<<<<<< LEFT
...
  @Test public void testNonNullNativeIgnoreingDocumentationParameterMatcher() {
    context.checking(new Expectations() {
      {
        exactly(1).of(mock).withBoolean(with.booleanIs(anything()));
...
  }
=======
>>>>>>> RIGHT

...
  @Test public void testNonNullNativeIgnoringDocumentationParameterMatcher() {
    context.checking(new Expectations() {
      {
        exactly(1).of(mock).withBoolean(with(any(Boolean.class)));
...
  }
