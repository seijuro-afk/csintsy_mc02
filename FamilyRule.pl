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
:- dynamic male/1, female/1. % Added dynamic declaration for gender predicates

% --- Dynamic base facts (what actually gets asserted) ---
:- dynamic father_base/2, mother_base/2, sibling_base/2.
:- dynamic brother_base/2, sister_base/2.

% --- BASE CONSTRAINTS (prevent self-relationships in base facts) ---
% Group all father/2 clauses together
% A child can only have one father. 'once/1' ensures only the first found father_base fact is used.
father(X, Y) :- once(father_base(X, Y)), X \= Y.

% Group all mother/2 clauses together
% A child can only have one mother. 'once/1' ensures only the first found mother_base fact is used.
mother(X, Y) :- once(mother_base(X, Y)), X \= Y.

% Group all sibling/2 clauses together
% Sibling is symmetric and cannot be self
sibling(X, Y) :- sibling_base(X, Y), X \= Y.
sibling(X, Y) :- sibling_base(Y, X), X \= Y.

% Group all brother/2 clauses together
% A brother is a male sibling
brother(X, Y) :- brother_base(X, Y), X \= Y.
brother(X, Y) :- sibling(X, Y), male(X), X \= Y.

% Group all sister/2 clauses together
% A sister is a female sibling
sister(X, Y) :- sister_base(X, Y), X \= Y.
sister(X, Y) :- sibling(X, Y), female(X), X \= Y.

% --- Logical rules ---

% Parent relationship derived from mother/father
parent(X, Y) :- father(X, Y).
parent(X, Y) :- mother(X, Y).

% Child relationship derived from parent
child(X, Y) :- parent(Y, X).

% Son is a male child
son(X, Y) :- child(X, Y), male(X).

% Daughter is a female child
daughter(X, Y) :- child(X, Y), female(X).


% Basic gender inference from direct base facts.
% IMPORTANT: These rules must NOT be recursive or depend on predicates
% that themselves require gender to be known (e.g., son, daughter, aunt, uncle).
male(X) :- father_base(X, _). % If X is a father (base fact), X is male.
female(X) :- mother_base(X, _). % If X is a mother (base fact), X is female.
% For individuals whose gender is not inferred from father_base/mother_base,
% you should assert their gender directly (e.g., male(john). female(mary).).


% --- GRANDPARENT RELATIONSHIPS ---
% Grandfather: father of a parent. Includes constraints to prevent cycles.
grandfather(X, Z) :- father(X, Y), parent(Y, Z), X \= Z, Y \= Z, X \= Y.
% Grandmother: mother of a parent. Includes constraints to prevent cycles.
grandmother(X, Z) :- mother(X, Y), parent(Y, Z), X \= Z, Y \= Z, X \= Y.
% Grandparent: parent of a parent. Includes constraints to prevent cycles.
grandparent(X, Z) :- parent(X, Y), parent(Y, Z), X \= Z, Y \= Z, X \= Y.

% Grandchild relationships
grandchild(X, Y) :- grandparent(Y, X), X \= Y.
grandson(X, Y) :- grandchild(X, Y), male(X), X \= Y.
granddaughter(X, Y) :- grandchild(X, Y), female(X), X \= Y.

% --- UNCLE/AUNT RELATIONSHIPS ---
% Uncle: male sibling of a parent
uncle(X, Z) :- parent(Y, Z), brother(X, Y), X \= Z.
% Aunt: female sibling of a parent
aunt(X, Z) :- parent(Y, Z), sister(X, Y), X \= Z.

% Nephew/Niece relationships
% Nephew: male child of a sibling
nephew(X, Y) :- male(X), parent(Z, X), sibling(Z, Y), X \= Y.
% Niece: female child of a sibling
niece(X, Y) :- female(X), parent(Z, X), sibling(Z, Y), X \= Y.


% --- RELATIVE RELATIONSHIPS ---
% Base relative relationships (direct relationships)
relative_direct(X, Y) :- parent(X, Y).
relative_direct(X, Y) :- parent(Y, X).
relative_direct(X, Y) :- sibling(X, Y).
relative_direct(X, Y) :- grandparent(X, Y).
relative_direct(X, Y) :- grandparent(Y, X).
relative_direct(X, Y) :- uncle(X, Y).
relative_direct(X, Y) :- aunt(X, Y).
relative_direct(X, Y) :- nephew(X, Y).
relative_direct(X, Y) :- niece(X, Y).


% Main relative predicate: Initiates the transitive search
relative(X, Y) :- relative_transitive(X, Y, [X]).

% Helper predicate for transitive relative relationship with cycle prevention
% relative_transitive(CurrentPerson, TargetPerson, VisitedList)
% Base case: CurrentPerson is directly related to TargetPerson, and TargetPerson hasnt been visited yet.
relative_transitive(X, Y, Visited) :-
    relative_direct(X, Y),
    \+ member(Y, Visited). % Ensure Y has not been visited to prevent immediate loops

% Recursive step: Find an intermediate relative Z, and then continue the search from Z to Y.
relative_transitive(X, Y, Visited) :-
    relative_direct(X, Z), % Find a direct relative Z of X
    X \= Z, % Ensure X and Z are different
    \+ member(Z, Visited), % Ensure Z has not been visited in this path
    relative_transitive(Z, Y, [Z|Visited]). % Recurse, adding Z to the visited list

% --- Consistency Checks ---

% Checks if a child has multiple fathers.
% Succeeds if there are two different individuals F1 and F2 who are both base fathers of Child.
multiple_fathers_for_child(Child) :-
    father_base(Father1, Child),
    father_base(Father2, Child),
    Father1 \= Father2.

% Checks if a child has multiple mothers.
% Succeeds if there are two different individuals M1 and M2 who are both base mothers of Child.
multiple_mothers_for_child(Child) :-
    mother_base(Mother1, Child),
    mother_base(Mother2, Child),
    Mother1 \= Mother2.

% General predicate to check for overall data consistency regarding unique parents.
% This predicate succeeds if any inconsistency (multiple fathers or mothers) is found.
% Your bot can query `inconsistent_data` to ensure the integrity of its family tree.
inconsistent_data :-
    multiple_fathers_for_child(_).
inconsistent_data :-
    multiple_mothers_for_child(_).