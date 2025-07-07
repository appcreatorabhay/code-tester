#include "LoginFilter.h"
#include "HttpRequest.h"
#include "FilterCallback.h"
#include "FilterChain.h"

TEST(LoginFilterTest, BasicFilterExecution) {
  // Create a mock HttpRequest object
  HttpRequestPtr req = makeRequest("GET", "example.com/login", "", 401);

  // Create a mock FilterCallback object
  FilterCallback mockCallback;

  // Create a mock FilterChain object
  FilterChain chain(mockCallback);

  // Create a LoginFilter object
  LoginFilter filter;

  // Set the filter to the chain
  filter.setChain(chain);

  // Set the callback function for the filter to execute
  filter.setCallback(mockCallback);

  // Set the request for the filter to execute
  filter.setRequest(req);

  // Perform the filter execution
  filter.doFilter();

  // Assert that the callback was called with the correct arguments
  ASSERT_EQ(mockCallback, chain);
}