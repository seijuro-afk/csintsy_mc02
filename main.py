from pyswip import Prolog
import re

# Initialize Prolog engine
prolog = Prolog()

# Consult the Prolog file containing family rules
# Ensure 'FamilyRule.pl' is in the same directory or accessible path
prolog.consult("FamilyRule.pl")

# Updated statement patterns to be consistent with Prolog rules
# These patterns are used to parse user input and form Prolog facts
statement_patterns = {
    "and are siblings": "sibling_base({0}, {1})", # Uses base fact
    "is a sister of": "sister_base({0}, {1})",  # Uses base fact
    "is the mother of": "mother_base({0}, {1})",  # Uses base fact
    "is a grandmother of": "grandmother({0}, {1})", # Direct assertion (no base needed)
    "is a child of": "child({0}, {1})", # Direct assertion
    "is a daughter of": "daughter({0}, {1})", # Direct assertion
    "is an uncle of": "uncle({0}, {1})", # Direct assertion
    "is a brother of": "brother_base({0}, {1})", # Uses base fact
    "is the father of": "father_base({0}, {1})", # Uses base fact
    "and are the parents of": ["parent({0}, {2})", "parent({1}, {2})"], # Direct assertion
    "is a grandfather of": "grandfather({0}, {1})", # Direct assertion
    "and are the children of": ["child({0}, {3})", "child({1}, {3})", "child({2}, {3})"], # Direct assertion
    "is a son of": "son({0}, {1})", # Direct assertion
    "is an aunt of": "aunt({0}, {1})", # Direct assertion
}

# Fixed question patterns - CORRECTED queries to match proper relationships
# These patterns are used to parse user questions and form Prolog queries
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
    r"Who are the siblings of (\w+)\?": "sibling(X, {0})", # Find X where sibling(X, person)
    r"Who are the sisters of (\w+)\?": "sister(X, {0})", # Find X where sister(X, person)
    r"Who are the brothers of (\w+)\?": "brother(X, {0})", # Find X where brother(X, person)
    r"Who is the mother of (\w+)\?": "mother(X, {0})", # Find X where mother(X, person)
    r"Who is the father of (\w+)\?": "father(X, {0})", # Find X where father(X, person)
    r"Who are the parents of (\w+)\?": "parent(X, {0})", # Find X where parent(X, person)
    r"Who are the daughters of (\w+)\?": "daughter(X, {0})", # Find X where daughter(X, person) - X is daughter of person
    r"Who are the sons of (\w+)\?": "son(X, {0})",  # Find X where son(X, person) - X is son of person
    r"Who are the children of (\w+)\?": "child(X, {0})",  # Find X where child(X, person) - X is child of person
    r"Who are the uncles of (\w+)\?": "uncle(X, {0})", # Find X where uncle(X, person)
    r"Who are the aunts of (\w+)\?": "aunt(X, {0})", # Find X where aunt(X, person)
    r"Who are the grandfathers of (\w+)\?": "grandfather(X, {0})", # Find X where grandfather(X, person)
    r"Who are the grandmothers of (\w+)\?": "grandmother(X, {0})", # Find X where grandmother(X, person)
    r"Who are the relatives of (\w+)\?": "relative(X, {0})", # Find X where relative(X, person)
}

# Function to process user statements (adding facts to Prolog)
def process_input(user_input):
    # First try the complex patterns with multiple people
    for phrase, template in statement_patterns.items():
        # Handle multi-person statements first (they have special patterns)
        if isinstance(template, list):
            if phrase == "and are the parents of" and len(template) == 2:
                match = re.match(r"(\w+)\s+and\s+(\w+)\s+are\s+the\s+parents\s+of\s+(\w+)\.", user_input)
                if match:
                    person1, person2, child = match.groups()
                    facts = [template[0].format(person1, child), template[1].format(person2, child)]
                    for fact in facts:
                        add_fact(fact)
                    return
            elif phrase == "and are the children of" and len(template) == 3:
                match = re.match(r"(\w+)\s+and\s+(\w+)\s+and\s+(\w+)\s+are\s+the\s+children\s+of\s+(\w+)\.", user_input)
                if match:
                    person1, person2, person3, parent = match.groups()
                    facts = [template[0].format(person1, parent), template[1].format(person2, parent), template[2].format(person3, parent)]
                    for fact in facts:
                        add_fact(fact)
                    return
            elif phrase == "and are siblings" and not isinstance(template, list):
                match = re.match(r"(\w+)\s+and\s+(\w+)\s+are\s+siblings\.", user_input)
                if match:
                    person1, person2 = match.groups()
                    fact = template.format(person1, person2)
                    add_fact(fact)
                    return
        # Then handle single-fact patterns with explicit regex patterns
        else:
            if phrase == "is a sister of":
                match = re.match(r"(\w+)\s+is\s+an?\s+sister\s+of\s+(\w+)\.", user_input)
                if match:
                    person1, person2 = match.groups()
                    fact = template.format(person1, person2)
                    add_fact(fact)
                    return
            elif phrase == "is the mother of":
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
            elif phrase == "is an uncle of":
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
            elif phrase == "is the father of":
                match = re.match(r"(\w+)\s+is\s+the\s+father\s+of\s+(\w+)\.", user_input)
                if match:
                    person1, person2 = match.groups()
                    fact = template.format(person1, person2)
                    add_fact(fact)
                    return
            elif phrase == "is a grandfather of":
                match = re.match(r"(\w+)\s+is\s+a\s+grandfather\s+of\s+(\w+)\.", user_input)
                if match:
                    person1, person2 = match.groups()
                    fact = template.format(person1, person2)
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
                    
    # If we get here, no pattern matched
    print("Unknown statement.")

