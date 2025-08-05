from pyswip import Prolog
prolog = Prolog()

# Updated statement patterns to be consistent with Prolog rules
statement_patterns = {
    "and are siblings": "sibling_base({0}, {1})",  # Uses base fact
    "is a sister of": "sister_base({0}, {1})",     # Uses base fact
    "is the mother of": "mother_base({0}, {1})",   # Uses base fact - FIXED
    "is a grandmother of": "grandmother({0}, {1})", # Direct assertion (no base needed)
    "is a child of": "child({0}, {1})",            # Direct assertion
    "is a daughter of": "daughter({0}, {1})",      # Direct assertion
    "is an uncle of": "uncle({0}, {1})",            # Direct assertion
    "is a brother of": "brother_base({0}, {1})",   # Uses base fact
    "is the father of": "father_base({0}, {1})",   # Uses base fact - FIXED
    "and are the parents of": ["parent({0}, {2})", "parent({1}, {2})"],  # Direct assertion
    "is a grandfather of": "grandfather({0}, {1})", # Direct assertion
    "and are the children of": ["child({0}, {3})", "child({1}, {3})", "child({2}, {3})"],  # Direct assertion
    "is a son of": "son({0}, {1})",               # Direct assertion
    "is an aunt of": "aunt({0}, {1})",            # Direct assertion
}

# Fixed question patterns - CORRECTED queries to match proper relationships
question_patterns = {
    # Questions answerable by Yes or No
    r"Are (\w+) and (\w+) siblings\?": "sibling({0}, {1})",
    r"Is (\w+) a sister of (\w+)\?": "sister({0}, {1})",
    r"Is (\w+) a brother of (\w+)\?": "brother({0}, {1})",
    r"Is (\w+) the mother of (\w+)\?": "mother({0}, {1})",
    r"Is (\w+) the father of (\w+)\?": "father({0}, {1})",
    r"Is (\w+) a grandmother of (\w+)\?": "grandmother({0}, {1})", 
    r"Is (\w+) a grandfather of (\w+)\?": "grandfather({0}, {1})",
    r"Is (\w+) a daughter of (\w+)\?": "daughter({0}, {1})",
    r"Is (\w+) a son of (\w+)\?": "son({0}, {1})",
    r"Is (\w+) a child of (\w+)\?": "child({0}, {1})",
    r"Is (\w+) an uncle of (\w+)\?": "uncle({0}, {1})",
    r"Is (\w+) an aunt of (\w+)\?": "aunt({0}, {1})",
    r"Are (\w+) and (\w+) relatives\?": "relative({0}, {1})",

    # Questions that expect a list of name/s - CORRECTED QUERIES
    r"Who are the siblings of (\w+)\?": "sibling(X, {0})",     # Find X where sibling(X, person)
    r"Who are the sisters of (\w+)\?": "sister(X, {0})",      # Find X where sister(X, person)  
    r"Who are the brothers of (\w+)\?": "brother(X, {0})",    # Find X where brother(X, person)
    r"Who is the mother of (\w+)\?": "mother(X, {0})",        # Find X where mother(X, person)
    r"Who is the father of (\w+)\?": "father(X, {0})",        # Find X where father(X, person)
    r"Who are the parents of (\w+)\?": "parent(X, {0})",      # Find X where parent(X, person)
    r"Who are the daughters of (\w+)\?": "daughter(X, {0})",  # FIXED: Find X where daughter(X, person) - X is daughter of person
    r"Who are the sons of (\w+)\?": "son(X, {0})",           # FIXED: Find X where son(X, person) - X is son of person
    r"Who are the children of (\w+)\?": "child(X, {0})",     # FIXED: Find X where child(X, person) - X is child of person
    r"Who are the uncles of (\w+)\?": "uncle(X, {0})",       # Find X where uncle(X, person)
    r"Who are the aunts of (\w+)\?": "aunt(X, {0})",         # Find X where aunt(X, person)
    r"Who are the grandfathers of (\w+)\?": "grandfather(X, {0})",  # Find X where grandfather(X, person)
    r"Who are the grandmothers of (\w+)\?": "grandmother(X, {0})",  # Find X where grandmother(X, person)
    r"Who are the relatives of (\w+)\?": "relative(X, {0})",        # Find X where relative(X, person)
}

