# pep302_example
This is a test for Python Import Hooks, defined on PEP302.

The ImportHooke code is inside the *`__init__.py`* file under the *example* directory.

Mainly we have one package **example** that contains three modules (**v1**, **v2** and **v3**).

Each module contains two submodules (**myclass** and **myenum**). The difference between the modules are on the **enums** definitions, and the classes inherite from the previous versions (e.g.: **example.v2.myclass.MyClass** inherits from **example.v1.myclass.MyClass**), but v2.myclass.MyClass should use the enum from v2.

So, our import hook will evaluate who started the "import tree" and replace the enum to the correct version, if needed.

To see it working, run:
```
python3.5 run_v1.py
python3.5 run_v2.py
python3.5 run_v3.py
```

You will see that, despite the expected result would be v2 and v3 using the enum from v1, they use the enum from it's own package version.

But if you run
```
python3.5 run_all.py
```

You will see the "expected" behaviour from the default python and the default inheritance theory.

NOTE: This code only works for **python >= 3.5**.
