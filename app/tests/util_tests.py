from app.utils.other import convert_markdown_to_html, convert_prices_data, convert_tags_to_list, convert_tags_to_string


# TESTS
def test_converting_markdown_to_html():
    value = "### heading"
    result = "<h3>heading</h3>"

    my_result = convert_markdown_to_html(value)
    print(my_result)

    assert result in my_result

    print("test_converting_markdown_to_html() test passed successfully.")


def test_converting_prices_data():
    data = "23.0|23,00|Zgodnja cena{}33.0|33,00|Normalna cena{}"
    prices_list = convert_prices_data(data=data)

    assert prices_list[0].price_dot == 23.0

    print("test_converting_prices_data() test passed successfully.")


def test_converting_tags_to_list():
    data = "12 weeks,programming,Ljubljana"

    l = convert_tags_to_list(data)

    assert l == ["12 weeks", "programming", "Ljubljana"]

    print("test_converting_tags_to_list() test passed successfully.")


def test_converting_tags_to_string():
    data = ["12 weeks", "programming", "Ljubljana"]

    s = convert_tags_to_string(data)

    assert s == "12 weeks,programming,Ljubljana"

    print("test_converting_tags_to_string() test passed successfully.")

# RUN TESTS
test_converting_markdown_to_html()
test_converting_prices_data()
test_converting_tags_to_list()
test_converting_tags_to_string()