import re

def process_input(user_input):
    for phrase, template in statement_patterns.items():
        # Build regex pattern dynamically based on known phrase
        if phrase == "and are siblings":
            match = re.match(r"(\w+)\s+and\s+(\w+)\s+are\s+siblings\.", user_input)
            if match:
                person1, person2 = match.groups()
                fact = template.format(person1, person2) 
                add_fact(fact)
                return
        elif phrase == "is a sister of":
            match = re.match(r"(\w+)\s+is\s+a\s+sister\s+of\s+(\w+)\.", user_input)
            if match:
                person1, person2 = match.groups()
                fact = template.format(person1, person2)
                add_fact(fact)
                return
        elif phrase == "is the mother of":  # FIXED
            match = re.match(r"(\w+)\s+is\s+the\s+mother\s+of\s+(\w+)\.", user_input)
            if match:
                person1, person2 = match.groups()
                fact = template.format(person1, person2)
                add_fact(fact)
                return
        elif phrase == "is a grandmother of":
            match = re.match(r"(\w+)\s+is\s+a\s+grandmother\s+of\s+(\w+)\.", user_input)
            if match:
                person1, person2 = match.groups()
                fact = template.format(person1, person2)
                add_fact(fact)
                return
        elif phrase == "is a child of":
            match = re.match(r"(\w+)\s+is\s+a\s+child\s+of\s+(\w+)\.", user_input)
            if match:
                person1, person2 = match.groups()
                fact = template.format(person1, person2)
                add_fact(fact)
                return
        elif phrase == "is a daughter of":
            match = re.match(r"(\w+)\s+is\s+a\s+daughter\s+of\s+(\w+)\.", user_input)
            if match:
                person1, person2 = match.groups()
                fact = template.format(person1, person2)
                add_fact(fact)
                return
        elif phrase == "is an uncle of":  # FIXED
            match = re.match(r"(\w+)\s+is\s+an\s+uncle\s+of\s+(\w+)\.", user_input)
            if match:
                person1, person2 = match.groups()
                fact = template.format(person1, person2)
                add_fact(fact)
                return
        elif phrase == "is a brother of":
            match = re.match(r"(\w+)\s+is\s+a\s+brother\s+of\s+(\w+)\.", user_input)
            if match:
                person1, person2 = match.groups()
                fact = template.format(person1, person2)
                add_fact(fact)
                return
        elif phrase == "is the father of":  # FIXED
            match = re.match(r"(\w+)\s+is\s+the\s+father\s+of\s+(\w+)\.", user_input)
            if match:
                person1, person2 = match.groups()
                fact = template.format(person1, person2)
                add_fact(fact)
                return
        elif phrase == "and are the parents of":
            match = re.match(r"(\w+)\s+and\s+(\w+)\s+are\s+the\s+parents\s+of\s+(\w+)\.", user_input)
            if match:
                person1, person2, child = match.groups()
                facts = [template[0].format(person1, child), template[1].format(person2, child)]
                for fact in facts:
                    add_fact(fact)
                return
        elif phrase == "is a grandfather of":
            match = re.match(r"(\w+)\s+is\s+a\s+grandfather\s+of\s+(\w+)\.", user_input)
            if match:
                person1, person2 = match.groups()
                fact = template.format(person1, person2)
                add_fact(fact)
                return
        elif phrase == "and are the children of":
            match = re.match(r"(\w+)\s+and\s+(\w+)\s+and\s+(\w+)\s+are\s+the\s+children\s+of\s+(\w+)\.", user_input)
            if match:
                person1, person2, person3, parent = match.groups()
                facts = [template[0].format(person1, parent), template[1].format(person2, parent), template[2].format(person3, parent)]
                for fact in facts:
                    add_fact(fact)
                return
        elif phrase == "is a son of":
            match = re.match(r"(\w+)\s+is\s+a\s+son\s+of\s+(\w+)\.", user_input)
            if match:
                person1, person2 = match.groups()
                fact = template.format(person1, person2)
                add_fact(fact)
                return
        elif phrase == "is an aunt of":
            match = re.match(r"(\w+)\s+is\s+an\s+aunt\s+of\s+(\w+)\.", user_input)
            if match:
                person1, person2 = match.groups()
                fact = template.format(person1, person2)
                add_fact(fact)
                return
    print("Unknown statement.")

