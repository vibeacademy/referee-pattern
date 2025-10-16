Feature: Simple Calculator
  As a user
  I want to perform basic arithmetic operations
  So that I can calculate results quickly

  Scenario: Add two numbers
    Given I have a calculator
    When I add 5 and 3
    Then the result should be 8

  Scenario: Subtract two numbers
    Given I have a calculator
    When I subtract 3 from 10
    Then the result should be 7

  Scenario: Multiply two numbers
    Given I have a calculator
    When I multiply 4 and 6
    Then the result should be 24

  Scenario: Divide two numbers
    Given I have a calculator
    When I divide 20 by 4
    Then the result should be 5.0

  Scenario: Handle division by zero
    Given I have a calculator
    When I divide 10 by 0
    Then it should raise a division by zero error
