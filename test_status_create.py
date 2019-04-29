def test_create_status(app, logged_user):
    input_text = 'Hello, world!!'
    # Find statuses on page before new status creation
    old_status_list = app.status_text_elements()
    # Create new status
    app.create_new_text_status(input_text)
    # Wait until new status appears
    app.wait_new_status_appear(old_status_list)
    # Verify text of new status
    new_status_element = app.status_text_elements()[0]
    assert new_status_element.text == input_text
    assert app.user_of_new_status_elements()[0].text == logged_user.real_name