def process_question(user_input):
    for pattern, query_template in question_patterns.items():
        match = re.match(pattern, user_input)
        if match:
            groups = match.groups()
            query = query_template.format(*groups)
            
            # Check if this is a "Who" question (returns multiple results)
            if "Who are" in pattern:
                answer_who_question(query, pattern, groups[0])
            else:
                answer_question(query)
            return
    print("Unknown question.")

prolog.consult("FamilyRule.pl")

def is_consistent(fact):
    try:
        # Parse the predicate and arguments from the fact string
        predicate = fact.split('(')[0]
        args = fact.split('(')[1].rstrip(')').split(', ')
        X = args[0]
        Y = args[1]

        # Prevent circular parent-child relationships
        if predicate == "child":
            result = list(prolog.query(f"child({Y}, {X})"))
            if result:
                return False
        elif predicate == "parent":
            result = list(prolog.query(f"parent({Y}, {X})"))
            if result:
                return False
        elif predicate == "father" or predicate == "mother":
            result = list(prolog.query(f"child({Y}, {X})"))
            if result:
                return False

        return True
    except Exception as e:
        print(f"Consistency check failed: {e}")
        return True

def add_fact(fact):
    if is_consistent(fact):
        try:
            prolog.assertz(fact)
            print("OK! I learned something.")
        except:
            print("That's impossible!")
    else:
        print("That's impossible!")

def answer_question(query):
    try:
        result = list(prolog.query(query))
        if result:
            print("Yes!")
        else:
            print("No!")
    except:
        print("Invalid query.")

