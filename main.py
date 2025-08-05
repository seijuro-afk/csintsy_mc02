from pyswip import Prolog
import re


prolog = Prolog()

prolog.consult("FamilyRule.pl")

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
    ", and are the children of": ["child({0}, {2})", "child({1}, {2})"], # Direct assertion
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

    # Questions that returns a list of names
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
    matched = False
    # Define regex patterns and their corresponding templates directly
    patterns_to_check = [
        (r"(\w+)\s+and\s+(\w+)\s+are\s+the\s+parents\s+of\s+(\w+)\.", ["parent({0}, {2})", "parent({1}, {2})"]),
        (r"(\w+)\s+and\s+(\w+)\s+are\s+children\s+of\s+(\w+)\.", ["child({0}, {2})", "child({1}, {2})"]),
        (r"(\w+)\s+and\s+(\w+)\s+are\s+siblings\.", "sibling_base({0}, {1})"),
        (r"(\w+)\s+is\s+an?\s+sister\s+of\s+(\w+)\.", "sister_base({0}, {1})"),
        (r"(\w+)\s+is\s+the\s+mother\s+of\s+(\w+)\.", "mother_base({0}, {1})"),
        (r"(\w+)\s+is\s+a\s+grandmother\s+of\s+(\w+)\.", "grandmother({0}, {1})"),
        (r"(\w+)\s+is\s+a\s+child\s+of\s+(\w+)\.", "child({0}, {1})"),
        (r"(\w+)\s+is\s+a\s+daughter\s+of\s+(\w+)\.", "daughter({0}, {1})"),
        (r"(\w+)\s+is\s+an\s+uncle\s+of\s+(\w+)\.", "uncle({0}, {1})"),
        (r"(\w+)\s+is\s+a\s+brother\s+of\s+(\w+)\.", "brother_base({0}, {1})"),
        (r"(\w+)\s+is\s+the\s+father\s+of\s+(\w+)\.", "father_base({0}, {1})"),
        (r"(\w+)\s+is\s+a\s+grandfather\s+of\s+(\w+)\.", "grandfather({0}, {1})"),
        (r"(\w+)\s+is\s+a\s+son\s+of\s+(\w+)\.", "son({0}, {1})"),
        (r"(\w+)\s+is\s+an\s+aunt\s+of\s+(\w+)\.", "aunt({0}, {1})"),
    ]

    for regex_pattern, template in patterns_to_check:
        match = re.match(regex_pattern, user_input)
        if match:
            groups = match.groups()
            # Convert all extracted names to lowercase for consistency with Prolog 
            groups_lc = tuple(g.lower() for g in groups)

            success = True  
            if isinstance(template, list):
                facts = [t.format(*groups_lc) for t in template]
                for fact in facts:
                    if not add_fact(fact):
                        success = False
                        break
            else:
                fact = template.format(*groups_lc)
                success = add_fact(fact)
                
            # Print a single success message if all facts were added
            if success:
                print("OK! I learned something.")
            else:
                print("That's impossible! (Consistency check failed)")
                
            matched = True
            break # Exit loop after matching

    if not matched:
        print("Unknown statement.")

# Function to process user questions
def process_question(user_input):
    for pattern, query_template in question_patterns.items():
        match = re.match(pattern, user_input)
        if match:
            groups = match.groups()
            # Convert all extracted names to lowercase for consistency with Prolog atoms
            groups_lc = tuple(g.lower() for g in groups)
            query = query_template.format(*groups_lc) # Use lowercased groups here

            # Check if this is a "Who" question (returns multiple results)
            if "Who are" in pattern or "Who is" in pattern:
                # Pass the lowercased reference person
                answer_who_question(query, pattern, groups_lc[-1] if groups_lc else None)
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

        # Reflexive relationships check (X cannot be related to X)
        if Y and X == Y:
            print(f"Consistency check failed: A person cannot be in a relationship with themselves ({X} and {Y} are the same).")
            return False

      
        # Parent-Child check (X is a child of B, X cannot be a child of A)
        if predicate in ["parent", "father_base", "mother_base"]:
            if Y and list(prolog.query(f"child({Y}, {X})")):
                print(f"Consistency check failed: {Y} cannot be a child of {X} if {X} is already a child of {Y}.")
                return False
        elif predicate == "child":
            if Y and list(prolog.query(f"child({Y}, {X})")):
                print(f"Consistency check failed: {Y} cannot be a child of {X} if {X} is already a child of {Y}.")
                return False

        # Child as Parent to own Parents check
        if predicate in ["father_base", "mother_base", "parent"]:
            if Y and list(prolog.query(f"child({X}, {Y})")):
                print(f"Consistency check failed: {X} cannot be a parent of {Y} if {X} is already a child of {Y} (circular relationship).")
                return False

        # Grandparent contradictions check
        if predicate in ["father_base", "mother_base"]:
            if Y and list(prolog.query(f"grandchild({X}, {Y})")):
                print(f"Consistency check failed: {X} cannot be parent of {Y} if {X} is already {Y}'s grandchild.")
                return False
            if Y and list(prolog.query(f"grandparent({Y}, {X})")):
                print(f"Consistency check failed: {X} cannot be parent of {Y} if {Y} is already {X}'s grandparent.")
                return False

   
        
        # Gender check for male
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
                
        # Gender check for female
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

        # A parent cannot be a child as an opposite sex (Example a father cannot be a daughter )
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

        # A child can only have one father or mother in the base facts
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

# add fact to Prolog after consistency check
def add_fact(fact):
    if is_consistent(fact):
        try:
            prolog.assertz(fact)
            return True  # Success
        except Exception as e:
            print(f"That's impossible! Error asserting fact: {e}")
            return False
    else:
        return False  # Consistency check failed

# answer yes or no questions
def answer_question(query):
    try:
        result = list(prolog.query(query))
        if result:
            print("Yes!")
        else:
            print("No!")
    except Exception as e:
        print(f"Invalid query: {e}")

# returns a list of names for "Who" questions
def answer_who_question(query, pattern, person):
    try:
        results = list(prolog.query(query))
        if results:
            names = [result['X'] for result in results]
            
            
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
                
                print(f"Found: {', '.join(names)}")
        else:
            print("No one found.")
    except Exception as e:
        print(f"Query failed: {e}")

# Main 
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
