from app.utils.other import convert_string_to_list, convert_list_to_string, convert_markdown_to_html


# TESTS
def test_converting_markdown_to_html():
    value = "### heading"
    result = "<h3>heading</h3>"

    my_result = convert_markdown_to_html(value)
    print(my_result)

    assert result in my_result

    print("test_converting_markdown_to_html() test passed successfully.")


# RUN TESTS
test_converting_markdown_to_html()