def answer_who_question(query, pattern, person):
    try:
        results = list(prolog.query(query))
        if results:
            # Extract the names from the results
            names = [result['X'] for result in results]
            
            # Format the response based on the question type
            if "siblings" in pattern:
                if len(names) == 1:
                    print(f"{names[0]} is a sibling of {person}.")
                elif len(names) == 2:
                    print(f"{names[0]} and {names[1]} are siblings of {person}.")
                else:
                    name_list = ", ".join(names[:-1]) + f", and {names[-1]}"
                    print(f"{name_list} are siblings of {person}.")
                    
            elif "sisters" in pattern:
                if len(names) == 1:
                    print(f"{names[0]} is a sister of {person}.")
                elif len(names) == 2:
                    print(f"{names[0]} and {names[1]} are sisters of {person}.")
                else:
                    name_list = ", ".join(names[:-1]) + f", and {names[-1]}"
                    print(f"{name_list} are sisters of {person}.")
                    
            elif "brothers" in pattern:
                if len(names) == 1:
                    print(f"{names[0]} is a brother of {person}.")
                elif len(names) == 2:
                    print(f"{names[0]} and {names[1]} are brothers of {person}.")
                else:
                    name_list = ", ".join(names[:-1]) + f", and {names[-1]}"
                    print(f"{name_list} are brothers of {person}.")
                    
            elif "children" in pattern:
                if len(names) == 1:
                    print(f"{names[0]} is a child of {person}.")
                elif len(names) == 2:
                    print(f"{names[0]} and {names[1]} are children of {person}.")
                else:
                    name_list = ", ".join(names[:-1]) + f", and {names[-1]}"
                    print(f"{name_list} are children of {person}.")
                    
            elif "parents" in pattern:
                if len(names) == 1:
                    print(f"{names[0]} is a parent of {person}.")
                elif len(names) == 2:
                    print(f"{names[0]} and {names[1]} are parents of {person}.")
                else:
                    name_list = ", ".join(names[:-1]) + f", and {names[-1]}"
                    print(f"{name_list} are parents of {person}.")
                    
            elif "daughters" in pattern:
                if len(names) == 1:
                    print(f"{names[0]} is a daughter of {person}.")
                elif len(names) == 2:
                    print(f"{names[0]} and {names[1]} are daughters of {person}.")
                else:
                    name_list = ", ".join(names[:-1]) + f", and {names[-1]}"
                    print(f"{name_list} are daughters of {person}.")
                    
            elif "sons" in pattern:
                if len(names) == 1:
                    print(f"{names[0]} is a son of {person}.")
                elif len(names) == 2:
                    print(f"{names[0]} and {names[1]} are sons of {person}.")
                else:
                    name_list = ", ".join(names[:-1]) + f", and {names[-1]}"
                    print(f"{name_list} are sons of {person}.")
                    
            elif "uncles" in pattern:
                if len(names) == 1:
                    print(f"{names[0]} is an uncle of {person}.")
                elif len(names) == 2:
                    print(f"{names[0]} and {names[1]} are uncles of {person}.")
                else:
                    name_list = ", ".join(names[:-1]) + f", and {names[-1]}"
                    print(f"{name_list} are uncles of {person}.")
                    
            elif "aunts" in pattern:
                if len(names) == 1:
                    print(f"{names[0]} is an aunt of {person}.")
                elif len(names) == 2:
                    print(f"{names[0]} and {names[1]} are aunts of {person}.")
                else:
                    name_list = ", ".join(names[:-1]) + f", and {names[-1]}"
                    print(f"{name_list} are aunts of {person}.")
                    
            elif "grandfathers" in pattern:
                if len(names) == 1:
                    print(f"{names[0]} is a grandfather of {person}.")
                elif len(names) == 2:
                    print(f"{names[0]} and {names[1]} are grandfathers of {person}.")
                else:
                    name_list = ", ".join(names[:-1]) + f", and {names[-1]}"
                    print(f"{name_list} are grandfathers of {person}.")
                    
            elif "grandmothers" in pattern:
                if len(names) == 1:
                    print(f"{names[0]} is a grandmother of {person}.")
                elif len(names) == 2:
                    print(f"{names[0]} and {names[1]} are grandmothers of {person}.")
                else:
                    name_list = ", ".join(names[:-1]) + f", and {names[-1]}"
                    print(f"{name_list} are grandmothers of {person}.")
                    
            elif "relatives" in pattern:
                if len(names) == 1:
                    print(f"{names[0]} is a relative of {person}.")
                elif len(names) == 2:
                    print(f"{names[0]} and {names[1]} are relatives of {person}.")
                else:
                    name_list = ", ".join(names[:-1]) + f", and {names[-1]}"
                    print(f"{name_list} are relatives of {person}.")
                    
            elif "mother" in pattern:
                if len(names) == 1:
                    print(f"{names[0]} is the mother of {person}.")
                else:
                    print("No one found.")
                    
            elif "father" in pattern:
                if len(names) == 1:
                    print(f"{names[0]} is the father of {person}.")
                else:
                    print("No one found.")
        else:
            print("No one found.")
    except Exception as e:
        print(f"Query failed: {e}")

while True:
    user_input = input("").strip()

    if user_input.upper() == "END":
        print("Goodbye!")
        break
    
    if user_input.endswith("."): # stating a fact
        process_input(user_input)
    elif user_input.endswith("?"): # asking a question
        process_question(user_input)  # Fixed: Now properly processes questions
    else:
        print("I don't understand that.")

