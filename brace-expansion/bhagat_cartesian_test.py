import unittest
from bhagat_cartesian import *

class TestCartesianProduct(unittest.TestCase):

    ## Basic Functionality Tests:
    
    def test_single_char_input(self):
        self.assertEqual(cartesianProduct("a"), ["a"])

    def test_simple_string_input(self):
        self.assertEqual(cartesianProduct("ababa"), ["ababa"])

    def test_braces_input(self):
        self.assertEqual(cartesianProduct("{a,b}"), ["a", "b"])

    def test_braces_on_right_side_of_simple_string(self):
        self.assertEqual(cartesianProduct("c{a,b}"), ["ca", "cb"])

    def test_braces_on_left_side_of_simple_string(self):
        self.assertEqual(cartesianProduct("{a,b}c"), ["ac", "bc"])

    def test_multiple_same_level_braces(self):
        self.assertEqual(cartesianProduct("{a,b}{c,d}"),
                                          ["ac", "ad", "bc", "bd"]) 

    def test_nested_braces(self):
        """Used test case given by prompt"""
        target_list = ["abijk", "abijl", "acdgijk", "acdgijl",
                       "acegijk", "acegijl", "acfgijk", "acfgijl",
                       "ahijk", "ahijl"]
        input_string = "a{b,c{d,e,f}g,h}ij{k,l}"
        self.assertEqual(cartesianProduct(input_string), target_list)

    ## Intermediate Functionality Tests
    ## Covers: Brace Closures, Empty Braces, Braces with 1 arg,
    ##         Stray Commas
        
    def test_no_brace_closure(self):
        self.assertEqual(cartesianProduct("a{b,c"), ["a{b,c"])

    def test_no_brace_closure_with_multiple_same_level_braces(self):
        self.assertEqual(cartesianProduct("a{b,c}{d"), ["ab{d", "ac{d"])

    def test_no_brace_closure_nested(self):
        self.assertEqual(cartesianProduct("a{b{c,d}"), ["a{bc", "a{bd"])

    def test_begins_with_closing_brace(self):
        self.assertEqual(cartesianProduct("{a,"), ["{a,"])

    def test_empty_braces(self):
        self.assertEqual(cartesianProduct("a{}"), ["a{}"])

    def test_one_argument_in_brace(self):
        self.assertEqual(cartesianProduct("a{b}"), ["a{b}"])

    def test_successive_commas_implying_empty_string_elements(self):
        self.assertEqual(cartesianProduct("a{b,,c}d"), ["abd", "ad", "acd"])

    def test_commas_before_braces(self):
        self.assertEqual(cartesianProduct(",{a,{b,c}}"), [",a", ",b", ",c"])

    def test_commas_before_closing_braces(self):
        self.assertEqual(cartesianProduct("{a,}b"), ["ab", "b"])

    ##  Tests for character escaping. Note that two backslashes are
    ##  needed to represent one 'input' backslash, in order to escape
    ##  the python interpreter. 

    def test_backslash_comma_escape(self):
        self.assertEqual(cartesianProduct("{a\\,b}c"), ["{a,b}c"])

    def test_backslash_open_brace_escape(self):
        self.assertEqual(cartesianProduct("{a,\\{b,c}}"), ["a}", "{b}", "c}"])

    def test_backslash_closed_brace_escape(self):
        self.assertEqual(cartesianProduct("{a,b{c,d\\}}"), ["{a,bc", "{a,bd}"])

    def test_backslash_escapes_itself(self):
        self.assertEqual(cartesianProduct("{a,b\\\\}c"), ["ac", "b\\c"])

    def test_error_if_last_character_is_backslash(self):
        try: 
            cartesianProduct("{a,b}c\\")
            self.fail("Program should fail when final character is an " +
                      "unescaped backslash.")
        except UnescapedBackslashTerminatedStringException:
            pass

    def test_space_as_argument_delimiter(self):
        self.assertEqual(cartesianProduct("{a,b} {c,d}"), ["a", "b", "c", "d"])

    def test_multiple_spaces(self):
        self.assertEqual(cartesianProduct("a  b  c"), ["a", "", "b", "", "c"])
    
    def test_backslash_escapes_space(self):
        self.assertEqual(cartesianProduct("{a,b}\\ {c,d}"), ["a c", "a d",
                                                             "b c", "b d"])