# Function to process user questions (querying Prolog)
def process_question(user_input):
    for pattern, query_template in question_patterns.items():
        match = re.match(pattern, user_input)
        if match:
            groups = match.groups()
            query = query_template.format(*groups)

            # Check if this is a "Who" question (returns multiple results)
            if "Who are" in pattern or "Who is" in pattern:
                answer_who_question(query, pattern, groups[-1] if groups else None) # Pass the last group as the reference person
            else:
                answer_question(query)
            return
    print("Unknown question.")

# Function to perform consistency checks before adding a fact
def is_consistent(fact):
    try:
        # Parse the predicate and arguments from the fact string
        predicate = fact.split('(')[0]
        args = fact.split('(')[1].rstrip(')').split(', ')
        X = args[0]
        Y = args[1] if len(args) > 1 else None # Y might not exist for gender facts

        # --- GENERATIONAL CONSISTENCY CHECKS ---
        # Prevent circular parent-child relationships (e.g., A is child of B, B is child of A)
        if predicate in ["parent", "father_base", "mother_base"]:
            if Y and list(prolog.query(f"child({Y}, {X})")):
                print(f"Consistency check failed: {Y} cannot be a child of {X} if {X} is already a child of {Y}.")
                return False
        elif predicate == "child":
            if Y and list(prolog.query(f"child({Y}, {X})")):
                print(f"Consistency check failed: {Y} cannot be a child of {X} if {X} is already a child of {Y}.")
                return False

        # NEW CHECK: If X is already a child of Y, X cannot be a parent of Y
        if predicate in ["father_base", "mother_base", "parent"]:
            if Y and list(prolog.query(f"child({X}, {Y})")):
                print(f"Consistency check failed: {X} cannot be a parent of {Y} if {X} is already a child of {Y} (circular relationship).")
                return False

        # Prevent grandparent contradictions
        if predicate in ["father_base", "mother_base"]:
            if Y and list(prolog.query(f"grandchild({X}, {Y})")):
                print(f"Consistency check failed: {X} cannot be parent of {Y} if {X} is already {Y}'s grandchild.")
                return False
            if Y and list(prolog.query(f"grandparent({Y}, {X})")):
                print(f"Consistency check failed: {X} cannot be parent of {Y} if {Y} is already {X}'s grandparent.")
                return False

        # --- COMPREHENSIVE GENDER CONSISTENCY CHECKS ---
        
        # 1. FIRST CHECK: If asserting a male role, check if person is already female
        male_roles = ["father_base", "brother_base", "son", "grandfather", "uncle"]
        female_roles = ["mother_base", "sister_base", "daughter", "grandmother", "aunt"]
        
        if predicate in male_roles:
            # Check if X is already in ANY female role
            for female_role in female_roles:
                # Check if X is in subject position (X is female_role of someone)
                if list(prolog.query(f"{female_role}({X}, _)")):
                    print(f"Gender consistency failed: {X} cannot be both male ({predicate}) and female ({female_role}).")
                    return False
            
            # Also check directly if X is known to be female
            if list(prolog.query(f"female({X})")):
                print(f"Gender consistency failed: {X} cannot be a {predicate} because {X} is female.")
                return False
                
        # 2. SECOND CHECK: If asserting a female role, check if person is already male
        elif predicate in female_roles:
            # Check if X is already in ANY male role
            for male_role in male_roles:
                # Check if X is in subject position (X is male_role of someone)
                if list(prolog.query(f"{male_role}({X}, _)")):
                    print(f"Gender consistency failed: {X} cannot be both female ({predicate}) and male ({male_role}).")
                    return False
            
            # Also check directly if X is known to be male
            if list(prolog.query(f"male({X})")):
                print(f"Gender consistency failed: {X} cannot be a {predicate} because {X} is male.")
                return False

        # 3. SPECIFIC CHECKS FOR daughter/son CASES
        if predicate == "daughter":
            # Check if X is already a father (most direct contradiction to your example)
            if list(prolog.query(f"father({X}, _)")):
                print(f"Gender consistency failed: {X} cannot be a daughter if {X} is already a father.")
                return False
            # Check other male roles too
            if list(prolog.query(f"son({X}, _)")) or list(prolog.query(f"brother({X}, _)")):
                print(f"Gender consistency failed: {X} cannot be a daughter and have a male role.")
                return False
                
        elif predicate == "son":
            # Check if X is already a mother or other female role
            if list(prolog.query(f"mother({X}, _)")):
                print(f"Gender consistency failed: {X} cannot be a son if {X} is already a mother.")
                return False
            if list(prolog.query(f"daughter({X}, _)")) or list(prolog.query(f"sister({X}, _)")):
                print(f"Gender consistency failed: {X} cannot be a son and have a female role.")
                return False

        # --- UNIQUE PARENT CONSISTENCY CHECKS ---
        if predicate == "father_base":
            existing_fathers = list(prolog.query(f"father_base(F, {Y})"))
            if existing_fathers and existing_fathers[0]['F'] != X:
                print(f"Consistency check failed: {Y} already has a father ({existing_fathers[0]['F']}).")
                return False
        elif predicate == "mother_base":
            existing_mothers = list(prolog.query(f"mother_base(M, {Y})"))
            if existing_mothers and existing_mothers[0]['M'] != X:
                print(f"Consistency check failed: {Y} already has a mother ({existing_mothers[0]['M']}).")
                return False

        return True
    except Exception as e:
        print(f"An error occurred during consistency check: {e}")
        return False # Default to False if an error occurs during check

