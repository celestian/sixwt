Feature: sixwt init

  Scenario: Missing configuration
    Given we have sixwt installed
    And sixwt is not properly configured
    When we run "sixwt wizard" non-interactively
    Then return code is "0"
    And we see "ERROR: Configuration file" on stdout
    And we see "doesn't exist" on stdout

  Scenario: Missing storage
    Given we have sixwt installed
    And sixwt is properly configured
    And storage directory is missing
    When we run "sixwt wizard" non-interactively
    Then return code is "0"
    And we see "You should run `sixwt init`" on stdout

  Scenario: Prepare storage
    Given we have sixwt installed
    And sixwt is properly configured
    And storage directory is missing
    When we run "sixwt init" non-interactively
    Then return code is "0"
    And storage directory exists

  Scenario: Prepare storage with examples
    Given we have sixwt installed
    And sixwt is properly configured
    And storage directory is missing
    When we run "sixwt init --with-examples" non-interactively
    Then return code is "0"
    And storage directory exists
    And catalog examples are created

  Scenario: Update DB without catalog
    Given we have sixwt installed
    And sixwt is properly configured
    And storage directory exists
    When we run "sixwt db update" non-interactively
    Then return code is "1"
    And we see "you can run `sixwt init --with-examples`" on stdout

  Scenario: Update DB
    Given we have sixwt installed
    And sixwt is properly configured
    And storage directory exists with catalog examples
    When we run "sixwt db update" non-interactively
    Then return code is "0"
    And db file exists

  Scenario: Wizard without storage
    Given we have sixwt installed
    And sixwt is properly configured
    And storage directory is missing
    When we run "sixwt wizard" non-interactively
    Then return code is "0"
    And we see "You should run `sixwt init`" on stdout

  Scenario: Wizard without DB
    Given we have sixwt installed
    And sixwt is properly configured
    And storage directory exists with catalog examples
    When we run "sixwt wizard" non-interactively
    Then return code is "0"
    And we see "ERROR: Database file" on stderr
    And we see "is missing" on stderr
    And we see "You should run `sixwt db update`" on stdout