# Tests below are considered tests for non-'public' methods. Tests above this
# line should not need to change, as they represent the publicly supported,
# guaranteed methods of bhagat_cartesian. 

class TopLevelCommaSplitter(unittest.TestCase):
    
    def test_basic_comma_split(self):
        self.assertEqual(split_by_top_level_commas("a,b"), ["a", "b"])

    def test_ignore_comma_in_simple_braces(self):
        self.assertEqual(split_by_top_level_commas("a{b,c}"), ["a{b,c}"])

    def test_ignore_comma_in_nested_braces(self):
        test_list = split_by_top_level_commas("a{b,c{d,e}}f,g")
        self.assertEqual(test_list, ["a{b,c{d,e}}f", "g"])

    def test_acknowledge_comma_if_braces_mismatched(self):
        test_list = split_by_top_level_commas("a{b,c{d,e}f")
        self.assertEqual(test_list, ["a{b", "c{d,e}f"])

class TestTopLevelBracePairFinder(unittest.TestCase):

    def test_basic_finder(self):
        self.assertEqual(top_level_brace_pairs("{}"), [(0,1)])

    def test_multiple_same_level_pairs(self):
        self.assertEqual(top_level_brace_pairs("{a}{b}"), [(0,2), (3,5)])

    def test_find_if_nested(self):
        self.assertEqual(top_level_brace_pairs("a{b{c,d}e}f"), [(1,9)])

    def test_find_when_braces_mismatched(self):
        self.assertEqual(top_level_brace_pairs("{a,{b,c}"), [(3,7)])

class TestOuterBraceFinder(unittest.TestCase):

    def test_basic_finder(self):
        self.assertEqual(outer_brace_finder("{}"), [0,1])

    def test_multiple_same_level_pairs(self):
        self.assertEqual(outer_brace_finder("{a}{b}"), [0,2])

    def test_find_if_nested(self):
        self.assertEqual(outer_brace_finder("a{b{c,d}e}f"), [1,9])

    def test_find_when_braces_mismatched(self):
        self.assertEqual(outer_brace_finder("{a,{b,c}"), [3,7])
      
class TestUnescapeString(unittest.TestCase):

    def test_commas_unescaped(self):
        self.assertEqual(unescape_string("ab,c\\,de,f"), "ab,c,de,f")

    def test_braces_unescaped(self):
        self.assertEqual(unescape_string("a{\\{b,c}"), "a{{b,c}")

    def test_spaces_unescaped(self):
        self.assertEqual(unescape_string("a b\\ c"), "a b c")

    def test_backslashes_unescaped(self):
        self.assertEqual(unescape_string("a b\\\\ c"), "a b\\ c")

    def test_fail_if_final_character_is_unescaped_backslash(self):
        try:
            unescape_string("hello\\")
            fail("Program should throw IndexError if final character is \"\\\"")
        except UnescapedBackslashTerminatedStringException:
            pass

    def test_final_character_is_escaped_backslash(self):
        self.assertEqual(unescape_string("hello\\\\"), "hello\\")

class TestSplitWithEscaping(unittest.TestCase):

    def test_basic_string_split(self):
        self.assertEqual(split_with_escaping("a,b"), ["a", "b"])

    def test_escaped_comma(self):
        self.assertEqual(split_with_escaping("a,b\\,c"), ["a", "b\\,c"])
    
class TestStringDistributor(unittest.TestCase):

    def test_single_element_lists(self):
        self.assertEquals(stringListDistribute(["a"], ["b"]), ["ab"])

    def test_first_argument_empty_list(self):
        self.assertEquals(stringListDistribute([], ["a"]), ["a"])

    def test_multiple_elements_in_first_arg(self):
        self.assertEquals(stringListDistribute(["a", "b"], ["a"]),
                                               ["aa", "ba"])

    def test_multiple_elements_in_second_arg(self):
        self.assertEquals(stringListDistribute(["a"], ["a", "b"]),
                                               ["aa", "ab"])

    def test_multiple_element_args(self):
        self.assertEquals(stringListDistribute(["a", "b"], ["c", "d"]),
                                               ["ac", "ad", "bc", "bd"])

if __name__ == '__main__':
    unittest.main()