# Function to add a fact to Prolog after consistency check
def add_fact(fact):
    if is_consistent(fact):
        try:
            prolog.assertz(fact)
            print("OK! I learned something.")
        except Exception as e:
            print(f"That's impossible! Error asserting fact: {e}")
    else:
        print("That's impossible! (Consistency check failed)")

# Function to answer Yes/No questions
def answer_question(query):
    try:
        result = list(prolog.query(query))
        if result:
            print("Yes!")
        else:
            print("No!")
    except Exception as e:
        print(f"Invalid query: {e}")

# Function to answer "Who" questions (listing results)
def answer_who_question(query, pattern, person):
    try:
        results = list(prolog.query(query))
        if results:
            names = [result['X'] for result in results]
            
            # Format the response based on relationship and count
            relationship_info = {
                "siblings": {"singular": "a sibling", "plural": "siblings"},
                "sisters": {"singular": "a sister", "plural": "sisters"},
                "brothers": {"singular": "a brother", "plural": "brothers"},
                "children": {"singular": "a child", "plural": "children"},
                "parents": {"singular": "a parent", "plural": "parents"},
                "daughters": {"singular": "a daughter", "plural": "daughters"},
                "sons": {"singular": "a son", "plural": "sons"},
                "uncles": {"singular": "an uncle", "plural": "uncles"},
                "aunts": {"singular": "an aunt", "plural": "aunts"},
                "grandfathers": {"singular": "a grandfather", "plural": "grandfathers"},
                "grandmothers": {"singular": "a grandmother", "plural": "grandmothers"},
                "relatives": {"singular": "a relative", "plural": "relatives"},
                "mother": {"singular": "the mother", "plural": "mothers"},
                "father": {"singular": "the father", "plural": "fathers"}
            }
            
            # Find which relationship we're dealing with
            rel_type = None
            for rel in relationship_info:
                if rel in pattern:
                    rel_type = rel
                    break
                    
            if rel_type:
                if len(names) == 1:
                    print(f"{names[0]} is {relationship_info[rel_type]['singular']} of {person}.")
                elif len(names) == 2:
                    print(f"{names[0]} and {names[1]} are {relationship_info[rel_type]['plural']} of {person}.")
                else:
                    name_list = ", ".join(names[:-1]) + f", and {names[-1]}"
                    print(f"{name_list} are {relationship_info[rel_type]['plural']} of {person}.")
            else:
                # Fallback in case pattern doesn't match any known relationship
                print(f"Found: {', '.join(names)}")
        else:
            print("No one found.")
    except Exception as e:
        print(f"Query failed: {e}")

# Main interaction loop
print("Initializing Chatbot...")
while True:
    user_input = input("").strip()

    if user_input.upper() == "END":
        print("Goodbye!")
        break
    
    if user_input.endswith("."): # stating a fact
        process_input(user_input)
    elif user_input.endswith("?"): # asking a question
        process_question(user_input)
    else:
        print("I don't understand that.")
