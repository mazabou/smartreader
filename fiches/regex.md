### Metacharacters

|Character|Description|
|-|-|
|\*|0 or more|
|+|1 or more|
|?|0 or more|
|{5}|exact number|
|{1,60}|range on number|
|.||
|^|in M mode, each line, replaced by \A (only begining of string)|
|$|replaced by \Z|
|\b|Word boundary, won’t match when it’s contained inside another word (whitespace or a non-alphanumeric character (opposite:\B)|
|[]||
|or|match either A or B|
|\||
|()||

|Sequence|Description|Equivalent|
|-|-|-|
|\d|Matches any decimal digit|[0-9]|
|\D|Matches any non-digit character|[^0-9]|
|\s|Matches any whitespace character|[ \t\n\r\f\v]|
|\S|Matches any non-whitespace character|[^ \t\n\r\f\v]|
|\w|Matches any alphanumeric character|[a-zA-Z0-9_]|
|\W|Matches any non-alphanumeric character|[^a-zA-Z0-9_]|

### Methods

|Method/Attribute|Purpose|
|-|-|
|match()|Determine if the RE matches at the beginning of the string|
|search()|Scan through a string, looking for any location where this RE matches|
|findall()|Find all substrings where the RE matches, and returns them as a list|
|finditer()|Find all substrings where the RE matches, and returns them as an iterator (match object instances)|

match() and search() return None if no match can be found. If they’re successful, a match object instance is returned, containing information about the match: where it starts and ends, the substring it matched, and more.

⚠️ When you give re.findall() a regex with groups (parenthesized expressions) in it, it returns the groups that match

### Match Object

|Method/Attribute|Purpose|
|-|-|
|group()|Return the string matched by the RE|
|start()|Return the starting position of the match|
|end()|Return the ending position of the match|
|span()|Return a tuple containing the (start, end) positions of the match|

```python
p = re.compile( ... )
m = p.match( 'string goes here' )
if m:
    print 'Match found: ', m.group()
else:
    print 'No match'
```

You don’t have to create a pattern object and call its methods. Under the hood, these functions simply create a pattern object for you and call the appropriate method on it. They also store the compiled object in a cache, so future calls using the same RE are faster.

(?:...) is a non-capturing paranthesis

### Modifying Strings

|Method/Attribute|Purpose|
|-|-|
|split()|Split the string into a list, splitting it wherever the RE matches|
|sub()|Find all substrings where the RE matches, and replace them with a different string|
|subn()|Does the same thing as sub(), but returns the new string and the number of replacements|

maxsplit, count etc: default value 0 means all

Empty matches are replaced only when they’re not adjacent to a previous match.

```python
>>> p = re.compile('x*')
>>> p.sub('-', 'abxd')
'-a-b-d-'}
```

```python
>>> p = re.compile('section{ ( [^}]* ) }', re.VERBOSE)
>>> p.sub(r'subsection{\1}','section{First} section{second}')
'subsection{First} subsection{second}'
```

replacement can also be a function

```python
>>> def hexrepl(match):
...     "Return the hex string for a decimal number"
...     value = int(match.group())
...     return hex(value)
...
>>> p = re.compile(r'\d+')
>>> p.sub(hexrepl, 'Call 65490 for printing, 49152 for user code.')
'Call 0xffd2 for printing, 0xc000 for user code.'
```

### Compilation flags

modify some aspects of how regular expressions work

Multiple flags can be specified by bitwise OR-ing them; re.I | re.M

|Flag	|Meaning|
|-|-|
|DOTALL, S|	Make . match any character, including newlines|
|IGNORECASE, I|	Do case-insensitive matches|
|LOCALE, L|	Do a locale-aware match|
|MULTILINE, M	|Multi-line matching, affecting ^ and $|
|VERBOSE, X|	Enable verbose REs, which can be organized more cleanly and understandably.|
|UNICODE, U	|Makes several escapes like \w, \b, \s and \d dependent on the Unicode character database.|

L

LOCALE

Make \\w, \\W, \\b, and \\B, dependent on the current locale.

Locales are a feature of the C library intended to help in writing programs that take account of language differences. For example, if you’re processing French text, you’d want to be able to write \\w+ to match words, but \\w only matches the character class [A-Za-z]; it won’t match 'é' or 'ç'. If your system is configured properly and a French locale is selected, certain C functions will tell the program that 'é' should also be considered a letter. Setting the LOCALE flag when compiling a regular expression will cause the resulting compiled object to use these C functions for \\w; this is slower, but also enables \\w+ to match French words as you’d expect.

```python
charref = re.compile(r"""
 &[#]                # Start of a numeric entity reference
 (
     0[0-7]+         # Octal form
   | [0-9]+          # Decimal form
   | x[0-9a-fA-F]+   # Hexadecimal form
 )
 ;                   # Trailing semicolon
""", re.VERBOSE)
```

### Analysing examples

```python
import re
print(re.split(r'\s*','here are some words')) 
```

\\s: space

r: this is a regular expression example: \\n isn’t the same (r’\\n’ = ‘\\\\n’)

r for raw

\*: 0 instance or more

```python
print(re.split(r'(\s*)','here are some words'))
```

( ): break and include

```python
print(re.split(r'[a-f]','here are some words'))
```

⚠️ case sensitive

range of letters

multipe ranges: [a-df-z0-9]

inside a character class, a metacharacter is stripped of its special nature

[^5] any character except those in the class

```python
print(re.split(r'[a-f]','here are some words’,re.I|re.M))
```

flags:

re.I: ignore case uppercase = downcase

re.M: multiline/ continuisly

```python
print(re.split(r'[a-f][a-f]','here are some words’,re.I|re.M))
```

next to each other! arrangement of characters

```python
print(re.findall(r'\d{1,5}\s\w+\s\w+\.', 'cascae213 main st.asaef'))
```

search for a pattern

findall: find instances

\\d: look for digits \\d = [0-9]

\\D: everything but digits

\\w: number or letter

\\.: regular period

. = any character but newline (\\n)

{,10} = 0-10

```python
pat = re.compile(r'<title>+.*<title>+',re.I|re.M)
title = re.findall(pat,str(text))
```

otherwise methods are executed everytime: saves time and ressources if the pattern is used multiple times.

if you need to match a [ or \\, you can precede them with a backslash to remove their special meaning: \\[ or \\\\.

### Phone number

0X XX XX XX XX

0X-XX-XX-XX-XX

0X.XX.XX.XX.XX

0XXXXXXXXX

```sh
^0\d([ .-]?\d{2}){4}$
```

^: on cherche l’expression au début de la chaîne

$: on cherche l’expression à la fin de la chaîne

```sh
>>> re.search(r"abc", "abcdef")
<_sre.SRE_Match object at 0x00AC1640>
```

Si l’expression n’est pas trouvée, la fonction renvoie None

```sh
if re.match(expression, chaine)
```

### Replace

```sh
>>> re.sub(r"(ab)", r" \1 ", "abcdef")
' ab cdef'
```

\\\<group number\>: starts at 1

### Group ids

```sh
(?P<id>[0-9]{2})
```

use \\g\<group name\>

### Grouping

Regular expressions are often used to dissect strings by writing a RE divided into several subgroups which match different components of interest

Groups are marked by the '(', ')' metacharacters. '(' and ')' have much the same meaning as they do in mathematical expressions; they group together the expressions contained inside them, and you can repeat the contents of a group with a repeating qualifier, such as \*, +, ?, or {m,n}

⚠️ ( )\* doesn’t appear in m.groups()

Subgroups are numbered from left to right, from 1 upward. Groups can be nested; to determine the number, just count the opening parenthesis characters, going from left to right

```python
>>> p = re.compile('(a(b)c)d')
>>> m = p.match('abcd')
>>> m.group(0)
'abcd'
>>> m.group(1)
'abc'
>>> m.group(2)
'b'
>>> m.group(2,1,2)
('b', 'abc', 'b')
>>> m.groups()
('abc', 'b')
```

### Backreferences

Backreferences in a pattern allow you to specify that the contents of an earlier capturing group must also be found at the current location in the string.

```python
>>> p = re.compile(r'\b(\w+)\s+\1\b')
>>> p.search('Paris in the the spring').group()
'the the'
```

### Lookahead Assertions

(?=…) Positive lookahead assertion: This succeeds if the contained regular expression, represented here by ..., successfully matches at the current location, and fails otherwise. But, once the contained expression has been tried, the matching engine doesn’t advance at all; the rest of the pattern is tried right where the assertion started.

(?!…) Negative lookahead assertion: This is the opposite of the positive assertion; it succeeds if the contained expression doesn’t match at the current position in the string.

.\*[.](?!bat$)[^.]\*$ The negative lookahead means: if the expression bat doesn’t match at this point, try the rest of the pattern; if bat$ does match, the whole pattern will fail. The trailing $ is required to ensure that something like sample.batch, where the extension only starts with bat, will be allowed. The [^.]\* makes sure that the pattern works when there are multiple dots in the filename.

.\*[.](?!bat$|exe$)[^.]\*$



Python extensions
-----------------

If the first character after the question mark is a P, you know that it’s an extension that’s specific to Python.

Non-capturing group

Sometimes you’ll want to use a group to collect a part of a regular expression, but aren’t interested in retrieving the group’s contents

```python
>>> m = re.match("([abc])+", "abc")
>>> m.groups()
('c',)
>>> m = re.match("(?:[abc])+", "abc")
>>> m.groups()
()
```

It should be mentioned that there’s no performance difference in searching between capturing and non-capturing groups; neither form is any faster than the other.

### Named Group

```python
>>> p = re.compile(r'(?P<word>\b\w+\b)')
>>> m = p.search( '(((( Lots of punctuation )))' )
>>> m.group('word')
'Lots'
>>> m.group(1)
'Lots'
```

works with back refrences too:

```python
>>> p = re.compile(r'\b(?P<word>\w+)\s+(?P=word)\b')
>>> p.search('Paris in the the spring').group()
'the the'
```

### Non-greedy Qualifiers

\*?, +?,??, and {m,n}? match as little text as possible

```python
>>> print re.match('<.*?>', s).group()
<html>
```

the '\>' is tried immediately after the first '\<' matches, and when it fails, the engine advances a character at a time, retrying the '\>' at every step

\* is greddy and will match till the end

### Password

```python
r"^[A-Za-z0-9]{6,}$"
```

### Example

I would like to match: some.name.separated.by.dots

^\\w+(?:\\.\\w+)+$

(\\w+(\\.|$))+

### How it works

<https://docs.python.org/2/howto/regex.html>

![](resources/43AD06642D225D1E0C5928395BFFBA07.jpg)

### Intresting stuff

1\. Perl 5 added several additional features to standard regular expressions, and the Python re module supports most of them. It would have been difficult to choose new single-keystroke metacharacters or new special sequences beginning with \\ to represent the new features without making Perl’s regular expressions confusingly different from standard REs. If you chose & as a new metacharacter, for example, old expressions would be assuming that & was a regular character and wouldn’t have escaped it by writing \\& or [&].

The solution chosen by the Perl developers was to use (?...) as the extension syntax. ? immediately after a parenthesis was a syntax error because the ? would have nothing to repeat, so this didn’t introduce any compatibility problems. The characters immediately after the ? indicate what extension is being used, so (?=foo) is one thing (a positive lookahead assertion) and (?:foo)is something else (a non-capturing group containing the subexpression foo).

Python adds an extension syntax to Perl’s extension syntax. If the first character after the question mark is a P, you know that it’s an extension that’s specific to Python. Currently there are two such extensions: (?P...) defines a named group, and (?P=name) is a backreference to a named group. If future versions of Perl 5 add similar features using a different syntax, the re module will be changed to support the new syntax, while preserving the Python-specific syntax for compatibility’s sake.

2\. Sometimes using the re module is a mistake. If you’re matching a fixed string, or a single character class, and you’re not using any re features such as the IGNORECASE flag, then the full power of regular expressions may not be required. Strings have several methods for performing operations with fixed strings and they’re usually much faster, because the implementation is a single small C loop that’s been optimized for the purpose, instead of the large, more generalized regular expression engine.

3\. Sometimes you’ll be tempted to keep using re.match(), and just add .\* to the front of your RE. Resist this temptation and use re.search() instead. The regular expression compiler does some analysis of REs in order to speed up the process of looking for a match. One such analysis figures out what the first character of a match must be; for example, a pattern starting with Crow must match starting with a 'C'. The analysis lets the engine quickly scan through the string looking for the starting character, only trying the full match if a 'C' is found. Adding .\* defeats this optimization, requiring scanning to the end of the string and then backtracking to find a match for the rest of the RE. Use re.search() instead.

4\. Note that parsing HTML or XML with regular expressions is painful. Quick-and-dirty patterns will handle common cases, but HTML and XML have special cases that will break the obvious regular expression; by the time you’ve written a regular expression that handles all of the possible cases, the patterns will be verycomplicated. Use an HTML or XML parser module for such tasks.

