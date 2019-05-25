Feature: Login feature
  Description: Registered user can sign in to Oxwall site at all pages.
  User information is on ....
  After login user should see Dashboard page.
  ...

  Scenario Outline: Login regular user
    Given I as a registered user with <username>, <password> and <real_name>
    When I sign in to Oxwall using Sign In button
    Then I see Dashboard page
    Then User menu has my <real_name>

    Examples:
    | username            | password       | real_name       |
    | !@#%^&<a *%^*{}))_+ | secret         | dsdfsd          |
    | !@#%^&<a *%^*{}))_+ | secret         | dsdfsd          |
    | New 1234098765!     | secret         | dsdfsd          |
    | Привіт!             | secret         | dsdfsd          |
