from getgauge.python import step

# software under test
def echo(input: str) -> str:
    return input


class EchoTests:
    @step("If input is <input>, then output should be <output>.")
    def assert_input_equals_output(self, input, output):
        assert echo(input) == output

    @step("If input is <Hello Syrocon!>, then output should not be <>.")
    def assert_input_not_equals_output(self, arg1, arg2):
        assert echo(arg1) != arg2

    @step("If input is input, then output should be output. <table>")
    def assert_input_equals_output_table(self, table):
        for input, output in table.rows:
            assert echo(input) == output

    @step("This is the setup section called before each scenario.")
    def setup(self):
        assert True

    @step("This is the teardown section only called once.")
    def teardown(self):
        assert True
