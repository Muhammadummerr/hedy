import hedy
import textwrap

from hedy_sourcemap import SourceRange
from tests.Tester import HedyTester, SkippedMapping
from parameterized import parameterized


class TestsLevel5(HedyTester):
    level = 5
    '''
    Tests should be ordered as follows:
     * commands in the order of hedy.py e.g. for level 1: ['print', 'ask', 'echo', 'turn', 'forward']
     * combined tests
     * markup tests
     * negative tests

    Naming conventions are like this:
     * single keyword positive tests are just keyword or keyword_special_case
     * multi keyword positive tests are keyword1_keywords_2
     * negative tests should be situation_gives_exception
    '''

    #
    # if tests
    #
    @parameterized.expand(HedyTester.commands_level_4)
    def test_if_equality_linebreak_print(self,  hedy, python):
        # line breaks after if-condition are allowed
        code = textwrap.dedent(f"""\
        naam is Hedy
        if naam is Hedy
        {hedy}""")

        expected = textwrap.dedent(f"""\
        naam = 'Hedy'
        if naam == 'Hedy':
          {python}""")

        self.single_level_tester(code=code, expected=expected)

    def test_if_equality_trailing_space_linebreak_print(self):
        code = textwrap.dedent("""\
        naam is James
        if naam is trailing_space
        print 'shaken'""")

        expected = textwrap.dedent("""\
        naam = 'James'
        if naam == 'trailing_space':
          print(f'shaken')""")

        self.single_level_tester(code=code, expected=expected)

    def test_if_equality_unquoted_rhs_with_space_linebreak_print(self):
        code = textwrap.dedent("""\
        naam is James
        if naam is James Bond
        print 'shaken'""")

        expected = textwrap.dedent("""\
        naam = 'James'
        if naam == 'James Bond':
          print(f'shaken')""")

        self.multi_level_tester(code=code, expected=expected, max_level=7)

    def test_if_equality_unquoted_rhs_with_space_and_trailing_space_linebreak_print(self):
        code = textwrap.dedent("""\
        naam is James
        if naam is trailing space
        print 'shaken'""")

        expected = textwrap.dedent("""\
        naam = 'James'
        if naam == 'trailing space':
          print(f'shaken')""")

        self.multi_level_tester(code=code, expected=expected, max_level=7)

    def test_if_2_vars_equality_print(self):
        code = textwrap.dedent("""\
        jouwkeuze is schaar
        computerkeuze is schaar
        if computerkeuze is jouwkeuze print 'gelijkspel!'""")

        expected = textwrap.dedent("""\
        jouwkeuze = 'schaar'
        computerkeuze = 'schaar'
        if computerkeuze == jouwkeuze:
          print(f'gelijkspel!')""")

        self.single_level_tester(code=code, expected=expected, output='gelijkspel!')

    def test_if_not_in_list_print(self):
        code = textwrap.dedent("""\
        items is red, green
        selected is red
        if selected not in items print 'not found!'
        else print 'found'""")

        expected = textwrap.dedent("""\
        items = ['red', 'green']
        selected = 'red'
        if selected not in items:
          print(f'not found!')
        else:
          print(f'found')""")

        self.multi_level_tester(
            max_level=7,
            code=code,
            expected=expected,
            output='found'
        )

    def test_if_not_in_list_in_print(self):
        code = textwrap.dedent("""\
        items is red, green
        selected is purple
        if selected not in items print 'not found!'
        else print 'found'""")

        expected = textwrap.dedent("""\
        items = ['red', 'green']
        selected = 'purple'
        if selected not in items:
          print(f'not found!')
        else:
          print(f'found')""")

        self.multi_level_tester(
            max_level=7,
            code=code,
            expected=expected,
            output='not found!'
        )

    def test_if_in_list_print(self):
        code = textwrap.dedent("""\
        items is red, green
        selected is red
        if selected in items print 'found!'""")

        expected = textwrap.dedent("""\
        items = ['red', 'green']
        selected = 'red'
        if selected in items:
          print(f'found!')""")

        self.multi_level_tester(
            max_level=7,
            code=code,
            expected=expected,
            output='found!',
            expected_commands=['is', 'is', 'if', 'in', 'print']
        )

    def test_if_in_undefined_list(self):
        code = textwrap.dedent("""\
        selected is red
        if selected in items print 'found!'""")

        self.multi_level_tester(code=code, exception=hedy.exceptions.UndefinedVarException, max_level=7)

    def test_if_equality_unquoted_rhs_with_space_print_gives_error(self):
        code = textwrap.dedent("""\
        naam is James
        if naam is James Bond print 'shaken'""")

        expected = textwrap.dedent("""\
        naam = 'James'
        pass""")

        skipped_mappings = [
            SkippedMapping(SourceRange(2, 1, 2, 37), hedy.exceptions.UnquotedEqualityCheckException),
        ]

        self.multi_level_tester(
            code=code,
            expected=expected,
            skipped_mappings=skipped_mappings,
            max_level=7
        )

    def test_if_equality_unquoted_rhs_with_space_and_following_command_print_gives_error(self):
        code = textwrap.dedent("""\
        naam is James
        if naam is James Bond print 'shaken' 
        print naam""")

        expected = textwrap.dedent("""\
        naam = 'James'
        pass
        print(f'{naam}')""")

        skipped_mappings = [
            SkippedMapping(SourceRange(2, 1, 2, 59), hedy.exceptions.UnquotedEqualityCheckException),
        ]

        self.multi_level_tester(
            code=code,
            expected=expected,
            skipped_mappings=skipped_mappings,
            max_level=7
        )

    def test_if_equality_unquoted_rhs_with_space_assign_gives_error(self):
        code = textwrap.dedent("""\
        naam is James
        if naam is James Bond naam is 'Pietjansma'""")

        expected = textwrap.dedent("""\
        naam = 'James'
        pass""")

        skipped_mappings = [
            SkippedMapping(SourceRange(2, 1, 2, 43), hedy.exceptions.UnquotedEqualityCheckException),
        ]

        self.multi_level_tester(
            code=code,
            expected=expected,
            skipped_mappings=skipped_mappings,
            max_level=7
        )

    @parameterized.expand(HedyTester.quotes)
    def test_if_equality_quoted_rhs_with_space(self, q):
        code = textwrap.dedent(f"""\
        naam is James
        if naam is {q}James Bond{q} print {q}shaken{q}""")

        expected = textwrap.dedent(f"""\
        naam = 'James'
        if naam == 'James Bond':
          print(f'shaken')""")

        self.single_level_tester(
            code=code,
            expected_commands=['is', 'if', 'print'],
            expected=expected)

    @parameterized.expand(HedyTester.quotes)
    def test_if_equality_quoted_rhs_with_spaces(self, q):
        code = textwrap.dedent(f"""\
        naam is James
        if naam is {q}Bond James Bond{q} print 'shaken'""")

        expected = textwrap.dedent(f"""\
        naam = 'James'
        if naam == 'Bond James Bond':
          print(f'shaken')""")

        self.single_level_tester(code=code, expected=expected)

    def test_ask_if(self):
        code = textwrap.dedent(f"""\
        name is ask 'what is your name?'
        if name is Hedy print 'nice' else print 'boo!'""")

        expected = textwrap.dedent(f"""\
        name = input(f'what is your name?')
        if name == 'Hedy':
          print(f'nice')
        else:
          print(f'boo!')""")

        self.single_level_tester(
            code=code,
            expected_commands=['ask', 'if', 'else', 'print', 'print'],
            expected=expected)

    def test_if_equality_single_quoted_rhs_with_inner_double_quote(self):
        code = textwrap.dedent(f"""\
        answer is no
        if answer is 'He said "no"' print 'no'""")

        expected = textwrap.dedent(f"""\
        answer = 'no'
        if answer == 'He said "no"':
          print(f'no')""")

        self.single_level_tester(
            code=code,
            expected_commands=['is', 'if', 'print'],
            expected=expected)

    def test_if_equality_double_quoted_rhs_with_inner_single_quote(self):
        code = textwrap.dedent(f"""\
        answer is no
        if answer is "He said 'no'" print 'no'""")

        expected = textwrap.dedent(f"""\
        answer = 'no'
        if answer == 'He said \\'no\\'':
          print(f'no')""")

        self.single_level_tester(code=code, expected=expected)

    def test_equality_promotes_int_to_string(self):
        code = textwrap.dedent("""\
        a is test
        b is 15
        if a is b c is 1""")
        expected = textwrap.dedent("""\
        a = 'test'
        b = '15'
        if a == b:
          c = '1'""")

        self.single_level_tester(code=code, expected=expected)

    def test_quoted_ask(self):
        code = textwrap.dedent("""\
        szogek is ask 'Hello'""")

        expected = "szogek = input(f'Hello')"

        self.multi_level_tester(code=code,
                                expected=expected,
                                max_level=11)

    def test_equality_with_lists_gives_error(self):
        code = textwrap.dedent("""\
        n is 1, 2
        m is 1, 2
        if n is m print 'success!'""")

        self.multi_level_tester(
            max_level=7,
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 3,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    def test_if_in_list_with_string_var_gives_type_error(self):
        code = textwrap.dedent("""\
        items is red
        if red in items print 'found!'""")
        self.multi_level_tester(
            max_level=7,
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    def test_if_in_list_with_input_gives_type_error(self):
        code = textwrap.dedent("""\
        items is ask 'What are the items?'
        if red in items print 'found!'""")
        self.multi_level_tester(
            max_level=7,
            code=code,
            extra_check_function=lambda c: c.exception.arguments['line_number'] == 2,
            exception=hedy.exceptions.InvalidArgumentTypeException
        )

    #
    # if else tests
    #
    def test_if_equality_print_else_print(self):
        code = textwrap.dedent("""\
        naam is Hedy
        if naam is Hedy print 'leuk' else print 'minder leuk'""")

        expected = textwrap.dedent("""\
        naam = 'Hedy'
        if naam == 'Hedy':
          print(f'leuk')
        else:
          print(f'minder leuk')""")

        self.single_level_tester(code=code, expected=expected)

    def test_if_ask_equality_print_else_print(self):
        code = textwrap.dedent("""\
        kleur is ask 'Wat is je lievelingskleur?'
        if kleur is groen print 'mooi!' else print 'niet zo mooi'""")

        expected = textwrap.dedent("""\
        kleur = input(f'Wat is je lievelingskleur?')
        if kleur == 'groen':
          print(f'mooi!')
        else:
          print(f'niet zo mooi')""")

        self.single_level_tester(code=code, expected=expected)

    def test_if_else_followed_by_print(self):
        code = textwrap.dedent("""\
        kleur is geel
        if kleur is groen antwoord is ok else antwoord is stom
        print antwoord""")

        expected = textwrap.dedent("""\
        kleur = 'geel'
        if kleur == 'groen':
          antwoord = 'ok'
        else:
          antwoord = 'stom'
        print(f'{antwoord}')""")

        self.single_level_tester(code=code, expected=expected)

    def test_if_equality_trailing_space_linebreak_print_else(self):
        # this code has a space at the end of line 2
        code = textwrap.dedent("""\
        naam is James
        if naam is trailing space
        print 'shaken' else print 'biertje!'""")

        expected = textwrap.dedent("""\
        naam = 'James'
        if naam == 'trailing space':
          print(f'shaken')
        else:
          print(f'biertje!')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    def test_if_equality_print_linebreak_else_print(self):
        # line break before else is allowed
        code = textwrap.dedent("""\
        naam is Hedy
        if naam is Hedy print 'leuk'
        else print 'minder leuk'""")

        expected = textwrap.dedent("""\
        naam = 'Hedy'
        if naam == 'Hedy':
          print(f'leuk')
        else:
          print(f'minder leuk')""")

        self.single_level_tester(code=code, expected=expected)

    def test_if_equality_print_linebreaks_else_print(self):
        # line break before else is allowed
        code = textwrap.dedent("""\
        naam is Hedy
        if naam is Hedy print 'leuk'\n\n       
        else print 'minder leuk'""")

        expected = textwrap.dedent("""\
        naam = 'Hedy'
        if naam == 'Hedy':
          print(f'leuk')
        else:
          print(f'minder leuk')""")

        self.single_level_tester(code=code, expected=expected)

    def test_if_equality_linebreak_print_else_print(self):
        # line break after if-condition is allowed
        code = textwrap.dedent("""\
        naam is Hedy
        if naam is Hedy
        print 'leuk' else print 'minder leuk'""")

        expected = textwrap.dedent("""\
        naam = 'Hedy'
        if naam == 'Hedy':
          print(f'leuk')
        else:
          print(f'minder leuk')""")

        self.single_level_tester(code=code, expected=expected)

    def test_if_equality_unquoted_with_space_linebreak_print_else_print(self):
        code = textwrap.dedent("""\
        naam is James
        if naam is James Bond
        print 'shaken' else print 'biertje!'""")

        expected = textwrap.dedent("""\
        naam = 'James'
        if naam == 'James Bond':
          print(f'shaken')
        else:
          print(f'biertje!')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    def test_two_ifs_assign_no_following(self):
        code = textwrap.dedent("""\
        if order is fries price is 5
        drink is water""")

        expected = textwrap.dedent("""\
        if 'order' == 'fries':
          price = '5'
        else:
          x__x__x__x = '5'
        drink = 'water'""")

        self.single_level_tester(code=code, expected=expected, translate=False)

    def test_two_ifs_assign_following(self):
        code = textwrap.dedent("""\
        if order is fries price is 5
        drink is water
        print drink""")

        expected = textwrap.dedent("""\
        if 'order' == 'fries':
          price = '5'
        else:
          x__x__x__x = '5'
        drink = 'water'
        print(f'{drink}')""")

        self.single_level_tester(code=code, expected=expected, translate=False)

    def test_if_equality_print_else_linebreak_print(self):
        # line break after else is allowed
        code = textwrap.dedent("""\
        naam is Hedy
        if naam is Hedy print 'leuk' else
        print 'minder leuk'""")

        expected = textwrap.dedent("""\
        naam = 'Hedy'
        if naam == 'Hedy':
          print(f'leuk')
        else:
          print(f'minder leuk')""")

        self.single_level_tester(code=code, expected=expected)

    def test_if_with_negative_number(self):
        code = textwrap.dedent("""\
      antwoord is -10
      if antwoord is -10 print 'Nice' else print 'Oh no'""")

        expected = textwrap.dedent("""\
      antwoord = '-10'
      if antwoord == '-10':
        print(f'Nice')
      else:
        print(f'Oh no')""")

        self.single_level_tester(code=code, expected=expected, output='Nice')

    def test_if_equality_linebreak_print_linebreak_else_print(self):
        # line breaks after if-condition and before else are allowed
        code = textwrap.dedent("""\
        naam is Hedy
        if naam is Hedy
        print 'leuk'
        else print 'minder leuk'""")

        expected = textwrap.dedent("""\
        naam = 'Hedy'
        if naam == 'Hedy':
          print(f'leuk')
        else:
          print(f'minder leuk')""")

        self.single_level_tester(code=code, expected=expected)

    def test_if_equality_linebreak_print_linebreak_else_linebreak_print(self):
        # line breaks after if-condition, before else and after else are allowed
        code = textwrap.dedent("""\
        naam is Hedy
        if naam is Hedy
        print 'leuk'
        else
        print 'minder leuk'""")

        expected = textwrap.dedent("""\
        naam = 'Hedy'
        if naam == 'Hedy':
          print(f'leuk')
        else:
          print(f'minder leuk')""")

        self.single_level_tester(code=code, expected=expected)

    def test_if_equality_linebreak_print_else_linebreak_print(self):
        # line breaks after if-condition and after else are allowed
        code = textwrap.dedent("""\
        naam is Hedy
        if naam is Hedy
        print 'leuk' else
        print 'minder leuk'""")

        expected = textwrap.dedent("""\
        naam = 'Hedy'
        if naam == 'Hedy':
          print(f'leuk')
        else:
          print(f'minder leuk')""")

        self.single_level_tester(code=code, expected=expected)

    def test_if_list_assignment_else_print(self):
        code = textwrap.dedent("""\
        people is mom, dad, Emma, Sophie
        dishwasher is people at random
        if dishwasher is Sophie
        print 'too bad I have to do the dishes'
        else
        print 'luckily no dishes because' dishwasher 'is already washing up'""")

        expected = HedyTester.dedent("people = ['mom', 'dad', 'Emma', 'Sophie']",
                                     HedyTester.list_access_transpiled('random.choice(people)'),
                                     "dishwasher = random.choice(people)",
                                     "if dishwasher == 'Sophie':",
                                     ("print(f'too bad I have to do the dishes')", '  '),
                                     "else:",
                                     ("print(f'luckily no dishes because{dishwasher}is already washing up')", '  '))

        self.single_level_tester(code=code, expected=expected)

    @parameterized.expand(HedyTester.quotes)
    def test_if_equality_quoted_rhs_with_space_else(self, q):
        code = textwrap.dedent(f"""\
        naam is James
        if naam is {q}James Bond{q} print {q}shaken{q} else print {q}biertje!{q}""")

        expected = textwrap.dedent(f"""\
        naam = 'James'
        if naam == 'James Bond':
          print(f'shaken')
        else:
          print(f'biertje!')""")

        self.single_level_tester(code=code, expected=expected)

    def test_if_equality_text_with_spaces_and_single_quotes_linebreak_print_else_print(self):
        code = textwrap.dedent("""\
        naam is James
        if naam is James 'Bond'
        print 'shaken' else print 'biertje!'""")

        expected = textwrap.dedent("""\
        naam = 'James'
        if naam == 'James \\'Bond\\'':
          print(f'shaken')
        else:
          print(f'biertje!')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    def test_if_equality_text_with_spaces_and_double_quotes_linebreak_print_else_print(self):
        code = textwrap.dedent("""\
        naam is James
        if naam is James "Bond"
        print 'shaken' else print 'biertje!'""")

        expected = textwrap.dedent("""\
        naam = 'James'
        if naam == 'James "Bond"':
          print(f'shaken')
        else:
          print(f'biertje!')""")

        self.multi_level_tester(max_level=7, code=code, expected=expected)

    def test_if_equality_print_else_print_bengali(self):
        code = textwrap.dedent("""\
        নাম is ask 'আপনার নাম কি?'
        if নাম is হেডি print 'ভালো!' else print 'মন্দ'""")

        expected = textwrap.dedent("""\
        নাম = input(f'আপনার নাম কি?')
        if নাম == 'হেডি':
          print(f'ভালো!')
        else:
          print(f'মন্দ')""")

        self.single_level_tester(code=code, expected=expected)

    #
    # combined tests
    #

    def test_consecutive_if_statements(self):
        code = textwrap.dedent("""\
        names is Hedy, Lamar
        name is ask 'What is a name you like?'
        if name is Hedy print 'nice!'
        if name in names print 'nice!'""")

        expected = textwrap.dedent("""\
        names = ['Hedy', 'Lamar']
        name = input(f'What is a name you like?')
        if name == 'Hedy':
          print(f'nice!')
        else:
          x__x__x__x = '5'
        if name in names:
          print(f'nice!')""")

        self.single_level_tester(code=code, expected=expected)

    def test_onno_3372(self):
        code = textwrap.dedent("""\
        antw is ask 'wat kies jij'
        if antw is schaar print 'gelijk spel!'
        print 'test'""")

        expected = textwrap.dedent("""\
        antw = input(f'wat kies jij')
        if antw == 'schaar':
          print(f'gelijk spel!')
        else:
          x__x__x__x = '5'
        print(f'test')""")

        self.single_level_tester(code=code,
                                 expected=expected)

    def test_restaurant_example(self):
        code = textwrap.dedent("""\
        print 'Welkom bij McHedy'
        eten is ask 'Wat wilt u eten?'
        if eten is friet saus is ask 'Welke saus wilt u bij de friet?'
        if eten is pizza topping is ask 'Welke topping wilt u op de pizza?'
        print eten""")

        expected = textwrap.dedent("""\
        print(f'Welkom bij McHedy')
        eten = input(f'Wat wilt u eten?')
        if eten == 'friet':
          saus = input(f'Welke saus wilt u bij de friet?')
        else:
          x__x__x__x = '5'
        if eten == 'pizza':
          topping = input(f'Welke topping wilt u op de pizza?')
        else:
          x__x__x__x = '5'
        print(f'{eten}')""")

        self.single_level_tester(code=code,
                                 expected=expected, translate=False)

    def test_onno_3372_else(self):
        code = textwrap.dedent("""\
        antw is ask 'wat kies jij'
        if antw is schaar print 'gelijk spel!' else print ''
        print 'test'""")

        expected = textwrap.dedent("""\
        antw = input(f'wat kies jij')
        if antw == 'schaar':
          print(f'gelijk spel!')
        else:
          print(f'')
        print(f'test')""")

        self.single_level_tester(code=code,
                                 expected=expected)

    def test_consecutive_if_and_if_else_statements(self):
        code = textwrap.dedent("""\
        naam is ask 'hoe heet jij?'
        if naam is Hedy print 'leuk'
        if naam is Python print 'ook leuk'
        else print 'minder leuk!'""")

        expected = textwrap.dedent("""\
        naam = input(f'hoe heet jij?')
        if naam == 'Hedy':
          print(f'leuk')
        else:
          x__x__x__x = '5'
        if naam == 'Python':
          print(f'ook leuk')
        else:
          print(f'minder leuk!')""")

        self.single_level_tester(code=code,
                                 expected=expected)

    def test_consecutive_if_else_statements(self):
        code = textwrap.dedent("""\
        names is Hedy, Lamar
        name is ask 'What is a name you like?'
        if name is Hedy print 'nice!' else print 'meh'
        if name in names print 'nice!' else print 'meh'""")

        expected = textwrap.dedent("""\
        names = ['Hedy', 'Lamar']
        name = input(f'What is a name you like?')
        if name == 'Hedy':
          print(f'nice!')
        else:
          print(f'meh')
        if name in names:
          print(f'nice!')
        else:
          print(f'meh')""")

        self.single_level_tester(code=code, expected=expected)

    def test_turn_if_forward(self):
        code = textwrap.dedent("""\
        angle is 90, 180, 270
        direction is angle at random
        turn direction
        if direction is 180 forward 100""")

        expected = HedyTester.dedent(
            """\
            angle = ['90', '180', '270']""",
            HedyTester.list_access_transpiled('random.choice(angle)'),
            "direction = random.choice(angle)",
            HedyTester.turn_transpiled('direction', self.level),
            "if direction == '180':",
            (HedyTester.forward_transpiled(100, self.level), '  '))

        self.single_level_tester(code=code, expected=expected)

    def test_turn_if_forward_else_forward(self):
        code = textwrap.dedent("""\
        angle is 90, 180, 270
        direction is angle at random
        if direction is 180 forward direction
        else turn direction""")

        expected = HedyTester.dedent(
            """\
            angle = ['90', '180', '270']""",
            HedyTester.list_access_transpiled('random.choice(angle)'),
            "direction = random.choice(angle)",
            "if direction == '180':",
            (HedyTester.forward_transpiled('direction', self.level), '  '),
            "else:",
            (HedyTester.turn_transpiled('direction', self.level), '  '))

        self.single_level_tester(code=code, expected=expected)

    def test_list_access_index(self):
        code = textwrap.dedent("""\
        friends is Hedy, Lola, Frida
        friend is friends at 2
        print friend""")

        expected = HedyTester.dedent("friends = ['Hedy', 'Lola', 'Frida']",
                                     HedyTester.list_access_transpiled('friends[int(2)-1]'),
                                     "friend = friends[int(2)-1]",
                                     "print(f'{friend}')")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    #
    # negative tests
    #

    def test_if_indent_gives_parse_error(self):
        code = textwrap.dedent("""\
        option is ask 'Rock Paper or Scissors?'
        if option is Scissors
            print 'Its a tie!'""")

        expected = textwrap.dedent("""\
        option = input(f'Rock Paper or Scissors?')
        pass
        pass""")

        skipped_mappings = [
            SkippedMapping(SourceRange(2, 1, 2, 22), hedy.exceptions.ParseException),
            SkippedMapping(SourceRange(3, 1, 3, 23), hedy.exceptions.InvalidSpaceException),
        ]

        self.multi_level_tester(
            code=code,
            expected=expected,
            skipped_mappings=skipped_mappings,
            max_level=7
        )

    def test_line_with_if_with_space_gives_invalid(self):
        code = textwrap.dedent("""\
        name is Hedy
         if name is 3 print 'leuk' else print 'stom'""")

        expected = textwrap.dedent("""\
        name = 'Hedy'
        pass""")

        skipped_mappings = [
            SkippedMapping(SourceRange(2, 1, 2, 45), hedy.exceptions.InvalidSpaceException),
        ]

        self.multi_level_tester(
            code=code,
            expected=expected,
            skipped_mappings=skipped_mappings,
            max_level=7)

    def test_pront_should_suggest_print(self):
        code = "pront 'Hedy is leuk!'"
        expected = "pass"

        skipped_mappings = [
            SkippedMapping(SourceRange(1, 1, 1, 23), hedy.exceptions.InvalidCommandException),
        ]

        self.multi_level_tester(
            code=code,
            expected=expected,
            skipped_mappings=skipped_mappings,
            extra_check_function=lambda c: str(c.arguments['guessed_command']) == 'print',
        )

    def test_print_no_quotes(self):
        code = textwrap.dedent("""\
        print 'Hoi ik ben Hedy de Waarzegger
        print 'Ik kan voorspellen wie morgen de loterij wint!'
        naam is ask 'Wie ben jij?'""")

        expected = textwrap.dedent("""\
        pass
        print(f'Ik kan voorspellen wie morgen de loterij wint!')
        naam = input(f'Wie ben jij?')""")

        skipped_mappings = [
            SkippedMapping(SourceRange(1, 1, 1, 37), hedy.exceptions.UnquotedTextException),
        ]

        self.single_level_tester(
            code=code,
            expected=expected,
            skipped_mappings=skipped_mappings
        )

    def test_print_quote_gives_exception(self):
        code = textwrap.dedent("""\
        print 'what's your name?'""")
        expected = "pass"

        skipped_mappings = [
            SkippedMapping(SourceRange(1, 1, 1, 27), hedy.exceptions.UnquotedTextException),
        ]

        self.single_level_tester(
            code=code,
            expected=expected,
            skipped_mappings=skipped_mappings
        )

    def test_ask_with_quote(self):
        code = textwrap.dedent("""\
        name is ask 'what's your name?'
        print name""")

        self.multi_level_tester(
            code=code,
            exception=hedy.exceptions.UnquotedTextException,
            extra_check_function=lambda c: c.exception.error_location[0] == 1,
            max_level=17
        )

    def test_if_equality_print_backtick_text_gives_error(self):
        code = "if 1 is 1 print `yay!` else print `nay`"

        expected = textwrap.dedent("""\
        if '1' == '1':
          pass
        else:
          pass""")

        skipped_mappings = [
            SkippedMapping(SourceRange(1, 11, 1, 23), hedy.exceptions.UnquotedTextException),
            SkippedMapping(SourceRange(1, 29, 1, 40), hedy.exceptions.UnquotedTextException),
        ]

        self.multi_level_tester(
            max_level=5,
            code=code,
            expected=expected,
            skipped_mappings=skipped_mappings
        )

    def test_if_fix_nl(self):
        code = textwrap.dedent("""\
            naam is 5
            als naam is 5 print 'leuk'
            print 'minder leuk!'""")

        expected = HedyTester.dedent("""\
        naam = '5'
        if naam == '5':
          print(f'leuk')
        else:
          x__x__x__x = '5'
        print(f'minder leuk!')""")

        self.multi_level_tester(
            max_level=5,
            code=code,
            lang='nl',
            expected=expected,
            translate=False
        )

    #
    # if pressed tests
    #

    def test_if_pressed_x_is_letter_key(self):
        code = textwrap.dedent("""\
        if x is pressed print 'it is a letter key' else print 'it is another letter key'""")

        expected = HedyTester.dedent("""\
        pygame_end = False
        while not pygame_end:
          pygame.display.update()
          event = pygame.event.wait()
          if event.type == pygame.QUIT:
            pygame_end = True
            pygame.quit()
            break
          if event.type == pygame.KEYDOWN:
            if event.unicode == 'x':
              print(f'it is a letter key')
              break
            else:
              print(f'it is another letter key')
              break
            # End of PyGame Event Handler""")

        self.multi_level_tester(code=code, expected=expected, max_level=7)

    def test_if_pressed_x_is_variable(self):
        code = textwrap.dedent("""\
        x is a
        if x is pressed print 'it is a letter key' else print 'it is another letter key'""")

        expected = HedyTester.dedent("""\
        x = 'a'
        pygame_end = False
        while not pygame_end:
          pygame.display.update()
          event = pygame.event.wait()
          if event.type == pygame.QUIT:
            pygame_end = True
            pygame.quit()
            break
          if event.type == pygame.KEYDOWN:
            if event.key == x:
              print(f'it is a letter key')
              break
            else:
              print(f'it is another letter key')
              break
            # End of PyGame Event Handler""")

        self.multi_level_tester(code=code, expected=expected, max_level=7)

    def test_double_if_pressed(self):
        code = textwrap.dedent("""\
        if x is pressed print 'first key' else print 'something else'
        if y is pressed print 'second key' else print 'something else'""")

        expected = HedyTester.dedent("""\
        pygame_end = False
        while not pygame_end:
          pygame.display.update()
          event = pygame.event.wait()
          if event.type == pygame.QUIT:
            pygame_end = True
            pygame.quit()
            break
          if event.type == pygame.KEYDOWN:
            if event.unicode == 'x':
              print(f'first key')
              break
            else:
              print(f'something else')
              break
            # End of PyGame Event Handler
        pygame_end = False
        while not pygame_end:
          pygame.display.update()
          event = pygame.event.wait()
          if event.type == pygame.QUIT:
            pygame_end = True
            pygame.quit()
            break
          if event.type == pygame.KEYDOWN:
            if event.unicode == 'y':
              print(f'second key')
              break
            else:
              print(f'something else')
              break
            # End of PyGame Event Handler""")

        self.multi_level_tester(code=code, expected=expected, max_level=7)

    def test_if_pressed_has_enter_after_pressed(self):
        code = textwrap.dedent("""\
        if x is pressed
        print 'it is a letter key' else print 'something else'""")

        expected = HedyTester.dedent("""\
        pygame_end = False
        while not pygame_end:
          pygame.display.update()
          event = pygame.event.wait()
          if event.type == pygame.QUIT:
            pygame_end = True
            pygame.quit()
            break
          if event.type == pygame.KEYDOWN:
            if event.unicode == 'x':
              print(f'it is a letter key')
              break
            else:
              print(f'something else')
              break
            # End of PyGame Event Handler""")

        self.multi_level_tester(code=code, expected=expected, max_level=7)

    def test_if_pressed_1_is_number_key(self):
        code = textwrap.dedent("""\
        if 1 is pressed print 'it is a number key' else print 'something else'""")

        expected = HedyTester.dedent("""\
        pygame_end = False
        while not pygame_end:
          pygame.display.update()
          event = pygame.event.wait()
          if event.type == pygame.QUIT:
            pygame_end = True
            pygame.quit()
            break
          if event.type == pygame.KEYDOWN:
            if event.unicode == '1':
              print(f'it is a number key')
              break
            else:
              print(f'something else')
              break
            # End of PyGame Event Handler""")

        self.multi_level_tester(code=code, expected=expected, max_level=7)

    def test_if_pressed_with_trailing_spaces_after_key(self):
        code = textwrap.dedent("""\
        if x       is pressed print 'trailing spaces!' else print 'something else'""")

        expected = HedyTester.dedent("""\
        pygame_end = False
        while not pygame_end:
          pygame.display.update()
          event = pygame.event.wait()
          if event.type == pygame.QUIT:
            pygame_end = True
            pygame.quit()
            break
          if event.type == pygame.KEYDOWN:
            if event.unicode == 'x':
              print(f'trailing spaces!')
              break
            else:
              print(f'something else')
              break
            # End of PyGame Event Handler""")

        self.multi_level_tester(code=code, expected=expected, max_level=7)

    def test_if_pressed_has_enter_before_else(self):
        code = textwrap.dedent("""\
        if x is pressed print 'x is pressed!'
        else print 'x is not pressed!'""")

        expected = HedyTester.dedent("""\
        pygame_end = False
        while not pygame_end:
          pygame.display.update()
          event = pygame.event.wait()
          if event.type == pygame.QUIT:
            pygame_end = True
            pygame.quit()
            break
          if event.type == pygame.KEYDOWN:
            if event.unicode == 'x':
              print(f'x is pressed!')
              break
            else:
              print(f'x is not pressed!')
              break
            # End of PyGame Event Handler""")

        self.multi_level_tester(code=code, expected=expected, max_level=7)

    def test_if_pressed_has_enter_before_both_prints_and_else(self):
        code = textwrap.dedent("""\
        if x is pressed
        print 'x is pressed!'
        else
        print 'x is not pressed!'""")

        expected = HedyTester.dedent("""\
        pygame_end = False
        while not pygame_end:
          pygame.display.update()
          event = pygame.event.wait()
          if event.type == pygame.QUIT:
            pygame_end = True
            pygame.quit()
            break
          if event.type == pygame.KEYDOWN:
            if event.unicode == 'x':
              print(f'x is pressed!')
              break
            else:
              print(f'x is not pressed!')
              break
            # End of PyGame Event Handler""")

        self.multi_level_tester(code=code, expected=expected, max_level=7)

    def test_if_pressed_has_enter_before_first_print_and_else(self):
        code = textwrap.dedent("""\
        if x is pressed
        print 'x is pressed!'
        else print 'x is not pressed!'""")

        expected = HedyTester.dedent("""\
        pygame_end = False
        while not pygame_end:
          pygame.display.update()
          event = pygame.event.wait()
          if event.type == pygame.QUIT:
            pygame_end = True
            pygame.quit()
            break
          if event.type == pygame.KEYDOWN:
            if event.unicode == 'x':
              print(f'x is pressed!')
              break
            else:
              print(f'x is not pressed!')
              break
            # End of PyGame Event Handler""")

        self.multi_level_tester(code=code, expected=expected, max_level=7)

    def test_if_pressed_has_enter_before_second_print_and_else(self):
        code = textwrap.dedent("""\
        if x is pressed print 'x is pressed!'
        else
        print 'x is not pressed!'""")

        expected = HedyTester.dedent("""\
        pygame_end = False
        while not pygame_end:
          pygame.display.update()
          event = pygame.event.wait()
          if event.type == pygame.QUIT:
            pygame_end = True
            pygame.quit()
            break
          if event.type == pygame.KEYDOWN:
            if event.unicode == 'x':
              print(f'x is pressed!')
              break
            else:
              print(f'x is not pressed!')
              break
            # End of PyGame Event Handler""")

        self.multi_level_tester(code=code, expected=expected, max_level=7)

    def test_if_pressed_has_enter_before_both_prints(self):
        code = textwrap.dedent("""\
        if x is pressed
        print 'x is pressed!'
        else print 'x is not pressed!'""")

        expected = HedyTester.dedent("""\
        pygame_end = False
        while not pygame_end:
          pygame.display.update()
          event = pygame.event.wait()
          if event.type == pygame.QUIT:
            pygame_end = True
            pygame.quit()
            break
          if event.type == pygame.KEYDOWN:
            if event.unicode == 'x':
              print(f'x is pressed!')
              break
            else:
              print(f'x is not pressed!')
              break
            # End of PyGame Event Handler""")

        self.multi_level_tester(code=code, expected=expected, max_level=7)

    def test_if_pressed_else_with_turtle(self):
        code = textwrap.dedent("""\
        if x is pressed forward 25 else turn 90""")

        expected = HedyTester.dedent(f"""\
        pygame_end = False
        while not pygame_end:
          pygame.display.update()
          event = pygame.event.wait()
          if event.type == pygame.QUIT:
            pygame_end = True
            pygame.quit()
            break
          if event.type == pygame.KEYDOWN:
            if event.unicode == 'x':
              {HedyTester.indent(
                HedyTester.forward_transpiled(25, self.level),
                14, True)
              }
              break
            else:
              {HedyTester.indent(
                HedyTester.turn_transpiled(90, self.level),
                14, True)
              }
              break
            # End of PyGame Event Handler""")

        self.multi_level_tester(
            code=code,
            expected=expected,
            extra_check_function=self.is_turtle(),
            max_level=7
        )

    def test_if_pressed_non_latin(self):
        code = textwrap.dedent("""\
        if ض is pressed print 'arabic' else print 'something else'
        if ש is pressed print 'hebrew' else print 'something else'
        if й is pressed print 'russian' else print 'something else'""")

        expected = HedyTester.dedent("""\
        pygame_end = False
        while not pygame_end:
          pygame.display.update()
          event = pygame.event.wait()
          if event.type == pygame.QUIT:
            pygame_end = True
            pygame.quit()
            break
          if event.type == pygame.KEYDOWN:
            if event.unicode == 'ض':
              print(f'arabic')
              break
            else:
              print(f'something else')
              break
            # End of PyGame Event Handler
        pygame_end = False
        while not pygame_end:
          pygame.display.update()
          event = pygame.event.wait()
          if event.type == pygame.QUIT:
            pygame_end = True
            pygame.quit()
            break
          if event.type == pygame.KEYDOWN:
            if event.unicode == 'ש':
              print(f'hebrew')
              break
            else:
              print(f'something else')
              break
            # End of PyGame Event Handler
        pygame_end = False
        while not pygame_end:
          pygame.display.update()
          event = pygame.event.wait()
          if event.type == pygame.QUIT:
            pygame_end = True
            pygame.quit()
            break
          if event.type == pygame.KEYDOWN:
            if event.unicode == 'й':
              print(f'russian')
              break
            else:
              print(f'something else')
              break
            # End of PyGame Event Handler""")

        self.multi_level_tester(code=code, expected=expected, max_level=7)

    def test_if_pressed_missing_else_gives_error(self):
        code = textwrap.dedent("""\
        if x is pressed print 'hi!'""")

        expected = "pass"

        skipped_mappings = [
            SkippedMapping(SourceRange(1, 1, 1, 28), hedy.exceptions.MissingElseForPressitException),
        ]

        self.multi_level_tester(
            max_level=7,
            code=code,
            expected=expected,
            skipped_mappings=skipped_mappings
        )

    def test_if_pressed_missing_else_gives_error_with_new_line(self):
        code = textwrap.dedent("""\
        if x is pressed print 'hi!'\n\n""")

        expected = "pass"

        skipped_mappings = [
            SkippedMapping(SourceRange(1, 1, 1, 28), hedy.exceptions.MissingElseForPressitException),
        ]

        self.multi_level_tester(
            max_level=7,
            code=code,
            expected=expected,
            skipped_mappings=skipped_mappings
        )

    #
    # button tests
    #
    def test_button(self):
        code = textwrap.dedent("""\
        knop is button""")

        expected = HedyTester.dedent(f"""\
        create_button('knop')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_two_buttons(self):
        code = textwrap.dedent("""\
        knop1 is button
        knop2 is button""")

        expected = HedyTester.dedent(f"""\
        create_button('knop1')
        create_button('knop2')""")

        self.multi_level_tester(code=code, expected=expected, max_level=11)

    def test_if_button_is_pressed_print(self):
        code = textwrap.dedent("""\
        PRINT is button
        OTHER is button
        if PRINT is pressed print 'The PRINT button got pressed!' else print 'other button was pressed!'""")

        expected = HedyTester.dedent(f"""\
        create_button('PRINT')
        create_button('OTHER')
        pygame_end = False
        while not pygame_end:
          pygame.display.update()
          event = pygame.event.wait()
          if event.type == pygame.QUIT:
            pygame_end = True
            pygame.quit()
            break
          if event.type == pygame.USEREVENT:
            if event.key == 'PRINT':
              print(f'The PRINT button got pressed!')
              break
            else:
              print(f'other button was pressed!')
              break
            # End of PyGame Event Handler""")

        self.multi_level_tester(code=code, expected=expected, max_level=7)

    def test_source_map(self):
        code = textwrap.dedent("""\
        print 'Do you want a good (g) or bad (b) ending?'
        if g is pressed print 'They lived happily ever after ❤'
        else print 'The prince was eaten by a hippopotamus 😭'""")

        expected_code = textwrap.dedent("""\
        print(f'Do you want a good (g) or bad (b) ending?')
        pygame_end = False
        while not pygame_end:
          pygame.display.update()
          event = pygame.event.wait()
          if event.type == pygame.QUIT:
            pygame_end = True
            pygame.quit()
            break
          if event.type == pygame.KEYDOWN:
            if event.unicode == 'g':
              print(f'They lived happily ever after ❤')
              break
            else:
              print(f'The prince was eaten by a hippopotamus 😭')
              break
            # End of PyGame Event Handler""")

        expected_source_map = {
            '1/1-1/50': '1/1-1/52',
            '2/17-2/56': '12/7-12/48',
            '3/6-3/54': '15/7-15/57',
            '2/1-3/54': '2/1-17/34',
            '1/1-3/55': '1/1-17/34'
        }

        self.single_level_tester(code, expected=expected_code)
        self.source_map_tester(code=code, expected_source_map=expected_source_map)
