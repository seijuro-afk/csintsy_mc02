/* The purpose of PROLOG is merely to serve as an inference engine
for the intelligence of the bot. */

% FamilyRule.pl - Family Relationship Rules
% Logical rules and dynamic declarations for family relationships

% --- Allow runtime assertions ---
:- dynamic father/2, mother/2, sibling/2, sister/2, brother/2.
:- dynamic grandfather/2, grandmother/2, uncle/2, aunt/2.
:- dynamic parent/2, child/2, daughter/2, son/2.

% --- Logical rules ---

% Parent relationship derived from mother/father
parent(X, Y) :- father(X, Y).
parent(X, Y) :- mother(X, Y).

% Gender inference
male(X) :- father(X, _).
male(X) :- son(X, _).
male(X) :- brother(X, _).
male(X) :- grandfather(X, _).
male(X) :- uncle(X, _).

female(X) :- mother(X, _).
female(X) :- daughter(X, _).
female(X) :- sister(X, _).
female(X) :- grandmother(X, _).
female(X) :- aunt(X, _).

% Symmetric sibling relationship - fixed version
sibling(X, Y) :- sibling_base(X, Y).
sibling(X, Y) :- sibling_base(Y, X).

% Base sibling facts (this is what gets asserted)
:- dynamic sibling_base/2.

% Alternative: if you want to keep the current approach, make sure it works both ways
% sibling(X, Y) :- brother(X, Y).
% sibling(X, Y) :- sister(X, Y).
% sibling(X, Y) :- brother(Y, X).
% sibling(X, Y) :- sister(Y, X).
