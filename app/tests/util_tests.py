from app.utils.csrf import get_csrf, check_csrf
from app.utils.other import convert_markdown_to_html, convert_prices_data


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

# RUN TESTS
test_converting_markdown_to_html()
test_converting_prices_data()