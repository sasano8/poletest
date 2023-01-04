# index


## example

``` python
from poletest.difftool import DiffTool, Raised

class Person:
  def greet(self, suffix=""):
    raise NotImplementedError()

class A(Person):
  def greet(self, name=""):
    return f"My name is {name}."

class B(Person):
  def greet(self, name=""):
    return f"I'm {name}."

class C(Person):
  def greet(self):
    return "Hi."

tool = DiffTool(A(), B(), C())

assert list(tool("greet", "Bob")) == [
    'My name is Bob.',
    "I'm Bob.",
    Raised(TypeError, 'greet() takes 1 positional argument but 2 were given')
]

# Take the first result as positive and compare it with the rest
assert not tool("greet", "Bob")

tool = DiffTool(A(), A())
assert tool("greet", "Bob") # All result are same.

tool = DiffTool(A(), B())
assert tool("greet", "Bob") # Raise Error.
```


``` python
class FsspecDiffTool(DiffTool):
    def exists(self, *args, **kwargs):
        return self.dispatch("exists", *args, **kwargs)

    def mkdir(self, *args, **kwargs):
        return self.dispatch("mkdir", *args, **kwargs)

    def test_senario(self):
        self.mkdir("test")
```