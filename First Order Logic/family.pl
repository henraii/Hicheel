male(bataa).
male(bold).
male(tomor).
male(dorj).
male(zolboo).
male(munkh).
male(temuulen).
male(bat).

female(saraa).
female(oyuna).
female(tsetseg).
female(ganaa).
female(anar).
female(naraa).
female(enkhee).

parent(bataa, bold).
parent(bataa, oyuna).
parent(bataa, tomor).
parent(saraa, bold).
parent(saraa, oyuna).
parent(saraa, tomor).
parent(bold, anar).
parent(bold, zolboo).
parent(tsetseg, anar).
parent(tsetseg, zolboo).
parent(dorj, munkh).
parent(dorj, naraa).
parent(oyuna, munkh).
parent(oyuna, naraa).
parent(tomor, enkhee).
parent(ganaa, enkhee).
parent(bat, temuulen).
parent(anar, temuulen).

person(X) :- male(X).
person(X) :- female(X).

father(X, Y) :- parent(X, Y), male(X).

mother(X, Y) :- parent(X, Y), female(X).

son(X, Y) :- parent(Y, X), male(X).

daughter(X, Y) :- parent(Y, X), female(X).

grandparent(X, Y) :- parent(X, Z), parent(Z, Y).

sibling(X, Y) :- parent(P, X), parent(P, Y), X \= Y.

brother(X, Y) :- sibling(X, Y), male(X).

sister(X, Y) :- sibling(X, Y), female(X).

uncle(X, Y) :- parent(P, Y), brother(X, P).

aunt(X, Y) :- parent(P, Y), sister(X, P).

cousin(X, Y) :- parent(P, X), parent(Q, Y), sibling(P, Q).

ancestor(X, Y) :- parent(X, Y).
ancestor(X, Y) :- parent(X, Z), ancestor(Z, Y).

descendant(X, Y) :- ancestor(Y, X).

has_child(X) :- parent(X, _).

childless(X) :- person(X), \+ has_child(X).

great_grandparent(X, Y) :- parent(X, Z), grandparent(Z, Y).
