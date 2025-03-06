/- @@@
# File for Test Cases
@@@ -/

import DMT1.MyWork.hw3.syntax
import DMT1.MyWork.hw3.semantics

open DMT1.MyWork.hw3.syntax
open DMT1.MyWork.hw3.semantics

/- @@@
In this file you will write test cases annotated
with light commentary for the upates you make to
the syntax.lean and semnantics.lean files, to show
that your syntactic extensions and semantics for
them are good.
@@@-/

/- @@@
As usual, here are a few variable expressions that
you can use to form a larger expressions if you wish.
@@@ -/

def X : Expr := {⟨0⟩}
def Y : Expr := {⟨1⟩}
def Z : Expr := {⟨2⟩}
def catHappy := {⟨3⟩}
def dogHappy := {⟨4⟩}

/- @@@
Here's an example of an expression using some of our
already defined concrete notation.
@@@ -/

def e0 : Expr := X ∧ ¬Y ∨ Z

/-!
Now here are two interpretations, represented as
Lean functions from the variables underlying our
variable expressions to Bool.

The first interpretation models a world where X
is true, Y is false, and Z is true.
-/

def i1 : Interp
| ⟨0⟩ => true
| ⟨1⟩ => false
| ⟨2⟩ => true
| _ => false


/-! @@@
Our second interpretation models a world with a
X false, Y true, and Z false.
@@@ -/

def i2 : Interp
| ⟨0⟩ => false
| ⟨1⟩ => true
| ⟨2⟩ => false
| _ => false

/- @@@
With these interpretations in hand, we can now
apply ⟦e0⟧ to each of them to see which, if either,
satisfies *e*. Hint: figure it out for yourself,
then check!
@@@ -/

#eval ⟦e0⟧ i1
#eval ⟦e0⟧ i2
