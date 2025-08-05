/* The purpose of PROLOG is merely to serve as an inference engine
for the intelligence of the bot. */

% FamilyRule.pl - Family Relationship Rules
% Logical rules and dynamic declarations for family relationships

% --- Allow runtime assertions for ALL predicates ---
:- dynamic father/2, mother/2, sibling/2, sister/2, brother/2.
:- dynamic grandfather/2, grandmother/2, uncle/2, aunt/2.
:- dynamic parent/2, child/2, daughter/2, son/2.
:- dynamic sibling_base/2, grandparent/2, grandchild/2.
:- dynamic grandson/2, granddaughter/2, nephew/2, niece/2.
:- dynamic cousin/2, relative/2.

% --- Dynamic base facts (what actually gets asserted) ---
:- dynamic father_base/2, mother_base/2, sibling_base/2.
:- dynamic brother_base/2, sister_base/2.

% --- BASE CONSTRAINTS (prevent self-relationships in base facts) ---
% Group all father/2 clauses together
father(X, Y) :- father_base(X, Y), X \= Y.

% Group all mother/2 clauses together  
mother(X, Y) :- mother_base(X, Y), X \= Y.

% Group all sibling/2 clauses together
sibling(X, Y) :- sibling_base(X, Y), X \= Y.
sibling(X, Y) :- sibling_base(Y, X), X \= Y.

% Group all brother/2 clauses together
brother(X, Y) :- brother_base(X, Y), X \= Y.
brother(X, Y) :- sibling(X, Y), male(X), X \= Y.

% Group all sister/2 clauses together
sister(X, Y) :- sister_base(X, Y), X \= Y.
sister(X, Y) :- sibling(X, Y), female(X), X \= Y.

% --- Logical rules ---

% Parent relationship derived from mother/father (with constraint)
parent(X, Y) :- father(X, Y), X \= Y.
parent(X, Y) :- mother(X, Y), X \= Y.

% Group all child/2 clauses together
child(X, Y) :- son(X, Y), X \= Y.
child(X, Y) :- daughter(X, Y), X \= Y.

% Group all son/2 clauses together
son(X, Y) :- parent(Y, X), male(X), X \= Y.

% Group all daughter/2 clauses together
daughter(X, Y) :- parent(Y, X), female(X), X \= Y.

% --- ENHANCED GENDER INFERENCE ---

% Basic gender inference from direct relationships
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

% --- GRANDPARENT RELATIONSHIPS ---
grandfather(X, Z) :- father(X, Y), parent(Y, Z), X \= Z, Y \= Z, X \= Y.
grandmother(X, Z) :- mother(X, Y), parent(Y, Z), X \= Z, Y \= Z, X \= Y.
grandparent(X, Z) :- parent(X, Y), parent(Y, Z), X \= Z, Y \= Z, X \= Y.

% Grandchild relationships (with constraint)
grandchild(X, Y) :- grandparent(Y, X), X \= Y.
grandson(X, Y) :- grandparent(Y, X), male(X), X \= Y.
granddaughter(X, Y) :- grandparent(Y, X), female(X), X \= Y.

% --- UNCLE/AUNT RELATIONSHIPS ---
% Group all uncle/2 clauses together
uncle(X, Z) :- male(X), sibling(X, Y), parent(Y, Z), X \= Z, X \= Y, Y \= Z.
uncle(X, Z) :- brother(X, Y), parent(Y, Z), X \= Z, X \= Y, Y \= Z.

% Group all aunt/2 clauses together
aunt(X, Z) :- female(X), sibling(X, Y), parent(Y, Z), X \= Z, X \= Y, Y \= Z.
aunt(X, Z) :- sister(X, Y), parent(Y, Z), X \= Z, X \= Y, Y \= Z.

% Nephew/Niece relationships (with constraint)
nephew(X, Y) :- male(X), parent(Z, X), sibling(Z, Y), X \= Y, X \= Z, Y \= Z.
niece(X, Y) :- female(X), parent(Z, X), sibling(Z, Y), X \= Y, X \= Z, Y \= Z.

% --- COUSIN RELATIONSHIPS ---
cousin(X, Y) :- parent(Z, X), sibling(Z, W), parent(W, Y), X \= Y, X \= Z, X \= W, Y \= Z, Y \= W, Z \= W.

% --- RELATIVE RELATIONSHIPS ---
relative(X, Y) :- parent(X, Y), X \= Y.
relative(X, Y) :- parent(Y, X), X \= Y.
relative(X, Y) :- sibling(X, Y), X \= Y.
relative(X, Y) :- grandparent(X, Y), X \= Y.
relative(X, Y) :- grandparent(Y, X), X \= Y.
relative(X, Y) :- uncle(X, Y), X \= Y.
relative(X, Y) :- aunt(X, Y), X \= Y.
relative(X, Y) :- nephew(X, Y), X \= Y.
relative(X, Y) :- niece(X, Y), X \= Y.
relative(X, Y) :- cousin(X, Y), X \= Y.

% Transitive relative relationship (with cycle prevention)
relative(X, Y) :- 
    relative(X, Z), 
    relative(Z, Y), 
    X \= Y, X \= Z, Y \= Z.
