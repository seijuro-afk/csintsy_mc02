from pyswip import Prolog
prolog = Prolog()

statement_patterns = {
    "and are siblings": "sibling({0}, {1})",
    "is a sister of": "sister({0}, {1})",
    "is a mother of": "mother({0}, {1})",
    "is a grandmother of": "grandmother({0}, {1})",
    "is a child of": "child({0}, {1})",
    "is a daughter of": "daughter({0}, {1})",
    "is a uncle of": "uncle({0}, {1})",
    "is a brother of": "brother({0}, {1})",
    "is a father of": "father({0}, {1})",
    "and are the parents of": ["parent({0}, {2})", "parent({1}, {2})"],
    "is a grandfather of": "grandfather({0}, {1})",
    "and are the children of": ["child({0}, {3})", "child({1}, {3})", "child({2}, {3})"],
    "is a son of": "son({0}, {1})",
    "is an aunt of": "aunt({0}, {1})",
}

import re

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
                print("Pattern matched and fact added.")
                return
        elif phrase == "is a mother of":
            match = re.match(r"(\w+)\s+is\s+a\s+mother\s+of\s+(\w+)\.", user_input)
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
        elif phrase == "is a uncle of":
            match = re.match(r"(\w+)\s+is\s+a\s+uncle\s+of\s+(\w+)\.", user_input)
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
        elif phrase == "is a father of":
            match = re.match(r"(\w+)\s+is\s+a\s+father\s+of\s+(\w+)\.", user_input)
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



prolog.consult("FamilyRule.pl")

def add_fact(fact):
    try:
        prolog.assertz(fact)
        print("OK! I learned something.")
    except:
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


while True:
    user_input = input("").strip()

    if user_input.upper() == "END":
        print("Goodbye!")
        break
    
    if user_input.endswith("."):
        process_input(user_input)
    elif user_input.endswith("?"):
        print("Test 1")
    else:
        print("I don't understand that.")
    
