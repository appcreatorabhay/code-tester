#include <gtest/gtest.h>
#include "LoginFilter.h"

TEST(LoginFilterTest, EmptyAuthorizationHeader) {
    LoginFilter filter;
    HttpRequestPtr req = drogon::makeHttpRequest("GET", "some_url", nullptr);
    filter.doFilter(req, [](HttpResponsePtr res) {
        EXPECT_EQ(k400BadRequest, res->getStatusCode());
        EXPECT_EQ("missing Authorization header", res->getHeader("error"));
    }, nullptr);
}

TEST(LoginFilterTest, TokenMissAuthorizationHeader) {
    LoginFilter filter;
    HttpRequestPtr req = drogon::makeHttpRequest("GET", "some_url", nullptr);
    req->setHeader("Authorization", "Bearer missing_token");
    filter.doFilter(req, [](HttpResponsePtr res) {
        EXPECT_EQ(k400BadRequest, res->getStatusCode());
        EXPECT_EQ("missing Authorization header", res->getHeader("error"));
    }, nullptr);
}

TEST(LoginFilterTest, TokenMalformed) {
    LoginFilter filter;
    HttpRequestPtr req = drogon::makeHttpRequest("GET", "some_url", nullptr);
    req->setHeader("Authorization", "Bearer token|invalid_token");
    filter.doFilter(req, [](HttpResponsePtr res) {
        EXPECT_EQ(k400BadRequest, res->getStatusCode());
        EXPECT_EQ("invalid token", res->getHeader("error"));
    }, nullptr);
}

TEST(LoginFilterTest, TokenValid) {
    LoginFilter filter;
    HttpRequestPtr req = drogon::makeHttpRequest("GET", "some_url", nullptr);
    req->setHeader("Authorization", "Bearer eyJ0aW…");
    filter.doFilter(req, [](HttpResponsePtr res) {
        EXPECT_EQ(200, res->getStatusCode());
    }, nullptr);
}

TEST(LoginFilterTest, TokenVerificationException) {
    LoginFilter filter;
    try {
        HttpRequestPtr req = drogon::makeHttpRequest("GET", "some_url", nullptr);
        req->setHeader("Authorization", "Bearer token");
        jwt::verifyToken(req->getHeader("Authorization"), "my_secret_key");
    } catch (jwt::token_verification_exception &e) {
        EXPECT_EQ(k400BadRequest, res->getStatusCode());
        EXPECT_EQ("invalid token", res->getHeader("error"));
    }
}