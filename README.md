langgen
=======

From samples create languages. Each language is able to generate a list of similar names, extracting probable sequences from the samples provided.

how to use it
=============

Given a set of names this library can generate similar names. The library comes with examples from real and fantasy languages (from Roman names to Elvish names) and the user is free to provide others. To create original languages different sets of samples can be created.

```python
>>> from langgen.langgen import *
>>> lang_samples = load_all_lang_samples()
>>> lang_samples.keys()
['elven', 'beowulf', 'welsh', 'celticmyth', 'norse', 'japanese', 'norsemyth', 'italian_cities', 'roman', 'greek', 'saxon', 'hebrew', 'russian', 'polish', 'odin']
```

Let's generate some Roman-soundin names:

```python
>>> samples = lang_samples["roman"]
>>> language = Language.language_from_samples(samples)
>>> language.name()
'Tiusius'
>>> language.name()
'Canuus'
>>> language.name()
'Laeliusla'
>>> language.name()
'Siius'
```
